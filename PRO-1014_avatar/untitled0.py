# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import pandas as pd
from PIL import Image
import tldextract as tld


a = pd.read_csv('checked_ping_final.csv')
a.reset_index(drop=True, inplace=True)
a = a[a['final']=='1']
a = a.loc[:, ['payload_url', 'final_payload_url']]
#%%
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)

#%%

def get_logo(driver):

    try:
        logo = driver.find_elements_by_xpath("//*[contains(@id, 'logo')]")
        logo = logo[0].find_elements_by_xpath(".//img")
        if logo[0].get_attribute('src') != None:
            print('case1')
            return logo[0].get_attribute('src')
    except:
        pass
    
    try:
        logo = driver.find_elements_by_xpath("//a[@href = '/home']")
        logo = logo[0].find_elements_by_xpath(".//img")
        if logo[0].get_attribute('src') != None:
            print('case2')
            return logo[0].get_attribute('src')
    except:
        pass
    
    try:
        logo = driver.find_elements_by_xpath("//a[@href = '/home/']")
        logo = logo[0].find_elements_by_xpath(".//img")
        if logo[0].get_attribute('src') != None:
            print('case2')
            return logo[0].get_attribute('src')
    except:
        pass
    
    try:
        logo = driver.find_elements_by_xpath("//a[@href = '/index']")
        logo = logo[0].find_elements_by_xpath(".//img")
        if logo[0].get_attribute('src') != None:
            print('case3')
            return logo[0].get_attribute('src')
    except:
        pass
    
    try:
        logo = driver.find_elements_by_xpath("//a[@href = '/index/']")
        logo = logo[0].find_elements_by_xpath(".//img")
        if logo[0].get_attribute('src') != None:
            print('case3')
            return logo[0].get_attribute('src')
    except:
        pass
    
    try:
        logo = driver.find_elements_by_xpath("//a[@href = '/index.html']")
        logo = logo[0].find_elements_by_xpath(".//img")
        if logo[0].get_attribute('src') != None:
            print('case3')
            return logo[0].get_attribute('src')
    except:
        pass
    
    try:
        logo = driver.find_elements_by_xpath("//a[@href = '/index.php']")
        logo = logo[0].find_elements_by_xpath(".//img")
        if logo[0].get_attribute('src') != None:
            print('case3')
            return logo[0].get_attribute('src')
    except:
        pass
    
    try:
        logo = driver.find_elements_by_xpath("//a[@href = '/index.php/']")
        logo = logo[0].find_elements_by_xpath(".//img")
        if logo[0].get_attribute('src') != None:
            print('case3')
            return logo[0].get_attribute('src')
    except:
        pass
    
    try:
        logo = driver.find_elements_by_xpath("//a[@href = '/index.html/']")
        logo = logo[0].find_elements_by_xpath(".//img")
        if logo[0].get_attribute('src') != None:
            print('case3')
            return logo[0].get_attribute('src')
    except:
        pass
    
    try:
        logo = driver.find_elements_by_xpath("//a[@href = '/']")
        logo = logo[0].find_elements_by_xpath(".//img")
        if logo[0].get_attribute('src') != None:
            print('case5')
            return logo[0].get_attribute('src')
    except:
        pass
    
    try:
        logo = driver.find_elements_by_xpath("//a[substring(@href, string-length(@href) - string-length('/home') +1) = '/home']")
        logo = logo[0].find_elements_by_xpath(".//img")
        if logo[0].get_attribute('src') != None:
            print('case6')
            return logo[0].get_attribute('src')
    except:
        pass
    
    try:
        logo = driver.find_elements_by_xpath("//a[substring(@href, string-length(@href) - string-length('/home/') +1) = '/home/']")
        logo = logo[0].find_elements_by_xpath(".//img")
        if logo[0].get_attribute('src') != None:
            print('case6')
            return logo[0].get_attribute('src')
    except:
        pass
    
    try:
        logo = driver.find_elements_by_xpath("//a[substring(@href, string-length(@href) - string-length('/index/') +1) = '/index/']")
        logo = logo[0].find_elements_by_xpath(".//img")
        if logo[0].get_attribute('src') != None:
            print('case7')
            return logo[0].get_attribute('src')
    except:
        pass
    
        
    try:
        logo = driver.find_elements_by_xpath("//a[substring(@href, string-length(@href) - string-length('/index') +1) = '/index']")
        logo = logo[0].find_elements_by_xpath(".//img")
        if logo[0].get_attribute('src') != None:
            print('case7')
            return logo[0].get_attribute('src')
    except:
        pass
    
    try:
        logo = driver.find_elements_by_xpath("//a[@href = '{}']"\
                                                  .format(driver.current_url))
        logo = logo[0].find_elements_by_xpath(".//img")
        if logo[0].get_attribute('src') != None:
            print('case4.5')
            return logo[0].get_attribute('src')
    except:
        pass
    
    try:
        logo = driver.find_elements_by_xpath("//a[@href = '{}']"\
                                                  .format(driver.current_url[:-1]))
        logo = logo[0].find_elements_by_xpath(".//img")
        if logo[0].get_attribute('src') != None:
            print('case4.5')
            return logo[0].get_attribute('src')
    except:
        pass

    try:
        logo = driver.find_elements_by_xpath("//a[@href = '{}']"\
                                                  .format(driver.current_url + "/"))
        logo = logo[0].find_elements_by_xpath(".//img")
        if logo[0].get_attribute('src') != None:
            print('case4.5')
            return logo[0].get_attribute('src')
    except:
        pass
    
    #try:
    #    logo = driver.find_elements_by_xpath("//img[starts-with(@alt, 'logo')]")
    #    if logo[0].get_attribute('src') != None:
    #        print('case3')
    #        return logo[0].get_attribute('src')
    #except:
    #    pass
    
    #try:
    #    logo = driver.find_elements_by_xpath("//*[contains(@class, 'logo')]")
    #    logo = logo[0].find_elements_by_xpath(".//img")
    #    if logo[0].get_attribute('src') != None:
    #        print('case4')
    #        return logo[0].get_attribute('src')
    #except:
    #    pass
    
    #try:
    #    logo = driver.find_elements_by_xpath("//a[contains(@href,'{}')]"\
    #                                              .format(driver.current_url))
    #    logo = logo[0].find_elements_by_xpath(".//img")
    #    if logo[0].get_attribute('src') != None:
    #        print('case4.5')
    #        return logo[0].get_attribute('src')
    #except:
    #    pass
    

    
    
    #try:
    #    logo = driver.find_elements_by_xpath("//a[contains(@class, 'brand')]")
    #    if logo[0].get_attribute('src') != None:
    #        print('case8')
    #        return logo[0].get_attribute('src')
    #except:
    #    pass
    
    #try:
    #    logo = driver.find_elements_by_xpath("//a[contains(@class, 'logo')]")
    #    if logo[0].get_attribute('src') != None:
    #        print('case9')
    #        return logo[0].get_attribute('src')
    #except:
    #    pass
    
    #try:
    #    logo = driver.find_elements_by_xpath("//*[contains(., 'logo')]")
    #    logo = logo[0].find_elements_by_xpath(".//img")
    #    if logo[0].get_attribute('src') != None:
    #        print('case10')
    #        return logo[0].get_attribute('src')
    #except:
    #    pass
    
    #try:
    #    logo = driver.find_elements_by_xpath("//img[contains(@src, 'logo')]")
    #    if logo[0].get_attribute('src') != None:
    #        print('case2')
    #        return logo[0].get_attribute('src')
    #except:
    #    pass
    
    return 'IMAGE'
