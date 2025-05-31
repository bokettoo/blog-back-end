# schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Base for Blog posts (common fields)
class BlogBase(BaseModel):
    title: str
    content: str
    excerpt: Optional[str] = None # Added excerpt
    is_published: bool = False

# For creating new blog posts (includes optional slug if user wants to provide)
class BlogCreate(BlogBase):
    slug: Optional[str] = None # Allow providing custom slug, generate if None

# For updating existing blog posts
class BlogUpdate(BlogBase):
    # All fields are optional for update, so they can be partially updated
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    is_published: Optional[bool] = None
    slug: Optional[str] = None


# For reading blog posts (includes generated fields like id, dates)
class Blog(BlogBase):
    id: int
    slug: str # Slug is always present after creation
    publication_date: datetime
    last_updated: datetime

    class Config:
        orm_mode = True # Enables Pydantic to read ORM models

# Admin User Schemas
class AdminUserBase(BaseModel):
    username: str
    email: EmailStr

class AdminUserCreate(AdminUserBase):
    password: str

class AdminUser(AdminUserBase):
    id: int

    class Config:
        orm_mode = True

# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class AdminUserLogin(BaseModel):
    username: str
    password: str