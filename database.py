from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)  # To esstablish connection w database
Base = (
    declarative_base()
)  # This is for defining/giving a schema for a class which can be used as a table
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False
)  # Create a session


def get_db():
    """function is used to create a new SQLAlchemy database session for each request."""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e  # Re-raise the exception so FastAPI can handle it properly
    finally:
        db.close()
