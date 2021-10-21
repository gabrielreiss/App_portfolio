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

#### itr
for ano in list(range(2011,2021)):
    url = 'http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/itr/DADOS/itr_cia_aberta_{}.zip'.format(ano)
    filename = 'itr_cia_aberta_{}.zip'.format(ano)

    urllib.request.urlretrieve(url, os.path.join(DOWNLOAD_DIR, filename))

    with zipfile.ZipFile(os.path.join(DOWNLOAD_DIR, filename), 'r') as zip_ref:
            zip_ref.extractall(DOWNLOAD_DIR)

    os.remove(os.path.join(DOWNLOAD_DIR, filename))

    #### arquivo geral
    arquivo = os.path.join(DOWNLOAD_DIR, 'itr_cia_aberta_{}.csv'.format(ano))
    temp = pd.read_csv(arquivo,
                        sep=';', encoding='latin1')
    temp.to_sql('itr_geral', conn, if_exists = 'append')
    del temp
    os.remove(arquivo)

    #### lista de demonstrativos ITR
    demonstrativos = ['BPA', 'BPP', 'DFC_MD', 'DFC_MI', 'DMPL', 'DRE', 'DVA']
    tipo = ['con', 'ind']

    for d in demonstrativos:
        for t in tipo:
            arquivo = os.path.join(DOWNLOAD_DIR, 'itr_cia_aberta_{}_{}_{}.csv'.format(d,t,ano))
            temp = pd.read_csv(arquivo,
                                sep=';', encoding='latin1')
            temp.to_sql('itr_{}'.format(d), conn, if_exists = 'append')
            del temp
            os.remove(arquivo)
            print("{}_{}_{}".format(d,t,ano))


