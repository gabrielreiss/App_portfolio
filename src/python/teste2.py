import os
import json
#import streamlit as st
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import yfinance as yf
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import pyfolio as pf
import warnings
import sqlalchemy
warnings.filterwarnings('ignore')

BASE_DIR = '.'
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATA_DIR = os.path.join(BASE_DIR,'data')
SQL_DIR = os.path.join(BASE_DIR, 'src', 'sql')

str_conn_itr = 'sqlite:///' + os.path.join(DATA_DIR, 'cvm_itr.db')
engine_itr = sqlalchemy.create_engine(str_conn_itr)
conn_itr = engine_itr.connect()

with open(os.path.join(SQL_DIR, 'select_pl.sql'), encoding='utf-8') as file:
    query = file.read()

lista = ['PETR3']
query.format(lista)



pl_temp = pd.read_sql_query(query.format(lista[0].split('.')[0]), conn_itr)
pl_temp['DT_FIM_EXERC'] = pd.to_datetime(pl_temp['DT_FIM_EXERC'])



pl_temp = pl_temp.drop_duplicates(subset='DT_FIM_EXERC')
print(pl_temp.dtypes)
pl_temp2 = pd.DataFrame(pl_temp['PL'])
pl_temp2 = pl_temp2.set_index(pl_temp['DT_FIM_EXERC'])

sns.lineplot(data=pl_temp2, y='PL', x=pl_temp2.index)
plt.show()