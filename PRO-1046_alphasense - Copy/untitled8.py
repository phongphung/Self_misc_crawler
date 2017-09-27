# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 16:22:07 2017

@author: sentifi
"""

from psycopg2 import connect
import pandas as pd
import numpy as np
import requests
import psycopg2 as db
b = pd.read_excel("check_da.xlsx")
a = pd.read_excel("Check_exist.xlsx")
a.fillna('', inplace=True)
a = a[a['sns_id']!='']
b
NE_DB = "dbname='rest_in_peace' user='dbo' host='10.0.0.137' password='sentifi'"

PROFILE_DB = "dbname='da0' user='dbw' host='da0.ssh.sentifi.com' password='sentifi.da0'"


a['sns_id'] = a['sns_id'].apply(lambda x: str(int(x)))

def connect_postgres(dbName):
    try:
        conn = db.connect(dbName)
        print("Initialised Connection")
        return conn
    except:
        raise
        
conn = connect_postgres(PROFILE_DB)
cur = conn.cursor()
cur.execute("set statement_timeout to 300000; select pg_sleep(2);")

query = """SELECT * from user_ml_classified_data where user_id in {}""".format(str(tuple(list(b['sns_id']))))
cur.execute(query)
temp = cur.fetchall()
temp = list(map(list, temp))
df = pd.DataFrame(temp)
conn.close()
for i in df.columns:
    df[i] = df[i].apply(lambda x: str(x))
df.to_clipboard()
