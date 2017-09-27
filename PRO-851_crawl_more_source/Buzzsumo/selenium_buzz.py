# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 12:59:24 2017

@author: sentifi
"""

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

driver = webdriver.Chrome()
driver.get('http://app.buzzsumo.com/login')

email = driver.find_element_by_name('email')
email.send_keys('pdphong312@gmail.com')
password = driver.find_element_by_name('password')
password.send_keys('connguoi')

signin = driver.find_element_by_id('sign-in')
signin.click()

#influencer_tab = driver.find_element_by_xpath("//a[@href='https://app.buzzsumo.com/#/amplification/twitter-influencers']")
#influencer_tab.click()

#%% support function
def write_result(file_object, ticker, influencers):
    file_object.write('"' + ticker + '","' + str(influencers) + '"\n')

def get_influencers(driver, influencers):
    new_influencers = driver.find_elements_by_class_name("influencer-username")
    new_influencers = list(map(lambda x: x.text, new_influencers))
    influencers.extend(new_influencers)
    return influencers

def wait_loading(driver):
    loading = driver.find_element_by_class_name("loader-container")
    wait_count = 8
    while loading.is_displayed():
        time.sleep(0.5)
        wait_count -= 1
        if wait_count == 0:
            return 0
    return 1

#%% loop
try:
    file_object  = open("result_news.csv", "a")
    for ticker in tickers_list[2287:]:
        print(ticker)
        print(tickers_list.index(ticker))

        query_input = driver.find_element_by_name("q")
        query_input.clear()
        query_input.send_keys(ticker)
        
        search_button = driver.find_element_by_id("search-btn")
        search_button.click()
        
        pages = []
        
        if wait_loading(driver):
            news = driver.find_elements_by_class_name("search-link")
            news = list(map(lambda x: x.text, news))    
            print(news)
            #pages = driver.find_elements_by_xpath("//a[@ng-click='selectPage(page.number, $event)']")
        #pages_len = len(pages)
        #if pages_len > 1:
        #    for i in range(1, pages_len - 1, 1):
        #        time.sleep(randint(10,15))
        #        pages[i].click()
        #        if wait_loading(driver):
        #            pages = driver.find_elements_by_xpath("//a[@ng-click='selectPage(page.number, $event)']")
        #            influencers = get_influencers(driver, influencers)
        #            print(influencers)
        write_result(file_object, ticker, news)
        time.sleep(randint(20,25))
except:
    file_object.close()
    raise

#%%
driver
