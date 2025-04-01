from sqlalchemy import create_engine, URL
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from decouple import config

# Load info from .env
host = config('host')
database = config('database')
user = config('user')
password = config('password')

# Create a connection url using SQL Alchemy's URL class
url = URL.create(
    database=database,
    username=user,
    password=password,
    host=host,
    drivername="postgresql+psycopg2"
)

# create a engine with above created url
engine = create_engine(url, echo=False)

try:
    engine.connect().close()

except OperationalError:
    print("No valid credentials, please ensure the presence of .env file")

# Create a session
def get_db():
    with Session(engine) as session:
        yield session
