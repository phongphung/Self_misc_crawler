# _*_ coding: utf-8 _*_

import scrapy
import pandas as pd

def convert(url):
    if not url.startswith('http://'):
        return 'http://' + url
    return url


class EZSpider(scrapy.Spider):
    name = "crawl_avatar"
    #result = pd.DataFrame(columns=['terms','keyword']
    
    a = pd.read_csv('checked_ping_final.csv')
    a.reset_index(drop=True, inplace=True)
    a = a[a['final']=='1']
    a = a.loc[:, ['payload_url', 'final_payload_url']]
    a = a.iloc[21000:]
    urls = list(map(convert, list(a['final_payload_url'])))
    
    def start_requests(self):
        
        for url in self.urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        twitter = self.get_twitter(response)
        temp = self.get_logo(response)
        with open('results3.csv', 'a') as f:
            f.write('"' + str(response.url) + '","' + str(temp) + '","' + str(twitter) + '"\n')
    	

    def get_logo(self, response):
        
        # case1
        temp = response.xpath("//*[contains(@id, 'logo')]")\
                .xpath(".//img")\
                .xpath("@src").extract()
        if len(temp) > 0:
            #print('case1')
            #print(temp)
            return temp
        
        # case2
        temp = response.xpath("//a[substring(@href, string-length(@href) - string-length('/home') +1) = '/home']")\
                .xpath(".//img")\
                .xpath("@src").extract()
        if len(temp) > 0:
            #print('case2')
            #print(temp)
            return temp
        
        # case2
        temp = response.xpath("//a[substring(@href, string-length(@href) - string-length('/home/') +1) = '/home/']")\
                .xpath(".//img")\
                .xpath("@src").extract()
        if len(temp) > 0:
            #print('case2')
            #print(temp)
            return temp
        
        # case3
        temp = response.xpath("//a[substring(@href, string-length(@href) - string-length('/index') +1) = '/index']")\
                .xpath(".//img")\
                .xpath("@src").extract()
        if len(temp) > 0:
            #print('case3')
            #print(temp)
            return temp
        
        # case3
        temp = response.xpath("//a[substring(@href, string-length(@href) - string-length('/index/') +1) = '/index/']")\
                .xpath(".//img")\
                .xpath("@src").extract()
        if len(temp) > 0:
            #print('case3')
            #print(temp)
            return temp
        
        # case3
        temp = response.xpath("//a[substring(@href, string-length(@href) - string-length('/index.html') +1) = '/index.html']")\
                .xpath(".//img")\
                .xpath("@src").extract()
        if len(temp) > 0:
            #print('case3')
            #print(temp)
            return temp
        
        # case3
        temp = response.xpath("//a[substring(@href, string-length(@href) - string-length('/index.html/') +1) = '/index.html/']")\
                .xpath(".//img")\
                .xpath("@src").extract()
        if len(temp) > 0:
            #print('case3')
            #print(temp)
            return temp
        
        # case3
        temp = response.xpath("//a[substring(@href, string-length(@href) - string-length('/index.php') +1) = '/index.php']")\
                .xpath(".//img")\
                .xpath("@src").extract()
        if len(temp) > 0:
            #print('case3')
            #print(temp)
            return temp
        
        # case3
        temp = response.xpath("//a[substring(@href, string-length(@href) - string-length('/index.php/') +1) = '/index.php/']")\
                .xpath(".//img")\
                .xpath("@src").extract()
        if len(temp) > 0:
            #print('case3')
            #print(temp)
            return temp
        
        # case4
        temp = response.xpath("//a[@href = '/']")\
                .xpath(".//img")\
                .xpath("@src").extract()
        if len(temp) > 0:
            #print('case4')
            #print(temp)
            return temp
        
        # case5
        temp = response.xpath("//a[@href = '{}']".format(response.url))\
                .xpath(".//img")\
                .xpath("@src").extract()
        if len(temp) > 0:
            #print('case5')
            #print(temp)
            return temp
        
        # case5
        temp = response.xpath("//a[@href = '{}']".format(response.url[:-1]))\
                .xpath(".//img")\
                .xpath("@src").extract()
        if len(temp) > 0:
            #print('case5')
            #print(temp)
            return temp
        
        # case5
        temp = response.xpath("//a[@href = '{}']".format(response.url + "/"))\
                .xpath(".//img")\
                .xpath("@src").extract()
        if len(temp) > 0:
            #print('case5')
            #print(temp)
            return temp
        
        print("Image")
        return 'IMAGE'
    
    def get_twitter(self, response):
        twitter = response.xpath("//*[contains(@href,'twitter.com')]")\
                .xpath("@href").extract()
        return twitter