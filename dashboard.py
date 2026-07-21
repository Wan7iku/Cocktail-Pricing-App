import streamlit as st
import pandas as pd
import plotly.express as px

from sqlalchemy import text
from sqlalchemy import create_engine
from database import engine

DATABASE_URL = "sqlite:///cocktail.db"

engine = create_engine(
    DATABASE_URL,
    echo=False
)

NUMERIC_COLUMNS = [
    "total_cost",
    "cost_after_spillage",
    "selling_price_before_vat",
    "selling_price_after_vat",
]

@st.cache_data(ttl=5)
def load_data():

    query = text("""
        SELECT *
        FROM cocktails
    """)

    df = pd.read_sql(query, engine)

    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    if "cocktail_name" in df.columns:
        df["cocktail_name"] = (
            df["cocktail_name"]
            .fillna("Unknown")
        )

    return df

def show():
    st.title("Welcome to the milk bar")
    st.subheader("📊 Cocktail Dashboard")
    st.caption("Overview of cocktail costs, selling prices, and profitability.")

    df = load_data()

    if df.empty:
        st.error("No data available.")
        st.stop()

    # Derived metrics
    if (
        "selling_price_after_vat" in df.columns
        and "cost_after_spillage" in df.columns
    ):
        df["profit"] = (
            df["selling_price_after_vat"]
            - df["cost_after_spillage"]
        )

        df["gp_percent"] = (
            (df["profit"] / df["selling_price_after_vat"])
            .replace([float("inf"), float("-inf")], pd.NA)
            * 100
        )

    # Sidebar
    st.sidebar.header("Filters")

    selected_cocktails = st.sidebar.multiselect(
        "Cocktail names",
        options=sorted(df["cocktail_name"].dropna().unique()),
        default=sorted(df["cocktail_name"].dropna().unique()),
        key="dashboard_filter",
    )


    if selected_cocktails:
        filtered_df = df[df["cocktail_name"].isin(selected_cocktails)].copy()
    else:
        filtered_df = df.copy()

# Key metrics
    total_cocktails = len(df)
    avg_gp = df["gp_percent"].mean() if "gp_percent" in df.columns else pd.NA
    avg_price = df["selling_price_after_vat"].mean() if "selling_price_after_vat" in df.columns else pd.NA
    if (
    "profit" in df.columns
    and not df["profit"].dropna().empty
):
     best_cocktail = df.loc[
        df["profit"].idxmax(),
        "cocktail_name"
     ]
    else:
     best_cocktail = "N/A"

    if "profit" in df.columns:
      top_profit = (
        df.dropna(subset=["profit"])
        .sort_values(
            "profit",
            ascending=False,
        )
        .head(10)
      )
    else:
        top_profit = pd.DataFrame()

    avg_cost = filtered_df["total_cost"].mean() if "total_cost" in filtered_df.columns else pd.NA
    avg_sell = (
        filtered_df["selling_price_after_vat"].mean()
        if "selling_price_after_vat" in filtered_df.columns
        else pd.NA
    )
    avg_margin = (
        filtered_df["gp_percent"].mean()
        if "gp_percent" in filtered_df.columns
        else pd.NA
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Cocktails",
        total_cocktails,
    )

    col2.metric(
        "Average GP %",
        f"{avg_gp:.1f}%",
    )

    col3.metric(
        "Average Price",
        f"KES {avg_price:.0f}",
    )

    col4.metric(
        "Top Profit Cocktail",
        best_cocktail,
    )

    st.caption(
        f"Showing {len(filtered_df)} cocktails • Avg. Cost: {'KES ' + f'{avg_cost:,.2f}' if pd.notna(avg_cost) else 'N/A'} • Avg. Selling Price: {'KES ' + f'{avg_sell:,.2f}' if pd.notna(avg_sell) else 'N/A'}"
    )

# Visualizations
    col1, col2 = st.columns(2)
    chart_df = filtered_df.dropna(
    subset=[
        "total_cost",
        "selling_price_after_vat",
        "profit",
        "gp_percent",
    ]
)

    
    scatter_fig = px.scatter(
        chart_df,
        x="total_cost",
        y="selling_price_after_vat",
        size=chart_df["profit"].clip(lower=1),
        color="gp_percent",
        hover_name="cocktail_name",
        labels={
            "total_cost": "Total Cost",
            "selling_price_after_vat": "Selling Price After VAT",
            "profit": "Profit",
            "gp_percent": "GP %",
        },
        title="Cost vs. Selling Price",
    )
    scatter_fig.update_layout(template="plotly_white")
    col1.plotly_chart(scatter_fig, use_container_width=True)
    if chart_df.empty:
        st.warning("No chart data available.")
        st.stop()

    fig1 = px.bar(
        top_profit,
        x="cocktail_name",
        y="profit",
        title="Top 10 Most Profitable Cocktails",
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
    )

    fig2 = px.bar(
        df.sort_values("gp_percent"),
        x="cocktail_name",
        y="gp_percent",
        title="Gross Profit % by Cocktail",
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
    )

    fig3 = px.scatter(
        chart_df,
        x="cost_after_spillage",
        y="selling_price_after_vat",
        hover_name="cocktail_name",
        title="Cost vs Selling Price",
   )

    st.plotly_chart(
        fig3,
        use_container_width=True,
    )

    hist_fig = px.histogram(
        filtered_df,
        x="gp_percent" if "gp_percent" in filtered_df.columns else "selling_price_after_vat",
        nbins=15,
        title="Distribution of GP %",
    )
    hist_fig.update_layout(template="plotly_white")
    st.plotly_chart(hist_fig, use_container_width=True)

    st.subheader("Cocktail Details")
    st.dataframe(
        filtered_df[
            [
                col
                for col in [
                    "cocktail_name",
                    "total_cost",
                    "cost_after_spillage",
                    "selling_price_before_vat",
                    "selling_price_after_vat",
                    "profit",
                    "gp_percent",
                ]
                if col in filtered_df.columns
            ]
        ].sort_values(
            by="profit" if "profit" in filtered_df.columns else "selling_price_after_vat",
            ascending=False,
        ),
        use_container_width=True,
    )




