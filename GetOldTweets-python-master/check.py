# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 09:48:39 2017

@author: sentifi
"""

#%%
import pandas as pd
from elasticsearch import Elasticsearch
import numpy as np
import psycopg2 as db


#%%

a = pd.read_excel('results_german_election.xlsx')
#%%
PROFILE_DB = "dbname='rest_in_peace' user='usentifi' host='rip-master.sentifi.com' password='dbPG96@usentifi' \
            port=5432"
DA0 = "dbname='da0' user='usentifi' host='prod-da0.sentifi.com' password='dbPG96@usentifi' \
            port=5432"
def connect_postgres(db_name):
    try:
        conn = db.connect(db_name)
        print("Initialised Connection")
        return conn
    except:
        print ("I am unable to connect to the database")
        raise
#%%
%%time
conn = connect_postgres(PROFILE_DB)
cur = conn.cursor()

query = """ SELECT sns_id FROM sns_account WHERE sns_name = 'tw'AND sns_id in {}
""".format(str(tuple(list(final['id_str']))))
    
cur.execute(query)
temp = cur.fetchall()
temp = list(map(list, temp))
df = pd.DataFrame(temp, columns= ['sns_id'])
conn.close()

#%%
final
final2 = pd.merge(left=final, right=df, left_on='id_str', right_on='sns_id', how='left')
final2.fillna('', inplace=True)
final3 = final2[final2['sns_id']=='']
#%%
conn = connect_postgres(DA0)
cur = conn.cursor()

query = """ SELECT user_id FROM user_ml_classified_data WHERE user_id in {}
""".format(str(tuple(list(final3['id_str']))))
    
cur.execute(query)
temp = cur.fetchall()
temp = list(map(list, temp))
df = pd.DataFrame(temp, columns= ['user_id'])
conn.close()

#%%
for i in df.columns:
    df[i] = df[i].apply(str)
final4 = pd.merge(left=final3, right=df, left_on='id_str', right_on='user_id', how='left')
