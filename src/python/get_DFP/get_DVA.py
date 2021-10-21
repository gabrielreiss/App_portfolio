import urllib.request
import pandas as pd
import os
import zipfile
import sqlalchemy

BASE_DIR = '.'
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
DATA_DIR = os.path.join(BASE_DIR,'data')
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'Downloads')

str_conn = 'sqlite:///' + os.path.join(DATA_DIR, 'cvm.db')
engine = sqlalchemy.create_engine(str_conn)
conn = engine.connect()

for ano in list(range(2010,2021)):
    url = 'http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/dva/DADOS/dva_cia_aberta_{}.zip'.format(ano)
    filename = 'dva_cia_aberta_{}.zip'.format(ano)

    urllib.request.urlretrieve(url, os.path.join(DOWNLOAD_DIR, filename))

    with zipfile.ZipFile(os.path.join(DOWNLOAD_DIR, filename), 'r') as zip_ref:
            zip_ref.extractall(DOWNLOAD_DIR)

    os.remove(os.path.join(DOWNLOAD_DIR, filename))

    dva_con = pd.read_csv(os.path.join(DOWNLOAD_DIR, 'dva_cia_aberta_con_{}.csv'.format(ano)),
                        sep=';', encoding='latin1')
    dva_con.to_sql('dva_con', conn, if_exists = 'append')
    del dva_con
    os.remove(os.path.join(DOWNLOAD_DIR, 'dva_cia_aberta_con_{}.csv'.format(ano)))

    dva_ind = pd.read_csv(os.path.join(DOWNLOAD_DIR, 'dva_cia_aberta_ind_{}.csv'.format(ano)),
                        sep=';', encoding='latin1')
    dva_ind.to_sql('dva_ind', conn, if_exists = 'append')
    del dva_ind
    os.remove(os.path.join(DOWNLOAD_DIR, 'dva_cia_aberta_ind_{}.csv'.format(ano)))

    print(ano)