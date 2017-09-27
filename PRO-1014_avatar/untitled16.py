# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 09:05:43 2017

@author: sentifi
"""

a['type_logo'] = a['logo'].apply(lambda x: type(x))
temp = a[a['type_logo']!=str]
for i in a.columns:
    a[i] = a[i].apply(lambda x: str(x))
a.to_excel('temp.xlsx', encoding='utf-8')

a['logo'] = a['logo'].apply(lambda x: x if 'WinError' not in x else '')
a['logo'] = a['logo'].apply(lambda x: x if 'Alert Text' not in x else '')
writer = pd.ExcelWriter(r'temp.xlsx', engine='xlsxwriter',options={'strings_to_urls': False})
a.to_excel(writer)
writer.close()
