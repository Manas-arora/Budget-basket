import streamlit as st

def render_sidebar():
    st.sidebar.image("https://img.icons8.com/plasticine/100/ingredients.png", width=80)
    st.sidebar.title("Budget Basket")
    st.sidebar.markdown("🛝 **Track and Compare Grocery Prices**\n\nSave more, shop smarter!")

def render_header():
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🛒 Budget Basket</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>Real-time Grocery Price Comparison</h4>", unsafe_allow_html=True)
    st.markdown("---")
