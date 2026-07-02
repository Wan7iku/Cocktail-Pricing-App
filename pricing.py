import streamlit as st

def show():
    st.title("Cocktail Pricing Engine")
from pathlib import Path

import pandas as pd


DATA_PATH = Path("data/cocktail_final_prices.csv")
NUMERIC_COLUMNS = [
    "total_cost",
    "cost_after_spillage",
    "selling_price_before_vat",
    "selling_price_after_vat",
]


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


df = load_data(DATA_PATH)


target_gp = st.slider(
    "Target GP %",
    min_value=50,
    max_value=90,
    value=75,
)
target_gp_decimal = target_gp / 100

price_change = st.slider(
    "Increase Price %",
    0,
    50,
    0,
)

cocktail_1 = st.selectbox(
    "Cocktail A",
    df["cocktail_name"].dropna().tolist(),
)

cocktail_2 = st.selectbox(
    "Cocktail B",
    df["cocktail_name"].dropna().tolist(),
    index=1,
)

selected_1 = df.loc[df["cocktail_name"] == cocktail_1]
selected_2 = df.loc[df["cocktail_name"] == cocktail_2]

if selected_1.empty or selected_2.empty:
    st.error("No matching cocktail found.")
    st.stop()

selected_1 = selected_1.iloc[0]
selected_2 = selected_2.iloc[0]

base_cost_1 = pd.to_numeric(selected_1.get("total_cost"), errors="coerce")
menu_price_1 = pd.to_numeric(selected_1.get("selling_price_after_vat"), errors="coerce")
cost_after_spillage_1 = pd.to_numeric(selected_1.get("cost_after_spillage"), errors="coerce")

base_cost_2 = pd.to_numeric(selected_2.get("total_cost"), errors="coerce")
menu_price_2 = pd.to_numeric(selected_2.get("selling_price_after_vat"), errors="coerce")
cost_after_spillage_2 = pd.to_numeric(selected_2.get("cost_after_spillage"), errors="coerce")

if pd.isna(base_cost_1) or pd.isna(menu_price_1) or pd.isna(cost_after_spillage_1):
    st.error(f"Missing pricing data for {cocktail_1}.")
    st.stop()

if pd.isna(base_cost_2) or pd.isna(menu_price_2) or pd.isna(cost_after_spillage_2):
    st.error(f"Missing pricing data for {cocktail_2}.")
    st.stop()

recommended_price_before_vat_1 = cost_after_spillage_1 / (1 - target_gp_decimal)
recommended_price_1 = recommended_price_before_vat_1 * 1.16
recommended_price_1 *= 1 + (price_change / 100)

recommended_price_before_vat_2 = cost_after_spillage_2 / (1 - target_gp_decimal)
recommended_price_2 = recommended_price_before_vat_2 * 1.16
recommended_price_2 *= 1 + (price_change / 100)

current_profit_1 = menu_price_1 - base_cost_1
recommended_profit_1 = recommended_price_1 - base_cost_1
current_gp_1 = ((menu_price_1 - cost_after_spillage_1) / menu_price_1) * 100 if menu_price_1 else 0
recommended_gp_1 = ((recommended_price_1 - cost_after_spillage_1) / recommended_price_1) * 100 if recommended_price_1 else 0
current_markup_1 = menu_price_1 / cost_after_spillage_1 if cost_after_spillage_1 else 0
recommended_markup_1 = recommended_price_1 / cost_after_spillage_1 if cost_after_spillage_1 else 0

current_profit_2 = menu_price_2 - base_cost_2
recommended_profit_2 = recommended_price_2 - base_cost_2
current_gp_2 = ((menu_price_2 - cost_after_spillage_2) / menu_price_2) * 100 if menu_price_2 else 0
recommended_gp_2 = ((recommended_price_2 - cost_after_spillage_2) / recommended_price_2) * 100 if recommended_price_2 else 0
current_markup_2 = menu_price_2 / cost_after_spillage_2 if cost_after_spillage_2 else 0
recommended_markup_2 = recommended_price_2 / cost_after_spillage_2 if cost_after_spillage_2 else 0


def money(value: float) -> str:
    return f"KES {value:,.2f}"


col1, col2 = st.columns(2)
with col1:
    st.subheader(cocktail_1)
    st.metric("Base Cost", money(base_cost_1))
    st.metric("Current Menu Price", money(menu_price_1))
    st.metric("Recommended Menu Price", money(recommended_price_1))
    st.metric("Current Profit", money(current_profit_1))
    st.metric("Recommended Profit", money(recommended_profit_1))
    st.metric("Current GP %", f"{current_gp_1:.1f}%")
    st.metric("Recommended GP %", f"{recommended_gp_1:.1f}%")
    st.metric("Current Markup", f"{current_markup_1:.2f}x")
    st.metric("Recommended Markup", f"{recommended_markup_1:.2f}x")
    if recommended_gp_1 >= 75:
        st.success("Excellent Margin")
    elif recommended_gp_1 >= 65:
        st.warning("Acceptable Margin")
    else:
        st.error("Low Margin")

with col2:
    st.subheader(cocktail_2)
    st.metric("Base Cost", money(base_cost_2))
    st.metric("Current Menu Price", money(menu_price_2))
    st.metric("Recommended Menu Price", money(recommended_price_2))
    st.metric("Current Profit", money(current_profit_2))
    st.metric("Recommended Profit", money(recommended_profit_2))
    st.metric("Current GP %", f"{current_gp_2:.1f}%")
    st.metric("Recommended GP %", f"{recommended_gp_2:.1f}%")
    st.metric("Current Markup", f"{current_markup_2:.2f}x")
    st.metric("Recommended Markup", f"{recommended_markup_2:.2f}x")
    if recommended_gp_2 >= 75:
        st.success("Excellent Margin")
    elif recommended_gp_2 >= 65:
        st.warning("Acceptable Margin")
    else:
        st.error("Low Margin")

st.subheader("Ingredient Cost Breakdown")

st.dataframe(
    pd.concat([selected_1.to_frame().T, selected_2.to_frame().T], ignore_index=True),
    width="stretch",
)