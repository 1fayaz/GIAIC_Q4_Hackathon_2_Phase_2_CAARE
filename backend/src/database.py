import logging
from sqlmodel import Session, create_engine
from src.config.settings import settings
from contextlib import contextmanager
from src.models.user import User
from src.models.task import Task
from sqlmodel import SQLModel
import sys


# Validate DATABASE_URL at startup
if not settings.database_url or settings.database_url == "postgresql://user:password@localhost/dbname":
    logging.error("DATABASE_URL is not properly configured. Please check your .env file.")
    sys.exit(1)

logging.info(f"Connecting to database: {'*' * len(settings.database_url) if settings.database_url else 'None'}")

# Create the database engine (using sync engine for compatibility with current endpoints)
try:
    engine = create_engine(settings.database_url, echo=True)
    logging.info("Database engine created successfully")
except Exception as e:
    logging.error(f"Failed to create database engine: {e}")
    sys.exit(1)

# Import all models to ensure they are registered with SQLModel metadata before create_all
def register_models():
    """
    Explicitly import and register all models to ensure they're available for table creation
    """
    from src.models.user import User  # noqa: F401
    from src.models.task import Task  # noqa: F401
    logging.info(f"Models registered: {list(SQLModel.metadata.tables.keys())}")


def create_db_and_tables():
    """
    Create database tables if they don't exist
    """
    logging.info("Starting database table initialization...")
    logging.info(f"Database URL scheme: {settings.database_url.split(':')[0] if ':' in settings.database_url else 'unknown'}")

    # Register all models
    register_models()

    logging.info(f"SQLModel metadata contains {len(SQLModel.metadata.tables)} tables")
    for table_name in SQLModel.metadata.tables.keys():
        logging.info(f"  - Table: {table_name}")

    logging.info("Executing SQLModel.metadata.create_all(engine)...")
    try:
        SQLModel.metadata.create_all(engine)
        logging.info("Database tables initialized successfully")

        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logging.info(f"Tables found in database after initialization: {tables}")

        required_tables = ['user', 'task']
        missing_tables = [table for table in required_tables if table not in tables]
        if missing_tables:
            logging.warning(f"Missing tables after initialization: {missing_tables}")
        else:
            logging.info("All required tables are present")

    except Exception as e:
        logging.error(f"Failed to initialize database tables: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def get_session():
    """
    Get a database session
    """
    with Session(engine) as session:
        yield session


@contextmanager
def get_db_session():
    """
    Get a database session as a context manager
    """
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()