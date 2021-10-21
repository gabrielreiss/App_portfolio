import urllib.request
import pandas as pd
import os
import zipfile
import sqlalchemy

BASE_DIR = '.'
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
DATA_DIR = os.path.join(BASE_DIR,'data')
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'Downloads')
SQL_DIR = os.path.join(BASE_DIR, 'src', 'sql')

str_conn = 'sqlite:///' + os.path.join(DATA_DIR, 'cvm_itr.db')
engine = sqlalchemy.create_engine(str_conn)
conn = engine.connect()

def executa_query(str_query,doc,dfs):
    with open(os.path.join(SQL_DIR, str_query), encoding='utf-8') as file:
        query = file.read()
    query = query.split(';')

    for i in range(0,len(query)):
        q2 = query[i].format(doc=doc,dfs=dfs)+';'
        conn.execute(q2)

#executa_query('create_pl.sql','dfp','con')
#executa_query('create_liq_corrente.sql')
#executa_query('create_margem_bruta.sql')
#executa_query('create_roe.sql')

for var in ['pl','liq_corrente','margem_bruta','roe','indicadores']:
    for doc in ['dfp','itr']:
        for dfs in ['con','ind']:
            print(var,doc,dfs)
            executa_query(f'create_{var}.sql',f'{doc}',f'{dfs}')