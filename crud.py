from sqlalchemy.orm import Session

from database import SessionLocal

from models import (
    Ingredient,
    Cocktail,
    Recipe,
)
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
def get_all_ingredients():

    db = SessionLocal()

    ingredients = (
        db.query(Ingredient)
        .order_by(Ingredient.ingredient_name)
        .all()
    )

    db.close()

    return ingredients
def get_ingredient_by_name(name):

    db = SessionLocal()

    ingredient = (
        db.query(Ingredient)
        .filter(
            Ingredient.ingredient_name == name
        )
        .first()
    )

    db.close()

    return ingredient
def add_ingredient(
    ingredient_name,
    unit,
    cost_per_unit,
    category=None,
):

    db = SessionLocal()

    ingredient = Ingredient(
        ingredient_name=ingredient_name,
        unit=unit,
        cost_per_unit=cost_per_unit,
        category=category,
    )

    db.add(ingredient)

    db.commit()

    db.refresh(ingredient)

    db.close()

    return ingredient
def get_all_cocktails():

    db = SessionLocal()

    cocktails = (
        db.query(Cocktail)
        .order_by(Cocktail.cocktail_name)
        .all()
    )

    db.close()

    return cocktails
def get_cocktail(cocktail_id):

    db = SessionLocal()

    cocktail = (
        db.query(Cocktail)
        .filter(
            Cocktail.cocktail_id == cocktail_id
        )
        .first()
    )

    db.close()

    return cocktail
def add_cocktail(
    cocktail_id,
    cocktail_name,
    total_cost,
    cost_after_spillage,
    selling_price_before_vat,
    selling_price_after_vat,
):

    db = SessionLocal()

    cocktail = Cocktail(

        cocktail_id=cocktail_id,

        cocktail_name=cocktail_name,

        total_cost=total_cost,

        cost_after_spillage=cost_after_spillage,

        selling_price_before_vat=selling_price_before_vat,

        selling_price_after_vat=selling_price_after_vat,

    )

    db.add(cocktail)

    db.commit()

    db.refresh(cocktail)

    db.close()

    return cocktail
def get_all_cocktails():

    db = SessionLocal()

    cocktails = (
        db.query(Cocktail)
        .order_by(Cocktail.cocktail_name)
        .all()
    )

    db.close()

    return cocktails
def get_cocktail(cocktail_id):

    db = SessionLocal()

    cocktail = (
        db.query(Cocktail)
        .filter(
            Cocktail.cocktail_id == cocktail_id
        )
        .first()
    )

    db.close()

    return cocktail
def add_cocktail(
    cocktail_id,
    cocktail_name,
    total_cost,
    cost_after_spillage,
    selling_price_before_vat,
    selling_price_after_vat,
):

    db = SessionLocal()

    cocktail = Cocktail(

        cocktail_id=cocktail_id,

        cocktail_name=cocktail_name,

        total_cost=total_cost,

        cost_after_spillage=cost_after_spillage,

        selling_price_before_vat=selling_price_before_vat,

        selling_price_after_vat=selling_price_after_vat,

    )

    db.add(cocktail)

    db.commit()

    db.refresh(cocktail)

    db.close()

    return cocktail
def add_recipe(
    cocktail_id,
    ingredient_id,
    quantity,
    unit,
):

    db = SessionLocal()

    recipe = Recipe(

        cocktail_id=cocktail_id,

        ingredient_id=ingredient_id,

        quantity=quantity,

        unit=unit,

    )

    db.add(recipe)

    db.commit()

    db.refresh(recipe)

    db.close()

    return recipe
def get_recipe(cocktail_id):

    db = SessionLocal()

    recipe = (
        db.query(Recipe)
        .filter(
            Recipe.cocktail_id == cocktail_id
        )
        .all()
    )

    db.close()

    return recipe
def delete_cocktail(cocktail_id):

    db = SessionLocal()

    cocktail = (
        db.query(Cocktail)
        .filter(
            Cocktail.cocktail_id == cocktail_id
        )
        .first()
    )

    if cocktail:

        db.delete(cocktail)

        db.commit()

    db.close()
