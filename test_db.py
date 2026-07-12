from sqlalchemy import inspect
from database import engine

inspector = inspect(engine)

print("Tables in the database:")

for table in inspector.get_table_names():
    print("-", table)