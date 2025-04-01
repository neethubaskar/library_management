# Library Management System Using FASTAPI

This is a simple library management system's api created using FastAPI for the endpoint, SQLAlchemy for ORM and PostgreSQL for the backend database.

# How to run this code?

1. Clone the repository:
   ```bash
   git clone https://github.com/neethubaskar/library_management.git
2. Navigate to the project directory:
   ```bash
   cd library_management
3. Create a .env file The file must follow this format
  ```bash
    host=database_host
    database=database_name
    user=database_username
    password=database_password
    secret=AccessToken_secret_key
    algorithm=Token_algorithm
4. Install the requirements
  ```bash
   pip install -r requirements.txt
5. Run the script
  Run the script with uvicorn main:app --reload

