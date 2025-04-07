from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Get the base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'zzp_tracker.db')}"

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Get a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize the database by creating all tables"""
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(DATABASE_URL.replace('sqlite:///', '')), exist_ok=True)
    
    # Import all models here to ensure they are registered with the Base
    from models.objects import Base, Transaction, Income, Expense
    
    # Create all tables
    Base.metadata.create_all(bind=engine) 
     