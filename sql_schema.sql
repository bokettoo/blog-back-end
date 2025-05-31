-- sql_schema.sql

-- Table for Blog Posts
CREATE TABLE IF NOT EXISTS blogs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    CONTENT TEXT NOT NULL,
    publication_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_published BOOLEAN DEFAULT FALSE,
    excerpt TEXT -- Added: Short summary or preview of the blog post
);

-- Add index for faster lookup by slug
CREATE INDEX IF NOT EXISTS idx_blogs_slug ON blogs (slug);

-- Add index for faster lookup by publication date (for chronological order)
CREATE INDEX IF NOT EXISTS idx_blogs_publication_date ON blogs (publication_date DESC);

-- Table for Admin Users
CREATE TABLE IF NOT EXISTS admin_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Initial Admin User (Run this ONLY ONCE after creating the table)
-- IMPORTANT: Replace 'your_admin_username', 'your_secure_password', and 'admin@example.com'
-- You should hash the password BEFORE inserting it. For production, NEVER store plain passwords.
-- Use a utility (like the Python script we discussed) to generate a hash first.
-- Example of how to get a hash (run in a Python shell):
-- from passlib.context import CryptContext
-- pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
-- print(pwd_context.hash("your_secure_password"))

-- INSERT INTO admin_users (username, hashed_password, email)
-- VALUES (
--     'your_admin_username',
--     '$2b$12$EXAMPLE_HASH_GENERATED_BY_PASSLIB.DO_NOT_STORE_PLAIN_TEXT', -- REPLACE WITH ACTUAL HASH
--     'admin@example.com'
-- );