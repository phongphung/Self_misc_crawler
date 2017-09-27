# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 09:35:22 2017

@author: sentifi
"""

from twython import Twython
import pandas as pd

a = pd.read_excel('username.xlsx')

final = pd.DataFrame()

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

token = list(_key_pair.iloc[0, :])

twitter = Twython(*token)

results = pd.DataFrame()
for i in range(0, len(a), 100):
    print(i)
    screen_names = list(a.iloc[i:(i+100), 0])
    comma_separated_string = ",".join(screen_names)
    output = twitter.lookup_user(screen_name=comma_separated_string)
    results = pd.concat([results, pd.DataFrame(output)], ignore_index=True)
    
final
