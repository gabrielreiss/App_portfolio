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

#cad_cia_aberta
url = 'http://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv'
temp = pd.read_csv(url,sep=';', encoding='latin1')
temp.to_sql('cad_cia_aberta', conn, if_exists = 'replace')
