import urllib.request
import pandas as pd
import os
import zipfile
import sqlalchemy

BASE_DIR = '.'
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
DATA_DIR = os.path.join(BASE_DIR,'data')
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'Downloads')

str_conn = 'sqlite:///' + os.path.join(DATA_DIR, 'cvm_itr.db')
engine = sqlalchemy.create_engine(str_conn)
conn = engine.connect()

#dfp
#doc = ['bpa', 'bpp', 'dre', 'dva', 'dfc_md', 'dfc_mi', 'dmpl']
doc = ['dva', 'dfc_md', 'dfc_mi', 'dmpl']
#doc = ['dfc_mi']
for docname in doc:
    for ano in list(range(2010,2020)):
        
        url = f'http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/{docname}/DADOS/{docname}_cia_aberta_{ano}.zip'
        filename = f'{docname}_cia_aberta_{ano}.zip'

        urllib.request.urlretrieve(url, os.path.join(DOWNLOAD_DIR, filename))

        with zipfile.ZipFile(os.path.join(DOWNLOAD_DIR, filename), 'r') as zip_ref:
                zip_ref.extractall(DOWNLOAD_DIR)

        os.remove(os.path.join(DOWNLOAD_DIR, filename))

        tipo = ['con', 'ind']

        for t in tipo:
            print(docname,ano,t)
            temp = pd.read_csv(os.path.join(DOWNLOAD_DIR, f'{docname}_cia_aberta_{t}_{ano}.csv'),sep=';', encoding='latin1')
            temp.to_sql(f'dfp_{docname}_{t}', conn, if_exists = 'append')
            del temp
            os.remove(os.path.join(DOWNLOAD_DIR, f'{docname}_cia_aberta_{t}_{ano}.csv'))

