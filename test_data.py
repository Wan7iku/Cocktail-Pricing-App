from database import SessionLocal
from models import Ingredient, Cocktail, Recipe

db = SessionLocal()

print("Ingredients:", db.query(Ingredient).count())
print("Cocktails:", db.query(Cocktail).count())
print("Recipes:", db.query(Recipe).count())

db.close()