# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 09:29:18 2017

@author: sentifi
"""

import scrapy

class YelpLoginSpider(scrapy.Spider):
    name = 'buzzsumo'
    start_urls = ["https://app.buzzsumo.com/login?redirect_to=https%3A%2F%2Fapp.buzzsumo.com%2Fresearch%2Fmost-shared"]
    tickers = ["amd", "INTC", "AAPL"]
    download_delay = 10
    def parse(self, response):

        csrftok_value = str(response.xpath("//input[@name='_token']/@value").extract_first())
        csrftok_name = "_token"

        email_name = 'email'
        email = 'phphong312@gmail.com'

        password_name = 'password'
        password = 'connguoi'

        formxpath = '//form[starts-with(@class, "form-signin")]'
        formdata = {csrftok_name : csrftok_value, email_name : email, password_name : password}

        #call scrapy post request with after_login as callback
        return scrapy.FormRequest.from_response(
                response,
                formxpath=formxpath,
                formdata=formdata,
                callback=self.after_login
                )

    def after_login(self, response):
        try:
            login = response.xpath("//a[contains(text(), 'Login')]")
        except:
            login = False
        
        if not login:
            for ticker in self.tickers:
                for i in range(1, 6):
                    url = """https://app.buzzsumo.com/amplification/twitter-influencers?type=influencers& result_type=relevancy&blogger&influencer&company&journalist&regular_people&ignore_broadcasters=false&active_only&q={}&page={}""".format(ticker, i)
                    yield scrapy.Request(url=url, callback=self.parse_result)
        else:
            print("cant login")

    def parse_result(self, response):
        twitter_user = response.xpath("//span[starts-with(@class, 'influencer-username')]")
        twitter_user = list(map(lambda x: x.getText(), twitter_user))
        with open('test.csv', 'a') as f:
            f.write('"' + str(response.url) + '","' + str(twitter_user) + '"\n')