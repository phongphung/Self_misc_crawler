# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 11:06:46 2017

@author: sentifi
"""

#%%
import pandas as pd
from elasticsearch import Elasticsearch
import numpy as np
import pandas as pd
import psycopg2 as db
PS_URL = "ps_w16_y2017"
TS_URL = "ts_w52_y2016"
RM_URL = "rm_search_staging"
TEST_URL = "ps_w1_y2017_test_roundup"
RAW_URL = "raw_tokens_ngram"
es_host = 'qa-ext-es.sentifi.com'
es_port = 9200
#%%
PROFILE_DB = "dbname='da0' user='usentifi' host='prod-da0.sentifi.com' password='dbPG96@usentifi' \
            port=5432"
NE_DB = "dbname= 'rest_in_peace' user='usentifi' host='rip-master.sentifi.com' password='dbPG96@usentifi' \
            port=5432"
def connect_postgres():
    try:
        conn = db.connect(NE_DB)
        print("Initialised Connection")
        return conn
    except:
        print("I am unable to connect to the database")
#%%
%%time
conn = connect_postgres()
cur = conn.cursor()
result_df = pd.DataFrame()
i = 0
query = """
SELECT DISTINCT sns_name
FROM "sns_account"
LIMIT 50
"""
    
cur.execute(query)
temp = cur.fetchall()
conn.close()

#%%
temp


#%%
def check(ne):
    try:
        payload = {}
        es = Elasticsearch([{'host': es_host, 'port': es_port}]) 
        results = es.search(index = RM_URL, body=payload, request_timeout=60000)
        #results = pd.DataFrame(results['aggregations']['distinct_id']['value'])
        try:
            a = results['hits']['total']
            #df = pd.DataFrame(list(df.values))
            #df[2] = df[2].apply(lambda x: str(x))
            #df = df[df[2]==sns_id]
        except:
            raise
        return a      
        
    except:
        raise
        
