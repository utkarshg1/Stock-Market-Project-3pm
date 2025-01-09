import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

class StockAPI:

    def __init__(self):
        self.url = "https://alpha-vantage.p.rapidapi.com/query"
        self.headers = {
            "x-rapidapi-key": st.secrets["API_KEY"],
            "x-rapidapi-host": "alpha-vantage.p.rapidapi.com",
        }

    def search_symbol(self, company_name):
        querystring = {
            "datatype": "json",
            "keywords": company_name,
            "function": "SYMBOL_SEARCH",
        }
        response = requests.get(self.url, headers=self.headers, params=querystring)
        data = response.json()["bestMatches"]
        search = {}
        for i in data:
            symbol = i["1. symbol"]
            search[symbol] = [i["2. name"], i["3. type"], i["4. region"]]
        return search

    def get_stock_data(self, symbol):
        querystring = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": "compact",
            "datatype": "json",
        }
        response = requests.get(self.url, headers=self.headers, params=querystring)
        data = response.json()["Time Series (Daily)"]
        df = pd.DataFrame(data).T
        df = df.astype(float).round(2)
        df.index = pd.to_datetime(df.index)
        df.index.name = "Date"
        return df

    def plot_candlestick(self, df):
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=df.index,
                    open=df["1. open"],
                    high=df["2. high"],
                    low=df["3. low"],
                    close=df["4. close"],
                )
            ]
        )
        fig.update_layout(width=1200, height=800)
        return fig
        