# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 13:40:06 2017

@author: sentifi
"""


import pandas as pd
from elasticsearch import Elasticsearch

RM_URL = "rm_search_staging"
es_host = 'es-int-client-1.senvpc'
es_port = 9200

def get_pub():
    try:
        query = { "size" : 0,
  "query": {
    "bool": {
      "must": [
        {"term": {
          "ne_mentions.id": {
            "value": "263"
          }
        }},
        {"range": {
          "score_content_0": {
            "from": 95
          }
        }}
      ]
    }
  },
  "aggs" : {
    "sns_id": {
      "terms": {
        "field" : "published_by.sns_id",
        "size" : 30000
      }
    }
  }
}

        es = Elasticsearch([{'host': es_host, 'port': es_port}]) 
        results = es.search(index = RM_URL, body=query, request_timeout=1000000)
        return results
    except:
        raise
        
a = get_pub()
a

test = pd.DataFrame(a.get('aggregations').get('sns_id').get('buckets'))
test
test['len'] = test['key'].apply(lambda x: len(x))
b = test[test['len'] < 24]
b.reset_index(drop=True, inplace=True)
b
del b['len']
del b['doc_count']
b

from psycopg2 import connect
import pandas as pd
import numpy as np
import requests
#import psycopg2
import psycopg2 as db

NE_DB = "dbname='rest_in_peace' user='dbo' host='10.0.0.137' password='sentifi'"

PROFILE_DB = "dbname='da0' user='dbw' host='da0.ssh.sentifi.com' password='sentifi.da0'"

def connect_postgres(dbName):
    try:
        conn = db.connect(dbName)
        print("Initialised Connection")
        return conn
    except:
        raise

def get_info(sns_id_list):
    try:
        conn = connect_postgres(NE_DB)
        cur = conn.cursor()
        query = """SELECT sns_id, display_name, screen_name, sns_tag, 
        payload ->> 'description' as description
        FROM "sns_account"
        WHERE sns_name = 'tw' and payload::text != 'null' 
        and payload is not null
        and sns_id in {}""".format(str(tuple(sns_id_list)))
        cur.execute(query)
        temp = cur.fetchall()
        temp = list(map(list, temp))
        df = pd.DataFrame(temp)
        conn.close()
        return df
    except:
        conn.close()
        raise
        
df_info = get_info(b['key'])

df_info

def get_cat(sns_id_list):
    try:
        conn = connect_postgres(NE_DB)
        cur = conn.cursor()
        query = """SELECT sns_id, category_id
        FROM "sns_category"
        WHERE sns_name = 'tw' and sns_id in {}""".format(str(tuple(sns_id_list)))
        cur.execute(query)
        temp = cur.fetchall()
        temp = list(map(list, temp))
        df = pd.DataFrame(temp)
        conn.close()
        return df
    except:
        conn.close()
        raise
        
df_cat = get_cat(b['key'])
final = pd.merge(left=df_info, right=df_cat, on=0, how='outer')
final

#cat_data = pd.read_clipboard()
cat_data
final.columns = ['sns_id', 'display_name', 'screen_name', 'sns_tag', \
                 'description', 'category_id']

final2 = pd.merge(left=final, right=cat_data, on='category_id', how='inner')
final2.to_excel('back_up1.xlsx', index=False)


PS_URL = 'ps_w20_y2017'
def get_sentifi_score(sns_id_list):
    try:
        query = { "size" : 50000,
  "fields": [
    "channel_meta.sns_id",
    "score.s_sentifi"
  ], 
  "query": {
    "bool": {
      "must": [
        {"terms": {
          "channel_meta.sns_id": sns_id_list
        }}
      ]
    }
  }
}

        es = Elasticsearch([{'host': es_host, 'port': es_port}]) 
        results = es.search(index = PS_URL, body=query, request_timeout=1000000)
        results = pd.DataFrame(results['hits']['hits'])
        df = pd.DataFrame(list(results.fields.values))

        for c in df.columns:
             df[c] = df[c].apply(lambda x: x[0] if x is not np.nan else np.nan)
        return df
    except:
        raise
        
type(final2['sns_id'][9])
temp_sentifi_score = get_sentifi_score(list(final2['sns_id']))
temp_sentifi_score.columns = ['sns_id', 'sentifi_score']
final3= final2.merge(temp_sentifi_score, on='sns_id')
final3 = final3[final3['sentifi_score'] > 80]
final3.to_excel('back_up_2.xlsx', index=False)

TS_URL = 'ts_w20_y2017'
def get_ts_263(sns_id_list):
    try:
        query = { "size": 10000, "fields": [
  "channel_meta.sns_id",
  "filters.topic.id",
  "filters.topic.s_score"
], 
  "query": {
    "bool": {
      "must": [
        {"terms": {
          "filters.topic.id": [
            "263"
          ]
        }},
        {
          "terms": {
            "channel_meta.sns_id": sns_id_list
          }
        }
      ]
    }
  }
}

        es = Elasticsearch([{'host': es_host, 'port': es_port}]) 
        results = es.search(index = TS_URL, body=query, \
                            request_timeout=1000000)
        results = pd.DataFrame(results['hits']['hits'])
        df = pd.DataFrame(list(results.fields.values))

        for c in df.columns:
             df[c] = df[c].apply(lambda x: x[0] if x is not np.nan else np.nan)
        return df
    except:
        raise
        
ts_score = get_ts_263(list(final3['sns_id']))
ts_score.columns = ['sns_id', 'topic_id', 'ts_score']
final4 = final3.merge(ts_score, on='sns_id')
finalfinal = final4[final4['ts_score']>75]
finalfinal.to_excel('check.xlsx', index=False)
