from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite database
DATABASE_URL = "sqlite:///cocktail.db"

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=False
)

# Create session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)