#%%
console 8 : 2000
console 9 : 25000
console 10 : 15000
console 11 : 34000
#%%
#a['logo'] = ''
for j in a[a['logo']==''].index[14047:15000]:
    try:
        i = a['final_payload_url'][j]
        print(i)
        driver.get(i) if 'http' in i else driver.get('http://' + i)
        logo = get_logo(driver)
        a.loc[j, 'logo'] = logo
        print(logo)
        print(a.loc[j, 'logo'])
    except Exception as e:
        a.loc[j, 'logo'] = str(e)
        continue
#%%
a[a['final_payload_url']=='http://www.subaru-net.com']
#%%
temp = a.iloc[a.index[14000:15000], :]
temp[temp['final_payload_url']=='http://www.subaru-net.com']
#%%
list(temp.index).index(15501)
#%%
a[(a['logo']!='') & (a['check']==False)]
a[a['logo']!='']
a['check'] = a['logo'].apply(lambda x: 'Alert Text' in x)
#%%
driver.get('http://sippindustries.com/')
get_logo(driver)
#a['logo'][38496]
driver.find_elements_by_xpath("//img")

#%%
logo = driver.find_elements_by_xpath('//a[@href = "{}"]'\
                                                  .format(driver.current_url))
logo = logo[0].find_elements_by_xpath(".//img")
logo
#%%
driver.current_url[:-1]
logo[0].find_elements_by_xpath(".//img")
#%%
a['type_logo'] = a['logo'].apply(lambda x: type(x))
a['logo'] = a['logo'].apply(lambda x: str(x))
a['logo'] = a['logo'].apply(lambda x: '' if 'Alert' in x else x)
a['logo'] = a['logo'].apply(lambda x: '' if 'timeout' in x else x)
a.fillna('', inplace=True)

a[a['logo']=='']
location = logo[0].location
size = logo[0].size

driver.save_screenshot("temp.png")
im = Image.open('temp.png')
left = location['x']
top = location['y']
right = location['x'] + size['width']
bottom = location['y'] + size['height']
im = im.crop((left, top, right, bottom))
driver.get('http://www.theambler.co.uk/')
get_logo(driver)
logo = driver.find_elements_by_xpath("//a['{}']/img"\
                                          .format(driver.current_url))
logo[0].get_attribute('src')
driver.current_url
driver.get('http://www.macclesfield-express.co.uk/')
get_logo(driver)
logo = driver.find_elements_by_xpath("//a[contains(@id, 'logo')]")
logo[0].value_of_css_property('background-color')
logo
body = driver.find_element_by_tag_name("body")
driver.execute_script("""
... var element = arguments[0],
...     style = element.currentStyle || window.getComputedStyle(element, false);
... 
... return style['background-image'];
... """, logo[0])

logo = driver.find_elements_by_xpath("//a[@href = '{}']"\
                              .format(driver.current_url))

#%%
a.to_csv('back_up4.csv')
