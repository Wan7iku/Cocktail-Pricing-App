import git
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

cocktail_id = st.text_input(
    "Cocktail ID",
    placeholder="e.g. w10rr"
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

 col1, col2, col3 = st.columns([3, 1, 1])

 ingredient = col1.selectbox(
      f"Ingredient {i+1}",
      ingredients_df["ingredient_name"],
      key=f"ingredient_{i}"
 )

 quantity = col2.number_input(
    "Quantity",
    min_value=0.0,
    value=30.0,
    key=f"qty_{i}"
 )

 unit = col3.selectbox(
    "Unit",
    ["ml", "pcs"],
    key=f"unit_{i}"
 )

 recipe_rows.append({
    "ingredient_name": ingredient,
    "quantity": quantity,
    "unit": unit
 })

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

    st.write("Recipe columns:", recipe_df.columns.tolist())
    st.write("Ingredient columns:", ingredients_df.columns.tolist())
    st.write("Merged columns:", merged.columns.tolist())
    # Calculate ingredient cost based on selected unit
    
    merged["unit_cost"] = merged["cost_per_unit"]

    merged["ingredient_cost"] = (
     merged["quantity"]
     * merged["unit_cost"]
   )

    merged["ingredient_cost"] = (
        merged["quantity"]
        * merged["unit_cost"]
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

    gp = (
        expected_profit
        / selling_price_after_vat
    ) * 100

    # Save results for later use by Save button

    st.session_state["merged"] = merged
    st.session_state["total_cost"] = total_cost
    st.session_state["cost_after_spillage"] = cost_after_spillage
    st.session_state["selling_price_after_vat"] = selling_price_after_vat
    st.session_state["gp"] = gp

    # DISPLAY RESULTS

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

    st.metric(
        "Expected GP %",
        f"{gp:.1f}%"
    )

    st.subheader("Ingredient Cost Breakdown")

    st.dataframe(
        merged[
            [
                "ingredient_name",
                "quantity",
                "unit",
                "unit_cost",
                "ingredient_cost"
            ]
        ],
        use_container_width=True
    )


# -----------------------------------
# SAVE COCKTAIL
# -----------------------------------
if st.button("Save Cocktail"):

    # Validate inputs FIRST

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

    cocktails_df = pd.read_csv(
        "data/cocktail_fin_prices.csv"
    )

    # Prevent duplicate IDs

    if cocktail_id in cocktails_df["cocktail_id"].astype(str).values:
        st.error("This Cocktail ID already exists.")
        st.stop()

    merged = st.session_state["merged"]

    total_cost = st.session_state["total_cost"]

    cost_after_spillage = st.session_state[
        "cost_after_spillage"
    ]

    selling_price_after_vat = st.session_state[
        "selling_price_after_vat"
    ]

    # -------------------------
    # SAVE RECIPE
    # -------------------------

    recipe_save = merged.copy()

    recipe_save["cocktail_id"] = cocktail_id
    recipe_save["cocktail_name"] = cocktail_name

    recipe_save.to_csv(
        "data/cocktail_recipes.csv",
        mode="a",
        header=False,
        index=False
    )

    # -------------------------
    # SAVE COCKTAIL SUMMARY
    # -------------------------

    new_cocktail = pd.DataFrame([{
        "cocktail_id": cocktail_id,
        "cocktail_name": cocktail_name,
        "total_cost": total_cost,
        "cost_after_spillage": cost_after_spillage,
        "selling_price_after_vat": selling_price_after_vat
    }])

    new_cocktail.to_csv(
        "data/cocktail_fin_prices.csv",
        mode="a",
        header=False,
        index=False
    )

    st.success(
        f"{cocktail_name} saved successfully! "
        f"(ID: {cocktail_id})"
    )
