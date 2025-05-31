# The Unfolding Mind Blog - Backend

This is the Python (FastAPI) backend for "The Unfolding Mind" personal blog. It provides a RESTful API for managing blog posts and handles user authentication (admin login) with JWT. The data is persisted in a PostgreSQL database.

## Features

- **RESTful API Endpoints:** For public blog access and protected admin operations.
- **JWT Authentication:** Secure login for admin users with access tokens.
- **Password Hashing:** Secure storage of admin passwords using bcrypt.
- **PostgreSQL Database:** Robust data storage for blogs and admin users.
- **SQLAlchemy ORM:** Pythonic database interaction.
- **Pydantic:** Data validation for API requests and responses.
- **Slug Generation:** Automatic creation of URL-friendly slugs for blog posts.
- **CORS Configuration:** Allows communication with your frontend.

## Technology Stack

- **Python 3.x**
- **FastAPI** (for building the API)
- **Uvicorn** (ASGI server)
- **PostgreSQL** (Database)
- **SQLAlchemy** (ORM for database interaction)
- **`psycopg2-binary`** (PostgreSQL adapter)
- **`python-jose[cryptography]`** (for JWT)
- **`passlib[bcrypt]`** (for password hashing)
- **`python-dotenv`** (for environment variables)
- **`python-slugify`** (for slug generation)

## Setup and Installation

1.  **Clone the repository (or navigate to your backend directory):**
    ```bash
    cd path/to/your/blog-backend
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    source venv/bin/activate # On macOS/Linux
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Database Setup (PostgreSQL)

1.  **Ensure PostgreSQL is Running:** Have a PostgreSQL server instance available (locally or remotely).
2.  **Create a Database:** Create an empty database (e.g., `blog_db`) for your blog.
3.  **Run Schema:** Execute the SQL commands in `sql_schema.sql` to create the necessary `blogs` and `admin_users` tables.
    ```bash
    psql -h <your_db_host> -p <your_db_port> -U <your_db_username> -d <your_db_name> -f sql_schema.sql
    ```
    (You will be prompted for your password).

## Environment Variables (`.env`)

Create a file named `.env` in the `blog-backend` directory (copy from `.env.example`) and fill in your database connection details and JWT secret:

```dotenv
DATABASE_URL="postgresql://user:password@host:port/dbname"
SECRET_KEY="your-super-secret-jwt-key" # Generate a strong random string!
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Admin User Setup (Crucial!)

After creating the `admin_users` table, you **must** insert at least one admin user.

1.  **Generate a hashed password:**
    ```bash
    python -c "from passlib.context import CryptContext; pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto'); print(pwd_context.hash('your_secure_password_here'))"
    ```
    Copy the long string output.
2.  **Insert into database (via `psql` or pgAdmin):**
    ```sql
    INSERT INTO admin_users (username, hashed_password, email)
    VALUES (
        'your_admin_username',
        'PASTE_YOUR_GENERATED_HASH_HERE',
        'admin@example.com'
    );
    ```

## Running the Server

From the parent directory of `blog-backend` (e.g., `theUnfoldingMind/`):

```bash
uvicorn back-end.main:app --reload --host 0.0.0.0 --port 8000
```

The API documentation (Swagger UI) will be available at `http://localhost:8000/docs`.

---
