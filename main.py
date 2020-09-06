# -*- coding: utf-8 -*-
__author__ = 'JudePark'
__email__ = 'judepark@kookmin.ac.kr'

from selenium import webdriver
from modules import search_by_filter

path = './chromedriver_v85'
driver = webdriver.Chrome(path)
driver.get('https://www.dbpia.co.kr/')

search_filter = {
    'keyword': '딥러닝',
    'year_filter': True,
    'year_start': 2019,
    'year_end': 2020
}

search_by_filter(driver, args=search_filter)

