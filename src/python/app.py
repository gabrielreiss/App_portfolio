import os
import json
import streamlit as st
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import yfinance as yf
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import pyfolio as pf
import warnings
import sqlalchemy
warnings.filterwarnings('ignore')
from modulos.serie_temporal_plot import serie_temporal_plot

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATA_DIR = os.path.join(BASE_DIR,'data')
SQL_DIR = os.path.join(BASE_DIR, 'src', 'sql')

with open(os.path.join(DATA_DIR,'tickets.json'), 'rb') as file:
    list_of_tickers = json.loads(file.read())
    list_of_tickers = list_of_tickers['tickets']

str_conn_itr = 'sqlite:///' + os.path.join(DATA_DIR, 'cvm_itr.db')
engine_itr = sqlalchemy.create_engine(str_conn_itr)
conn_itr = engine_itr.connect()



if __name__ == "__main__":
    st.title('Análise de Portifólio para Investimentos')
    
    options_tickers = st.multiselect("Lista de tickers", list_of_tickers, default=['PETR3.SA'])
    #options_tickers
    
    #aplicativo ainda só funciona para 1 ação
    #options_tickers = options_tickers[0]

    st.header('Variacões ITR')
    serie_temporal_plot('pl','itr','con',conn_itr,SQL_DIR,options_tickers,"Patrimônio Líquido")
    serie_temporal_plot('liq_corrente','itr','con',conn_itr,SQL_DIR,options_tickers,"Liquidez Corrente")
    serie_temporal_plot('margem_bruta','itr','con',conn_itr,SQL_DIR,options_tickers,"Margem Bruta")
    serie_temporal_plot('roe','itr','con',conn_itr,SQL_DIR,options_tickers,"ROE")

    st.header('Variacões DFP')
    serie_temporal_plot('pl','dfp','con',conn_itr,SQL_DIR,options_tickers,"Patrimônio Líquido")
    serie_temporal_plot('liq_corrente','dfp','con',conn_itr,SQL_DIR,options_tickers,"Liquidez Corrente")
    serie_temporal_plot('margem_bruta','dfp','con',conn_itr,SQL_DIR,options_tickers,"Margem Bruta")
    serie_temporal_plot('roe','dfp','con',conn_itr,SQL_DIR,options_tickers,"ROE")






    start = datetime.datetime(2012,5,31)
    end = datetime.datetime.today()

    carteira = web.get_data_yahoo(options_tickers, start=start, end=end)["Adj Close"]
    carteira.dropna(inplace=True)

    ibov = web.get_data_yahoo("^BVSP", start=start, end=end)["Adj Close"]
    ibov.dropna(inplace=True)

    #st.dataframe(carteira.tail())

    ####
    sns.set()
    carteira.plot(figsize=(10,5))
    st.pyplot()

    ####
    #carteira_normalizada = (carteira / carteira.iloc[0]) * 1000
    #carteira_normalizada.dropna(inplace=True)

    #ibov_normalizado = (ibov / ibov.iloc[0]) * len(options_tickers) * 1000

    #carteira_normalizada["saldo"] = carteira_normalizada.sum(axis=1)

    #carteira_normalizada["saldo"].plot(figsize=(18,8), label="Minha Carteira")
    #ibov_normalizado.plot(label="IBOV")
    #plt.legend()
    #st.pyplot()

    ####
    #retorno_carteira = carteira.pct_change()
    #retorno_ibov = ibov.pct_change()
    #retorno_ibov = retorno_ibov.dropna()

    #retorno_acumulado = (1 + retorno_carteira).cumprod()
    #retorno_acumulado.iloc[0] = 1
    #retorno_acumulado["saldo"] = retorno_acumulado.sum(axis=1)
    #retorno_acumulado["retorno"] = retorno_acumulado["saldo"].pct_change()
    #retorno_acumulado = retorno_acumulado.dropna()

    #st.dataframe(retorno_acumulado["retorno"])
    #st.dataframe(retorno_ibov)
    #pf.create_full_tear_sheet(retorno_acumulado["retorno"], benchmark_rets=retorno_ibov)