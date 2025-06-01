from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from slugify import slugify
from datetime import timedelta
from typing import Optional # <--- Make sure this is imported!

from . import models, schemas, auth
from .database import engine, get_db
import os

# Create database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="The Unfolding Mind Blog API",
    description="Backend API for The Unfolding Mind personal blog.",
    version="1.0.0",
)

# CORS Configuration
origins = [
    "http://localhost:5173", # Your React frontend development URL (Vite default)
    "http://127.0.0.1:5173",
    # Add your production frontend URL here when deployed
    # "https://your-production-blog-url.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Public Blog Endpoints ---

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.get("/api/blogs", response_model=list[schemas.Blog])
def get_all_published_blogs(db: Session = Depends(get_db)):
    """
    Retrieve all published blog posts, sorted chronologically descending.
    """
    blogs = db.query(models.Blog).filter(models.Blog.is_published == True).order_by(desc(models.Blog.publication_date)).all()
    return blogs

@app.get("/api/blogs/latest", response_model=Optional[schemas.Blog]) # <--- CRITICAL CHANGE: Added Optional!
def get_latest_published_blog(db: Session = Depends(get_db)):
    """
    Retrieve the single latest published blog post.
    """
    latest_blog = db.query(models.Blog).filter(models.Blog.is_published == True).order_by(desc(models.Blog.publication_date)).first()
    # --- CRITICAL CHANGE: Removed the 'if latest_blog is None: raise HTTPException(...)' block! ---
    return latest_blog # FastAPI will now correctly return null with 200 OK if latest_blog is None

@app.get("/api/blogs/{slug}", response_model=schemas.Blog)
def get_blog_by_slug(slug: str, db: Session = Depends(get_db)):
    """
    Retrieve a single published blog post by its slug.
    """
    blog = db.query(models.Blog).filter(models.Blog.slug == slug, models.Blog.is_published == True).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found or not published")
    return blog

# --- (Rest of your admin endpoints are below this point in the full main.py) ---
# --- Admin Authentication Endpoint ---

@app.post("/api/admin/login", response_model=schemas.Token)
def admin_login(user_credentials: schemas.AdminUserLogin, db: Session = Depends(get_db)):
    """
    Authenticate an admin user and return an access token.
    """
    user = db.query(models.AdminUser).filter(models.AdminUser.username == user_credentials.username).first()
    if not user or not auth.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# --- Admin Blog Management Endpoints (Protected) ---
@app.post("/api/admin/blogs", response_model=schemas.Blog, status_code=status.HTTP_201_CREATED)
def create_blog_post(blog: schemas.BlogCreate, db: Session = Depends(get_db),
                     current_user: models.AdminUser = Depends(auth.get_current_admin_user)):
    """
    Create a new blog post. Requires admin authentication.
    """
    if not blog.slug:
        blog.slug = slugify(blog.title) # Generate slug from title if not provided
        if not blog.slug:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title or slug must be provided.")

    existing_blog = db.query(models.Blog).filter(models.Blog.slug == blog.slug).first()
    if existing_blog:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A blog with this slug already exists.")

    # --- NO CHANGE NEEDED HERE ---
    # blog.dict() will include publication_date if it was set in the schema,
    # otherwise, models.py default will kick in.
    db_blog = models.Blog(**blog.dict())
    # --- END NO CHANGE ---

    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

@app.get("/api/admin/blogs", response_model=list[schemas.Blog])
def get_all_admin_blogs(db: Session = Depends(get_db),
                        current_user: models.AdminUser = Depends(auth.get_current_admin_user)):
    """
    Retrieve all blog posts (published and unpublished). Requires admin authentication.
    """
    blogs = db.query(models.Blog).order_by(desc(models.Blog.publication_date)).all()
    return blogs

@app.get("/api/admin/blogs/{blog_id}", response_model=schemas.Blog)
def get_admin_blog_by_id(blog_id: int, db: Session = Depends(get_db),
                         current_user: models.AdminUser = Depends(auth.get_current_admin_user)):
    """
    Retrieve a single blog post by its ID. Requires admin authentication.
    """
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog

@app.put("/api/admin/blogs/{blog_id}", response_model=schemas.Blog)
def update_blog_post(blog_id: int, blog_update: schemas.BlogUpdate, db: Session = Depends(get_db),
                     current_user: models.AdminUser = Depends(auth.get_current_admin_user)):
    """
    Update an existing blog post by its ID. Requires admin authentication.
    """
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if db_blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    update_data = blog_update.dict(exclude_unset=True)

    if 'title' in update_data and 'slug' not in update_data:
        update_data['slug'] = slugify(update_data['title'])

    if 'slug' in update_data and update_data['slug'] != db_blog.slug:
        existing_blog_with_new_slug = db.query(models.Blog).filter(models.Blog.slug == update_data['slug'], models.Blog.id != blog_id).first()
        if existing_blog_with_new_slug:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A blog with this slug already exists.")

    for key, value in update_data.items():
        setattr(db_blog, key, value)

    db.add(db_blog)
    db_blog.last_updated = func.now() # Manually update last_updated
    db.commit()
    db.refresh(db_blog)
    return db_blog

@app.delete("/api/admin/blogs/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog_post(blog_id: int, db: Session = Depends(get_db),
                     current_user: models.AdminUser = Depends(auth.get_current_admin_user)):
    """
    Delete a blog post by its ID. Requires admin authentication.
    """
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if db_blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    db.delete(db_blog)
    db.commit()
    return {"message": "Blog deleted successfully"}