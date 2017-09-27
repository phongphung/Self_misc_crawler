# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 09:12:12 2017

@author: sentifi
"""
import sys
import glob
import pandas as pd


a = pd.read_csv('bundestagswahl%20OR%20bundestagswahlen2013-10-012013-11-01.csv', sep=';', error_bad_lines=False)

def to_int(x):
    try:
        return int(x)
    except:
        return ''
    
a['id2'] = a['id'].apply(to_int)

for i in a.columns:
    a[i] = a[i].apply(str)


results = pd.DataFrame()
for filename in glob.glob('./*.csv'):
    temp = pd.read_csv(filename, sep=';', error_bad_lines=False, encoding=sys.getfilesystemencoding())
    temp['id2'] = a['id'].apply(to_int)
    for i in temp.columns:
        temp[i] = temp[i].apply(str)
    results = pd.concat([results, temp])
    
for filename in glob.glob('*.csv'):
    print(filename)