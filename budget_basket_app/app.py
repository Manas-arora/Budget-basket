import streamlit as st
import pandas as pd
from data_loader import load_data
from utils import compare_prices, get_price_change, get_price_trend
from ui_components import render_sidebar, render_header

# Set page configuration
st.set_page_config("🛒 Budget Basket", layout="centered")

# Render sidebar and header
render_sidebar()
render_header()

# Load data
data = load_data()
sample_store = list(data.values())[0]
product_list = sorted(sample_store["Product"].dropna().unique())

# Product search
st.markdown("### 🔎 Search for a Product")
product_search = st.text_input("Search:")
filtered_products = [p for p in product_list if product_search.lower() in p.lower()] if product_search else product_list
product = st.selectbox("Select product:", filtered_products)

# Date selection
st.markdown("### 🗓️ Choose a Date")
date_columns = [col for col in sample_store.columns if col != "Product"]
selected_date = st.selectbox("Date:", date_columns)

# Store selection
st.markdown("### 🏪 Choose Stores to Compare")
store_list = list(data.keys())
selected_stores = st.multiselect("Stores:", store_list, default=store_list)

# Price comparison logic
raw_prices = compare_prices(data, product, selected_date)
filtered_prices = {k: v for k, v in raw_prices.items() if k in selected_stores}
price_changes = get_price_change(data, product, selected_date)

# Display results
if filtered_prices:
    min_p, max_p = min(filtered_prices.values()), max(filtered_prices.values())
    price_range = st.slider("💸 Price range filter (₹):", 
                            min_value=int(min_p), 
                            max_value=int(max_p),
                            value=(int(min_p), int(max_p)))
    shown_prices = {s: p for s, p in filtered_prices.items() if price_range[0] <= p <= price_range[1]}

    if shown_prices:
        best_store = min(shown_prices, key=shown_prices.get)
        best_price = shown_prices[best_store]
        avg_price = sum(shown_prices.values()) / len(shown_prices)
        min_store, min_price = min(shown_prices.items(), key=lambda x: x[1])
        max_store, max_price = max(shown_prices.items(), key=lambda x: x[1])

        st.markdown("---")
        st.markdown(f"### 🥇 Best Price: ₹{best_price} at **{best_store}**")
        st.markdown(f"### 📊 Average Price: ₹{avg_price:.2f}")
        st.markdown(f"📉 Lowest: ₹{min_price} ({min_store}) | 📈 Highest: ₹{max_price} ({max_store})")

        df_summary = pd.DataFrame([
            {
                "Store": store,
                "Price": price,
                "Diff from Avg": price - avg_price,
                "Change from Prev Day": price_changes.get(store, float("nan"))
            }
            for store, price in shown_prices.items()
        ])

        st.markdown("### 📋 Price Comparison Table")
        st.dataframe(df_summary.style.format({
            "Price": "₹{:.2f}",
            "Diff from Avg": "₹{:+.2f}",
            "Change from Prev Day": "₹{:+.2f}"
        }))

        st.download_button("📥 Download CSV", df_summary.to_csv(index=False).encode(), f"{product}_prices.csv", "text/csv")
    else:
        st.warning("No prices found under the current filters.")
else:
    st.warning("No prices found for the selected product and date.")

# Final Trend Display
st.markdown("---")
st.markdown("### 📈 Price Trend Over Time")
trend_df = get_price_trend(data, product, selected_stores)

if not trend_df.empty:
    import plotly.express as px
    fig = px.line(trend_df, x="Date", y="Price", color="Store", markers=True, title=f"Price Trend: {product}")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📊 Price Distribution")
    dist_fig = px.box(trend_df, x="Store", y="Price", points="all")
    st.plotly_chart(dist_fig, use_container_width=True)

    pivot = trend_df.pivot(index="Date", columns="Store", values="Price").sort_index()
    pivot.index = pivot.index.strftime("%d %b")
    st.markdown("### 🧾 Historical Price Table")
    st.dataframe(pivot.style.format("₹{:.2f}").highlight_min(axis=1, color="lightgreen").highlight_max(axis=1, color="salmon"))
