import pandas as pd

from database import SessionLocal
from models import Ingredient, Cocktail, Recipe
db = SessionLocal()
def import_ingredients():

    df = pd.read_csv("Ingredients_utf8.csv")

    count = 0

    for _, row in df.iterrows():

        existing = (
            db.query(Ingredient)
            .filter_by(
                ingredient_name=row["ingredient_id"]
            )
            .first()
        )

        if existing:
            continue

        ingredient = Ingredient(
            ingredient_name=row["ingredient_name"],
            unit=row["unit"],
            cost_per_unit=float(row["cost_per_unit"]),
            category=row.get("category", None)
        )

        db.add(ingredient)

        count += 1

    db.commit()

    print(f"✅ Imported {count} ingredients")

def import_cocktails():

    df = pd.read_csv("data/cocktail_fin_prices.csv")

    count = 0

    for _, row in df.iterrows():

        existing = (
            db.query(Cocktail)
            .filter_by(
                cocktail_id=row["cocktail_id"]
            )
            .first()
        )

        if existing:
            continue

        cocktail = Cocktail(

            cocktail_id=row["cocktail_id"],

            cocktail_name=row["cocktail_name"],

            total_cost=float(row["total_cost"]),

            cost_after_spillage=float(row["cost_after_spillage"]),

            selling_price_before_vat=float(
                row.get(
                    "selling_price_before_vat",
                    0
                )
            ),

            selling_price_after_vat=float(
                row["selling_price_after_vat"]
            )

        )

        db.add(cocktail)

        count += 1

    db.commit()

    print(f"✅ Imported {count} cocktails") 
    
def import_recipes():

    df = pd.read_csv("data/recipes.csv")

    count = 0

    for _, row in df.iterrows():

        ingredient = (
            db.query(Ingredient)
            .filter_by(
                ingredient_name=row["ingredient_name"]
            )
            .first()
        )

        if ingredient is None:
            continue

        recipe = Recipe(

            cocktail_id=row["cocktail_id"],

            ingredient_id=row["ingredient_id"],

            quantity=float(row["unit_quantity"]),
            )

        db.add(recipe)

        count += 1

    db.commit()

    print(f"✅ Imported {count} recipe rows")
if __name__ == "__main__":

    print("Starting import...\n")

    import_ingredients()

    import_cocktails()

    import_recipes()

    db.close()

    print("\n🎉 Database import completed!")
