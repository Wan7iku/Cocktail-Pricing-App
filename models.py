from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Date,
)
class Base(DeclarativeBase):
    pass
class Ingredient(Base):

    __tablename__ = "ingredients"

    ingredient_id = Column(Integer, primary_key=True, autoincrement=True)

    ingredient_name = Column(String, nullable=False)

    unit = Column(String, nullable=False)

    cost_per_unit = Column(Float, nullable=False)

    category = Column(String)

    supplier_id = Column(Integer)

    recipes = relationship("Recipe", back_populates="ingredient")

class Cocktail(Base):

    __tablename__ = "cocktails"

    cocktail_id = Column(String, primary_key=True)

    cocktail_name = Column(String, nullable=False)

    total_cost = Column(Float)

    cost_after_spillage = Column(Float)

    selling_price_before_vat = Column(Float)

    selling_price_after_vat = Column(Float)

    recipes = relationship("Recipe", back_populates="cocktail")

class Recipe(Base):

    __tablename__ = "recipes"

    recipe_id = Column(Integer, primary_key=True, autoincrement=True)

    cocktail_id = Column(
        String,
        ForeignKey("cocktails.cocktail_id")
    )

    ingredient_id = Column(
        Integer,
        ForeignKey("ingredients.ingredient_id")
    )

    quantity = Column(Float)

    unit = Column(String)

    cocktail = relationship(
        "Cocktail",
        back_populates="recipes"
    )

    ingredient = relationship(
        "Ingredient",
        back_populates="recipes"
    )
class Inventory(Base):

    __tablename__ = "inventory"

    inventory_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    ingredient_id = Column(
        Integer,
        ForeignKey("ingredients.ingredient_id")
    )

    quantity_in_stock = Column(Float)

    minimum_stock = Column(Float)
class Sale(Base):

    __tablename__ = "sales"

    sale_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    cocktail_id = Column(
        String,
        ForeignKey("cocktails.cocktail_id")
    )

    sale_date = Column(Date)

    quantity = Column(Integer)

    selling_price = Column(Float)
class Supplier(Base):

    __tablename__ = "suppliers"

    supplier_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    supplier_name = Column(String)

    phone = Column(String)

    email = Column(String)
supplier_id = Column(
    Integer,
    ForeignKey("suppliers.supplier_id"),
    nullable=True
)

supplier = relationship("Supplier")