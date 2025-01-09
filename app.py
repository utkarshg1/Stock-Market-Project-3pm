import streamlit as st
from utils import StockAPI

# Set the header title
st.set_page_config(page_title= "Stock Market App", layout="wide")

# Intialize the stock api class
@st.cache_resource
def get_stock_api():
    return StockAPI()

client = get_stock_api()

# Search stocks function
@st.cache_data(ttl=3600)
def search_company(company):
    return client.search_symbol(company)

# Plot the chart
@st.cache_data(ttl=3600)
def plot_chart(symbol):
    df = client.get_stock_data(symbol)
    fig = client.plot_candlestick(df)
    return fig

# Add the title of app in body
st.title("Stock Market App")

# Add a subheader showing author name
st.subheader("by Utkarsh Gaikwad")

# Take company name as input from user
company = st.text_input("Company Name : ")

# After typing company name show the respectivs symbols
if company:
    search = search_company(company)
    
    if search:
        options = st.selectbox("Select Company Symbol : ", list(search.keys()))
        selected_data = search.get(options)
        st.success(f"Name : {selected_data[0]}")
        st.success(f"Type : {selected_data[1]}")
        st.success(f"Region : {selected_data[2]}")

        button = st.button("Plot", type="primary")

        if button:
            fig = plot_chart(options)
            st.plotly_chart(fig)

    else:
        st.error("Company Name not found")