import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///cocktail.db")

ingredients = pd.read_sql(
    "SELECT * FROM ingredients",
    engine
)