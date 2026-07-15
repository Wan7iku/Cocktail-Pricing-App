import streamlit as st
import pandas as pd
from crud import (
    get_all_ingredients,
    get_all_cocktails,
    get_ingredient_by_name,
    add_cocktail,
    add_recipe,
)

def show():

    st.title("🍸 Recipe Builder")
    
    # -----------------------
    # LOAD INGREDIENT DATABASE
    # -----------------------
    ingredients = get_all_ingredients()

    ingredients_df = pd.DataFrame(
        [
            {
                "ingredient_id": i.ingredient_id,
                "ingredient_name": i.ingredient_name,
                "cost_per_unit": i.cost_per_unit,
                "unit": i.unit,
            }
            for i in ingredients
        ]
    )
    # -----------------------
    # GP TARGET
    # -----------------------

    target_gp = st.slider(
        "Target GP %",
        min_value=50,
        max_value=90,
        value=75,
        key="recipe_target_gp",
    )

    target_gp_decimal = target_gp / 100

    # -----------------------
    # COCKTAIL DETAILS
    # -----------------------

    cocktail_name = st.text_input(
        "Cocktail Name",
        placeholder="e.g Passion Mojito",
        key="recipe_name",
    )

    cocktail_id = st.text_input(
        "Cocktail ID",
        placeholder="e.g. w10rr",
        key="recipe_id",
    )

    st.subheader("Recipe")

    # -----------------------
    # NUMBER OF INGREDIENTS
    # -----------------------

    num_ingredients = st.number_input(
        "Number of Ingredients",
        min_value=1,
        max_value=15,
        value=3,
        key="recipe_num_ingredients",
    )

    recipe_rows = []

    # -----------------------
    # INGREDIENT INPUTS
    # -----------------------

    for i in range(num_ingredients):

        col1, col2, col3 = st.columns([3, 1, 1])

        ingredient = col1.selectbox(
            f"Ingredient {i+1}",
            ingredients_df["ingredient_name"],
            key=f"ingredient_{i}",
        )

        quantity = col2.number_input(
            "Quantity",
            min_value=0.0,
            value=30.0,
            key=f"qty_{i}",
        )

        unit = col3.selectbox(
            "Unit",
            ["ml", "pcs"],
            key=f"unit_{i}",
        )

        recipe_rows.append(
            {
                "Cocktail_id": cocktail_id,
                "ingredient_name": ingredient,
                "quantity": quantity,
                "unit": unit,
            }
        )

    # -----------------------
    # CALCULATE PRICE
    # -----------------------

    if st.button("Calculate Price", key="calculate_recipe"):

        recipe_df = pd.DataFrame(recipe_rows)

        merged = recipe_df.merge(
            ingredients_df[
                [
                    "ingredient_id",
                    "ingredient_name",
                    "cost_per_unit",
                ]
            ],
            on="ingredient_name",
            how="left",
        )

        merged["unit_cost"] = merged["cost_per_unit"]

        merged["ingredient_cost"] = (
            merged["quantity"] * merged["unit_cost"]
        )

        total_cost = merged["ingredient_cost"].sum()

        cost_after_spillage = total_cost * 1.10

        recommended_price = (
            cost_after_spillage
            / (1 - target_gp_decimal)
        )

        selling_price_after_vat = recommended_price * 1.16

        expected_profit = (
            selling_price_after_vat
            - cost_after_spillage
        )

        gp = (
            expected_profit
            / selling_price_after_vat
        ) * 100

        st.session_state["merged"] = merged
        st.session_state["total_cost"] = total_cost
        st.session_state["cost_after_spillage"] = cost_after_spillage
        st.session_state["selling_price_after_vat"] = (
            selling_price_after_vat
        )
        st.session_state["gp"] = gp

        st.success("Pricing Calculated")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Recipe Cost", f"KES {total_cost:,.2f}")
        c2.metric(
            "Cost After Spillage",
            f"KES {cost_after_spillage:,.2f}",
        )
        c3.metric(
            "Recommended Price",
            f"KES {selling_price_after_vat:,.2f}",
        )
        c4.metric(
            "Expected Profit",
            f"KES {expected_profit:,.2f}",
        )

        st.metric("Expected GP %", f"{gp:.1f}%")

        st.subheader("Ingredient Cost Breakdown")

        st.dataframe(
            merged[
                [
                    "ingredient_name",
                    "quantity",
                    "unit",
                    "unit_cost",
                    "ingredient_cost",
                ]
            ],
            use_container_width=True,
        )

    # -----------------------
    # SAVE COCKTAIL
    # -----------------------

    if st.button("Save Cocktail", key="save_recipe"):

        if not cocktail_name.strip():
            st.error("Please enter a cocktail name.")
            st.stop()

        if not cocktail_id.strip():
            st.error("Please enter a cocktail ID.")
            st.stop()

        if "merged" not in st.session_state:
            st.error(
                "Please calculate the recipe before saving."
            )
            st.stop()

        cocktails = get_all_cocktails()

        existing_ids = [
          c.cocktail_id
        for c in cocktails
       ]

        if cocktail_id in existing_ids:
         st.error("Cocktail ID already exists.")
         st.stop()

        merged = st.session_state["merged"]

        total_cost = st.session_state["total_cost"]

        cost_after_spillage = st.session_state[
            "cost_after_spillage"
        ]

        selling_price_after_vat = st.session_state[
            "selling_price_after_vat"
        ]

        add_cocktail(
            cocktail_id=cocktail_id,
            cocktail_name=cocktail_name,
            total_cost=total_cost,
            cost_after_spillage=cost_after_spillage,
            selling_price_before_vat=(
               cost_after_spillage /
               (1 - target_gp_decimal)
         ),
         selling_price_after_vat=selling_price_after_vat,
        )
        for _, row in merged.iterrows():
          ingredient = get_ingredient_by_name(
            row["ingredient_name"]
        )

        add_recipe(
           cocktail_id=cocktail_id,
           ingredient_id=ingredient.ingredient_id,
           quantity=row["quantity"],
            unit=row["unit"],
        )
    st.success(
         f"{cocktail_name} saved successfully! "
         f"(ID: {cocktail_id})"
    )