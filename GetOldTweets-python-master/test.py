import tweepy
import json
import pandas as pd
import datetime
from time import sleep
import time
import multiprocessing as mp
from multiprocessing import Process

def getID(status):
    return status.id


def getURL(status):
    urls = status._json.get('entities').get('urls')
    if not urls:
        return pd.DataFrame()
    return pd.DataFrame(urls)


class TwitterAuth:
    _key_pair = pd.DataFrame([['PhhJjvWZz3o02vndrsIQzs1Hd', 'pDPG39dkgg0JLnmTOkUqTpTPefrjkBinIPJyNHNkQLtpAvpjCd',
                              '800985392719613952-iG8viwdDkI4we9qgkBqT68wHYULnFeN',
                              'mqc4SaOfVm78ofT1MqqI1t9I87s2GYA1dUy6wYRuQd3tC'],
                              ['nQ9BvzAtO2t2X8RfroqPcuJDW', 'gu710znDaKosWuqujSbSQZiEDVGJL1VFL7ZoPjDlCcuDBHu70j',
                              '828546867076096001-d4SNoJOVds8GPvBL563yxOyx9Nuwzqn',
                              'spm2dyXramxPAJGJD4eYFj9NZ8eVODhlvNfF0Y1dmUVYB'],
                              ['U09OTfiGzOSssG9wmSuUWuHUm', 'iVLalLEOohK0LYwIamGzuCi1PYL5QoX3FgTl7W6ODBYZqRLmn9',
                              '2802135358-WRddkHwAq2ohyeaEGpHkf48a3n2rmsaonpcbeiy',
                              'g8r7ARvxWfdBahnFjbRUrk2SZj43xWfZ02nqhOO10IzqR'],
                              ['pip7fVZeUPPCGq3V2OHxeEd9C', 'pqiWh519kC2S5gbmtOoAdZB5JZWi3whvql8UCmc9Ddq8k4qh7J',
                              '892458735519514624-l6N2H6Qz7AYRNDDFsV7mplRAz1QWMo4',
                              'TBFYBjgtbF27ODHYW3gBp4HseZOmopQ1pcJY7T8wKwjYt']],
                             columns=['consummer_key', 'consummer_secret', 'access_token', 'access_token_secret'])
    _key_pair['remaining'] = ''
    _key_pair['now'] = ''
    _key_pair['reset'] = ''
    _key_pair['count_down'] = ''
    _key_pair['status'] = 0

    def __init__(self):
        self._key = None
        self.Key = ['', '', '', '']
        self._wait = 0
        self.refresh_info()
        self._get_key()
        if self._key is None:
            print('No key available now, please wait' + str(self._wait) + 'secs')
        self.Api = None
        self._temp_get_auth()

    def test(self):
        self._key_pair['status'][3] = 99

    def refresh_info(self):
        for key_index in self._key_pair.index:
            consumer_key, consumer_secret, access_token, access_token_secret, *_ = list(self._key_pair.iloc[key_index, :])
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            _api = tweepy.API(auth)
            _limit = _api.rate_limit_status().get('resources').get('statuses').get(u'/statuses/lookup')
            self._key_pair.loc[key_index, ['remaining', 'now', 'reset']] = _limit.get('remaining'), int(time.time()), \
                                                                           int(_limit.get('reset'))
        self._key_pair['count_down'] = self._key_pair.apply(lambda x: int(x['reset']) - int(x['now']), axis=1)
        self._key_pair['status'] = self._key_pair.apply(lambda x: -1 if x['remaining'] == 0 else x['status'], axis=1)

    def _temp_get_auth(self):
        if self._key is None:
            self.Api = None
            return
        consumer_key, consumer_secret, access_token, access_token_secret, *_ = list(self._key_pair.iloc[self._key, :])
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.Api = tweepy.API(auth)
        return

    def _get_key(self):
        check = self._key_pair[self._key_pair['remaining'] > 0]
        if check.empty:
            next_reset = min(self._key_pair['reset'])
            self._key, self._wait = None, next_reset
            return

        check_0 = check[check['status'] >= 0]  # check status 0
        if not check_0.empty:
            self._key, self._wait = check_0[check_0['remaining'] == max(check_0['remaining'])].index[0], 0
            self._key_pair.loc[self._key, 'status'] += 1
            return


    def renew_key(self, old_key):
        self._key_pair.loc[old_key, 'status'] = 0
        self._get_key()
        self.update_key()
        self._temp_get_auth()
        if self._key is None:
            print('No key available now, please wait' + str(self._wait) + 'secs')

    def update_key(self):
        if self._key is None:
            self.Key = ['', '', '', '']
            return
        self.Key = list(self._key_pair.iloc[self._key, [0, 1, 2, 3]])


def get_url_from_tweet_id(_api, id_list):
    result = _api.statuses_lookup(id_list)
    result = list(map(lambda x: x._json.get('entities').get('urls'), result))
    return pd.DataFrame(result)

def write_url_from_tweet_id(file, _api, id_list):
    result = _api.statuses_lookup(id_list)
    result = list(map(lambda x: x._json.get('entities').get('urls'), result))
    file.write(str(file) + '\n')

def get_expanded_url(start):
    f = open(str(start)+'processed.csv', 'a') 
    #results_df = pd.DataFrame()
    api = TwitterAuth()
    for i in range(start, 101, 8):
        print('file: ' +str(i))
        final = pd.read_csv(str(i) + '.csv')
        data = final['ext_id']
        chunk_size = 100
        chunks = [data[x:x + chunk_size] for x in range(0, len(data), chunk_size)]
        count = 0
        for j in chunks:
            count+=1
            print(count)
            #temp = get_url_from_tweet_id(api.Api, list(j))
            #results_df = pd.concat([results_df, temp], ignore_index=True)
            write_url_from_tweet_id(f, api.Api, list(j))


if __name__ == '__main__':
    numbers = list(range(8))
    procs = []
    
    for index, number in enumerate(numbers):
        proc = Process(target=get_expanded_url, args=((65+number),))
        procs.append(proc)
        proc.start()
    
    for proc in procs:
        proc.join()