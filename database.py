import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Declarative base from SQLAlchemy
Base = declarative_base()

try:
    # Database connection specifics for local PostgreSQL connection
    server = os.environ["DB_SERVER"]
    user = os.environ["DB_USER"]
    password = os.environ["DB_PASSWORD"]
    database = os.environ["DB_NAME"]
    conn_string = f"postgresql+psycopg2://{user}:{password}@{server}/{database}"

    # Create engine
    engine = create_engine(conn_string)
except KeyError:
    pass

# Initialise session class
Session = sessionmaker()