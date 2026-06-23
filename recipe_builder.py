import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Recipe Builder",
    page_icon="🍸",
    layout="wide"
)

st.title("🍸 Cocktail Recipe Builder")

# -----------------------
# LOAD INGREDIENT DATABASE
# -----------------------

@st.cache_data
def load_ingredients():
    return pd.read_csv("data/ingredients_utf8.csv")

ingredients_df = load_ingredients()

# -----------------------
# GP TARGET
# -----------------------

target_gp = st.slider(
    "Target GP %",
    min_value=50,
    max_value=90,
    value=75
)

target_gp_decimal = target_gp / 100

# -----------------------
# COCKTAIL NAME
# -----------------------

cocktail_name = st.text_input(
    "Cocktail Name",
    placeholder="e.g Passion Mojito"
)

st.subheader("Recipe")

# -----------------------
# NUMBER OF INGREDIENTS
# -----------------------

num_ingredients = st.number_input(
    "Number of Ingredients",
    min_value=1,
    max_value=15,
    value=3
)

recipe_rows = []

# -----------------------
# INGREDIENT INPUTS
# -----------------------

for i in range(num_ingredients):

    col1, col2 = st.columns([3, 1])

    ingredient = col1.selectbox(
        f"Ingredient {i+1}",
        ingredients_df["ingredient_name"],
        key=f"ingredient_{i}"
    )

    quantity = col2.number_input(
        "Quantity (ml)",
        min_value=0.0,
        value=30.0,
        step=5.0,
        key=f"qty_{i}"
    )

    recipe_rows.append(
        {
            "ingredient_name": ingredient,
            "quantity_ml": quantity
        }
    )

# -----------------------
# CALCULATE BUTTON
# -----------------------

if st.button("Calculate Price"):

    recipe_df = pd.DataFrame(recipe_rows)

    merged = recipe_df.merge(
        ingredients_df,
        on="ingredient_name",
        how="left"
    )

    merged["ingredient_cost"] = (
        merged["quantity_ml"]
        * merged["cost_per_ml"]
    )

    total_cost = merged["ingredient_cost"].sum()

    # 10% spillage allowance
    cost_after_spillage = total_cost * 1.10

    recommended_price = (
        cost_after_spillage
        / (1 - target_gp_decimal)
    )

    selling_price_after_vat = (
        recommended_price
        * 1.16
    )

    expected_profit = (
        selling_price_after_vat
        - cost_after_spillage
    )

    # -----------------------
    # DISPLAY RESULTS
    # -----------------------

    st.success("Pricing Calculated")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Recipe Cost",
        f"KES {total_cost:,.2f}"
    )

    col2.metric(
        "Cost After Spillage",
        f"KES {cost_after_spillage:,.2f}"
    )

    col3.metric(
        "Recommended Price",
        f"KES {selling_price_after_vat:,.2f}"
    )

    col4.metric(
        "Expected Profit",
        f"KES {expected_profit:,.2f}"
    )

    gp = (
        expected_profit
        / selling_price_after_vat
    ) * 100

    st.metric(
        "Expected GP %",
        f"{gp:.1f}%"
    )

    st.subheader("Ingredient Cost Breakdown")

    st.dataframe(
        merged[
            [
                "ingredient_name",
                "quantity_ml",
                "cost_per_ml",
                "ingredient_cost"
            ]
        ],
        use_container_width=True
    )
