import urllib.request
import pandas as pd
import os
import zipfile
import sqlalchemy

BASE_DIR = '.'
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
DATA_DIR = os.path.join(BASE_DIR,'data')
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'Downloads')

str_conn_itr = 'sqlite:///' + os.path.join(DATA_DIR, 'cvm_itr.db')
engine_itr = sqlalchemy.create_engine(str_conn_itr)
conn_itr = engine_itr.connect()

str_conn_cvm = 'sqlite:///' + os.path.join(DATA_DIR, 'cvm.db')
engine_cvm = sqlalchemy.create_engine(str_conn_cvm)
conn_cvm = engine_cvm.connect()

url = 'http://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv'

temp = pd.read_csv(url,
                    sep=';', encoding='latin1')

temp.to_sql('cad_cia_aberta', conn_itr, if_exists = 'replace')
temp.to_sql('cad_cia_aberta', conn_cvm, if_exists = 'replace')




