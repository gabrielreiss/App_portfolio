import os
import streamlit as st
import pandas as pd
import numpy as np
import json
import pandas_datareader.data as web
import yfinance as yf
yf.pdr_override()

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATA_DIR = os.path.join(BASE_DIR,'data')

with open(os.path.join(DATA_DIR,'tickets.json'), 'rb') as file:
    list_of_tickers = json.loads(file.read())
    list_of_tickers = list_of_tickers['tickets']

if __name__ == "__main__":
    tickers = list_of_tickers[0:10]
    print(tickers)
    carteira = web.get_data_yahoo(tickers, period="5y")["Adj Close"]
    print(carteira.tail())