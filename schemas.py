# schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Base for Blog posts (common fields)
class BlogBase(BaseModel):
    title: str
    content: str
    excerpt: Optional[str] = None
    is_published: bool = False
    publication_date: Optional[datetime] = None # <--- ADDED: Allow setting publication_date

# For creating new blog posts (includes optional slug if user wants to provide)
class BlogCreate(BlogBase):
    slug: Optional[str] = None

# For updating existing blog posts
class BlogUpdate(BlogBase):
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    is_published: Optional[bool] = None
    slug: Optional[str] = None
    publication_date: Optional[datetime] = None # <--- ADDED: Allow updating publication_date

# For reading blog posts (includes generated fields like id, dates)
class Blog(BlogBase):
    id: int
    slug: str
    # publication_date is already here
    last_updated: datetime

    class Config:
        orm_mode = True

# Admin User Schemas (no changes)
class AdminUserBase(BaseModel):
    username: str
    email: EmailStr

class AdminUserCreate(AdminUserBase):
    password: str

class AdminUser(AdminUserBase):
    id: int

    class Config:
        orm_mode = True

# Authentication Schemas (no changes)
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class AdminUserLogin(BaseModel):
    username: str
    password: str