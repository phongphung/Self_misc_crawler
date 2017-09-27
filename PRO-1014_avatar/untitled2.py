    from selenium import webdriver

    driver = webdriver.Chrome()

    driver.get('https://www.homely.com.au/agents')

    search = driver.find_element_by_xpath(
                        "//input[starts-with(@class, 'SearchAutoComplete-input')]")
    search.clear()
    search.send_keys('ge')
    auto_complete = driver.find_elements_by_xpath(
            "//li[starts-with(@class, 'SearchAutoComplete-item')]")
    auto_complete[0].click()
