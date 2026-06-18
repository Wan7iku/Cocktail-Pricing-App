import streamlit as st
import pandas as pd

df = pd.read_csv("data/cocktail_final_prices.csv")

st.title("🍸 Cocktail Pricing Engine")

target_gp = st.slider(
    "Target GP %",
    min_value=50,
    max_value=90,
    value=75
)
target_gp_decimal = target_gp / 100

cocktail = st.selectbox(
    "Choose Cocktail",
    df["cocktail_name"]
)

selected = df[df["cocktail_name"] == cocktail]
selected = selected.iloc[0]

selling_price = (
    selected["cost_after_spillage"]
    / (1 - target_gp_decimal)
)

final_price = selling_price * 1.16

profit = (
    selected["selling_price_after_vat"]
    - selected["total_cost"]
)

st.metric(
    "Base Cost",
    f"KES {selected['total_cost']:.2f}"
)

st.metric(
    "Menu Price",
    f"KES {selected['selling_price_after_vat']:.2f}"
)

st.metric(
    "Recommended Price",
    f"KES {final_price:.2f}"
)

st.metric(
    "Profit",
    f"KES {profit:.2f}"
)

st.dataframe(selected.to_frame().T)