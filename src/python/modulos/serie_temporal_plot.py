import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import streamlit as st
import os

def serie_temporal_plot(indicador,
                        doc,
                        dfs,
                        conn_itr,
                        SQL_DIR,
                        options_tickers,
                        titulo,
                        *kargs):
#### 
# indicador = ['pl, 'liq_corrente','margem_bruta', 'roe]
# doc = ['itr', 'dfp']
# dfs = ['con', 'ind']

    sns.set()
    with open(os.path.join(SQL_DIR, f'select_{indicador}.sql'), encoding='utf-8') as file:
        query = file.read()
    pl_temp = pd.read_sql_query(query.format(
        cod=options_tickers[0].split('.')[0],
        doc=doc,
        dfs=dfs
        ), conn_itr)
    #st.dataframe(pl_temp)

    pl_temp['DT_FIM_EXERC'] = pd.to_datetime(pl_temp['DT_FIM_EXERC'])
    pl_temp = pl_temp.drop_duplicates(subset='DT_FIM_EXERC')

    pl_temp2 = pd.DataFrame(pl_temp['VL_CONTA'])
    pl_temp2 = pl_temp2.set_index(pl_temp['DT_FIM_EXERC'])
    #st.dataframe(pl_temp2)

    plt.figure(figsize=(12,5))
    ax = sns.lineplot(data=pl_temp2, y='VL_CONTA', x=pl_temp2.index, palette="tab10", linewidth=2.5)
    ax.set(xlabel='Ano', ylabel=titulo)
    plt.title(f'Evolução do {titulo}')

    if indicador == 'roe':
        ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:.4f}'))
    elif indicador == 'pl':
        ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))        
    else:
        ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.2f}'))

    st.pyplot()