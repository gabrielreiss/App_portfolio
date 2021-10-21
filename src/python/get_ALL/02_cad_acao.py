import urllib.request
import pandas as pd
import os
import zipfile
import sqlalchemy

BASE_DIR = '.'
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
DATA_DIR = os.path.join(BASE_DIR,'data')
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'Downloads')

str_conn = 'sqlite:///' + os.path.join(DATA_DIR, 'info_contabil.db')
engine = sqlalchemy.create_engine(str_conn)
conn = engine.connect()

#cad cnpj ação
url = os.path.join(DATA_DIR, 'cad_cnpj_acao.csv')
temp = pd.read_csv(url,sep=';', encoding='latin1')
temp2 = pd.concat([pd.Series(row['CNPJ'], row['Código'].split(','))
                   for _, row in temp.iterrows()]).reset_index()
temp2.columns = ['Código','CNPJ']
temp3 = pd.merge(temp2, temp, how='left', on ='CNPJ')
temp3['Código_x'] = temp3['Código_x'].str.strip()
temp3.to_sql('cad_cod', conn, if_exists = 'replace', index=False)