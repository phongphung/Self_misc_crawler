# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 13:08:44 2017

@author: sentifi
"""

import pandas as pd
import urltools

a = pd.read_excel('AllForNow.xlsx')

a.fillna('', inplace=True)

a['test'] = a['text'].apply(lambda x: x.split(','))
a['test'] = a['test'].apply(lambda x: x[-1])
a
a['location'] = a.apply(lambda x: x['location'] if x['location']!='' else x['test'], axis=1)
a
a['url'] = a['url'].apply(lambda x: urltools.extract(x).url)
a['url'] = a['url'].apply(lambda x: urltools.split(x).netloc)
a

a.to_excel('AllForNow.xlsx')
