# -*- coding: utf-8 -*-
__author__ = 'JudePark'
__email__ = 'judepark@kookmin.ac.kr'


from selenium import webdriver


def search_by_filter(driver: webdriver, args: dict) -> None:
    xpath = driver.find_element_by_xpath
    keyword = driver.find_element_by_id('keyword')
    keyword.clear()
    keyword.send_keys(args['keyword'])
    search_click_btn = xpath("//*[@id='header']/div[5]/div[6]/div[1]/div[1]/a")
    driver.execute_script("arguments[0].click();", search_click_btn)

    if args['year_filter'] is True:
        year_start = args['year_start']
        year_end = args['year_end']

        xpath("//*[@id='dev_sartYY']").send_keys(year_start)
        xpath("//*[@id='dev_endYY']").send_keys(year_end)
        click_btn = xpath("//*[@id='sidebar']/form/div[3]/div/div[1]/ul/li[4]/p/button")
        driver.execute_script("arguments[0].click();", click_btn)

