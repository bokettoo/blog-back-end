from passlib.context import CryptContext

# Instantiate the password context (as defined in auth.py)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Your chosen secure password for the admin user
your_admin_password = "Bokettoiswise2811Blog" # CHANGE THIS!

# Generate the hash
hashed_password = pwd_context.hash(your_admin_password)
print(hashed_password)
