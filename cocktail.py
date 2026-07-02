import streamlit as st

import pricing
import recipe_builder
import dashboard

st.set_page_config(
    page_title="Cocktail Costing System",
    layout="wide"
)

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a page",
    [
        "Pricing Engine",
        "Recipe Builder",
        "Cocktail Dashboard"
    ]
)

if page == "Pricing Engine":
    pricing.show()

elif page == "Recipe Builder":
    recipe_builder.show()

elif page == "Cocktail Dashboard":
    dashboard.show()