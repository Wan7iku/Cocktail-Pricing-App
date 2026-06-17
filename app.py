import streamlit as st
import pandas as pd

st.title("Cocktail Pricing Engine")

df = pd.read_csv("data/cocktail_final_prices.csv")

st.dataframe(df)