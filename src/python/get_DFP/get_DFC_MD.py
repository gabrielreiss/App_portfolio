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
    url = 'http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/dfc_md/DADOS/dfc_md_cia_aberta_{}.zip'.format(ano)
    filename = 'dfc_md_cia_aberta_{}.zip'.format(ano)

    urllib.request.urlretrieve(url, os.path.join(DOWNLOAD_DIR, filename))

    with zipfile.ZipFile(os.path.join(DOWNLOAD_DIR, filename), 'r') as zip_ref:
            zip_ref.extractall(DOWNLOAD_DIR)

    os.remove(os.path.join(DOWNLOAD_DIR, filename))

    dfc_md_con = pd.read_csv(os.path.join(DOWNLOAD_DIR, 'dfc_md_cia_aberta_con_{}.csv'.format(ano)),
                        sep=';', encoding='latin1')
    dfc_md_con.to_sql('dfc_md_con', conn, if_exists = 'append')
    del dfc_md_con
    os.remove(os.path.join(DOWNLOAD_DIR, 'dfc_md_cia_aberta_con_{}.csv'.format(ano)))

    dfc_md_ind = pd.read_csv(os.path.join(DOWNLOAD_DIR, 'dfc_md_cia_aberta_ind_{}.csv'.format(ano)),
                        sep=';', encoding='latin1')
    dfc_md_ind.to_sql('dfc_md_ind', conn, if_exists = 'append')
    del dfc_md_ind
    os.remove(os.path.join(DOWNLOAD_DIR, 'dfc_md_cia_aberta_ind_{}.csv'.format(ano)))

    print(ano)