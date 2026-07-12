from database import engine
from models import Base

def create_database():
    """
    Create all tables defined in models.py
    """
    Base.metadata.create_all(bind=engine)
    print("✅ cocktail.db created successfully!")
    print("✅ All tables have been created.")

if __name__ == "__main__":
    create_database()