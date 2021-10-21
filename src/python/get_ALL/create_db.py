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

#cad cnpj ação
url = os.path.join(DATA_DIR, 'cad_cnpj_acao.csv')
temp = pd.read_csv(url,sep=';', encoding='latin1')
temp2 = pd.concat([pd.Series(row['CNPJ'], row['Código'].split(','))
                   for _, row in temp.iterrows()]).reset_index()
temp2.columns = ['Código','CNPJ']
temp3 = pd.merge(temp2, temp, how='left', on ='CNPJ')
temp3['Código_x'] = temp3['Código_x'].str.strip()
temp3.to_sql('cad_cod', conn, if_exists = 'replace', index=False)

#dfp
doc = ['bpa', 'bpp', 'dre', 'dva', 'dfc_md', 'dfc_mi', 'dmpl']
for docname in doc:
    for ano in list(range(2010,2021)):
        print(doc,ano)
        url = 'http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/dva/DADOS/{docname}_cia_aberta_{ano}.zip'.format(docname,ano)
        filename = '{docname}_cia_aberta_{ano}.zip'.format(docname,ano)

        urllib.request.urlretrieve(url, os.path.join(DOWNLOAD_DIR, filename))

        with zipfile.ZipFile(os.path.join(DOWNLOAD_DIR, filename), 'r') as zip_ref:
                zip_ref.extractall(DOWNLOAD_DIR)

        os.remove(os.path.join(DOWNLOAD_DIR, filename))

        tipo = ['con', 'ind']

        for t in tipo:
            temp = pd.read_csv(os.path.join(DOWNLOAD_DIR, 'f{docname}_cia_aberta_{t}_{ano}.csv'),sep=';', encoding='latin1')
            temp.to_sql(f'dfp_{docname}', conn, if_exists = 'append')
            del temp
            os.remove(os.path.join(DOWNLOAD_DIR, f'{docname}_cia_aberta_{t}_{ano}.csv'))

#### itr
for ano in list(range(2010,2021)):
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
