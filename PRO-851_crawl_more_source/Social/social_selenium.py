# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 14:49:59 2017

@author: sentifi
"""

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import pandas as pd
import time
from random import randint

#%% Init, preparation
tickers = pd.read_excel('topic.xlsx')
tickers.fillna('', inplace=True)
tickers['Ticker'] = tickers.apply(lambda x: x['short_name'] if x['short_name']!='' else x['legal_name'], axis=1)
tickers
tickers_list = list(tickers['Ticker'])

#%%
from pymongo import MongoClient
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'PRO851'
MONGO_COLLECTION = 'social2'
def mongo_connection(host, port, db, collection):
    try:
        conn = MongoClient(host, port)
        return conn[db][collection]
    except:
        raise

def mongo_logging(connection, content):
    try:
        connection.insert_one(content)
    except:
        raise

conn = mongo_connection(MONGO_HOST,MONGO_PORT,MONGO_DB,MONGO_COLLECTION )

#%%
tickers_list[473]
#%%
count = 0

#%%

for i in tickers_list[6117:]:
    print(i)
    print(tickers_list.index(i))
    if i=='':
        continue
    count += 1
    if count==1:
        #chromeOptions = Options()
        #chromeOptions.add_argument("--kiosk")
        #driver = webdriver.Chrome(chrome_options=chromeOptions)
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get('https://app.socialanimal.io/login')
        email_field = driver.find_element_by_id('email')
        email_field.send_keys('pdphong312@gmail.com')
        password_field = driver.find_element_by_id('password')
        password_field.send_keys('connguoi')
        login = driver.find_element_by_id('log_me_in')
        login.click()
        time.sleep(4)
        collapse_mashboard = driver.find_element_by_id('collapse_mashboard')
        collapse_mashboard.click()
    domain_list = []
    #influencers_list = []
    time.sleep(4)
    search_field = driver.find_element_by_id('research-input-text')
    search_field.clear()
    search_field.send_keys(i)
    
    
    #Search button sometimes throw back error as non clickable, maybe the page not rendered probably
    time.sleep(randint(7,8))
    driver.execute_script("window.scrollTo(0, 0)")
    try:
        search = driver.find_element_by_id('research-input-btn')
        search.click()
    except:
        time.sleep(4)
        search = driver.find_element_by_id('research-input-btn')
        search.click()
    
    #Wait loading, check if total pages exists, if not, next ticker
    time.sleep(randint(3,9))
    try:
        if driver.current_url[-1] == '#':
            replace = 1
        else:
            replace = driver.current_url[-1]
        total_pages = int(driver.find_element_by_id('page-hilights').text.replace('Page {} of '.format(replace), ''))
    except NoSuchElementException:
        continue
    except ValueError:
        total_pages = int(driver.find_element_by_id('page-hilights').text.replace('Page {} of '.format(driver.find_element_by_id('page-hilights').text[-1]), ''))
        
    if total_pages > 10: total_pages = 10
    #In case total page exists, wrap contents
    for j in range(total_pages - 1 if total_pages > 1 else 1):
        try:
            #Just sleep to load, check loading
            time.sleep(randint(4,6))
            loading = driver.find_elements_by_id('content-search-loader')
            if len(loading) > 0:
                continue
                
            domain = driver.find_elements_by_xpath('//span[starts-with(@class, "search-result-domain")]')
            domain_list.extend(map(lambda x: x.text, domain))
            try:
                driver.find_element_by_xpath('//a[@href="#page-'+ str(j + 2) +'"]').click()
            except NoSuchElementException:
                continue #check page 2
                
            loading = driver.find_elements_by_id('content-search-loader')
            if len(loading) > 0:
                time.sleep(randint(7,8))
        except NoSuchElementException:
            raise #expect this wont happen
    domain_list = list(set(domain_list))
    time.sleep(randint(4,6))
    mongo_logging(conn, {"Ticker" : i, "News": domain_list})
    if count==400:
        driver.close
        count = 0
        
