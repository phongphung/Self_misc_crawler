# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 13:59:25 2017

@author: sentifi
"""

import httplib2
import yaml
import json
import logging
from datetime import datetime
from datetime import timedelta
from imp import reload
from pytz import timezone
import pandas as pd
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

def google_custom_search(query, api_key, cse_id, **kwargs):
    http = httplib2.Http()
    service = build('customsearch', 'v1', developerKey=api_key, http=http)
    try:
        res = service.cse().list(q=query, cx=cse_id, **kwargs).execute()
        return res, True
    except HttpError as e:
        #raise
        logging.info('HTTP Error')
        logging.info(e)
        if json.loads(e.content.decode())['error']['code'] == 403:
            logging.info('Key threshold reached')
            return None, False
        else:
            return None, True
    except Exception as e:
        #raise
        logging.info(e)
        return None, True


def my_search(query, google_keys):
    active_key = 0

    while True:
        api_key = google_keys[active_key]['api_key']
        cse_id = google_keys[active_key]['cse_id']
        google_keys[active_key]['status'] = 1
        logging.info('Crawling from {}'.format(query))
        search_results, key_valid = google_custom_search(query, api_key, cse_id)
        if not key_valid:
            active_key = rotate_keys(google_keys)
            logging.info('Key rotated: {}'.format(active_key))
            if active_key == None:
                reset_keys(google_keys)
                logging.info('No key to use. Exit')
                logging.info('Stuck at {}'.format(query))
                active_key = 0
                return None
        else:
            if search_results:
                try:
                    temp = pd.DataFrame(search_results.get('items'))
                    temp['query'] = query
                    return temp
                except Exception as e:
                    logging.info(e)
                    return None
    
def rotate_keys(google_keys):
    """
    Disble current key.
    Return next available key.
    """
    for key in google_keys:
        if key['status'] == 1:
            key['status'] = -1 
        
    for idx, key in enumerate(google_keys):
        if key['status'] == 0:
            key['status'] = 1 
            return idx
    return None


def reset_keys(google_keys):
    for key in google_keys:
        key['status'] = 0
        


logging.basicConfig(filename='PRO_1046.log', filemode='tw', \
                    level=logging.DEBUG)

g_key1 = dict(api_key='AIzaSyCusz2rAW_qTLTrwJ4TzRTa0wqdYmqrb6g',\
                     cse_id = '015458923067084818477:799qjartqou', status=0)

g_key2 = dict(api_key='AIzaSyDjkL7_DLqTe5OvyuaM2mmDe_wnqdwTWaU',\
                     cse_id = '000519485165825485187:ag0v58uffwa', status=0)

g_key3 = dict(api_key='AIzaSyDq0OXw1teZ4B2VGMbQcvhfzngV7UQL_sI',\
                     cse_id = '003546909602338648873:bqkeq9qrteu', status=0)

google_keys = [g_key1, g_key2, g_key3]
google_keys
active_key = 0

df = pd.read_excel('Alpha_sense.xlsx')
df.fillna('', inplace=True)
df['title'] = ''
df['description'] = ''
results = pd.DataFrame()

for i in df.index:
    query = df.loc[i, 'Name']
    print(query)
    temp = my_search(query, google_keys)
    results = pd.concat([results, temp])
    df.loc[i, 'URL'] = temp.loc[0, 'formattedUrl']
    df.loc[i, 'title'] = temp.loc[0, 'title']
    df.loc[i, 'description'] = temp.loc[0, 'snippet']

query = 'Barron’s*'
temp = my_search(query, google_keys)
temp
df.to_clipboard()

results.to_clipboard()
results

df2 = pd.read_excel('temp2.xlsx')
df2['URL_2'] = ''
df2['title_2'] = ''
df2['description_2'] = ''
results_2 = pd.DataFrame()
#%%
for i in df2.index[996:]:
    try:
        query = str(df2.loc[i, 'displayLink']) + ' twitter'
        print(query)
        temp = my_search(query, google_keys)
        results = pd.concat([results, temp])
        
        df2.loc[i, 'URL_2'] = temp.loc[0, 'formattedUrl']
        df2.loc[i, 'title_2'] = temp.loc[0, 'title']
        df2.loc[i, 'description_2'] = temp.loc[0, 'snippet']
    except:
        raise
#%%
df2[df2['URL_2']!='']
df2.fillna('', inplace=True)

#%%
results.to_csv('back_up1_all_11am_05_07_2017.csv')
#%%
results.to_excel('Alpha_sense_twitter.xlsx')
df2.to_excel('Alpha_sense_twitter_neat.xlsx')
