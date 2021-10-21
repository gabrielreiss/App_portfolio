import urllib.request
import pandas as pd
import os
import zipfile
import sqlalchemy

BASE_DIR = '.'
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))
DATA_DIR = os.path.join(BASE_DIR,'data')
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'Downloads')

str_conn_itr = 'sqlite:///' + os.path.join(DATA_DIR, 'cvm_itr.db')
engine_itr = sqlalchemy.create_engine(str_conn_itr)
conn_itr = engine_itr.connect()

str_conn_cvm = 'sqlite:///' + os.path.join(DATA_DIR, 'cvm.db')
engine_cvm = sqlalchemy.create_engine(str_conn_cvm)
conn_cvm = engine_cvm.connect()

url = os.path.join(DATA_DIR, 'cad_cnpj_acao.csv')

temp = pd.read_csv(url,
                    sep=';', encoding='latin1')

temp2 = pd.concat([pd.Series(row['CNPJ'], row['Código'].split(','))
                   for _, row in temp.iterrows()]).reset_index()

temp2.columns = ['Código','CNPJ']
temp3 = pd.merge(temp2, temp, how='left', on ='CNPJ')

temp3['Código_x'] = temp3['Código_x'].str.strip()

temp3.to_sql('cad_cod', conn_itr, if_exists = 'replace', index=False)
temp3.to_sql('cad_cod', conn_cvm, if_exists = 'replace', index=False)