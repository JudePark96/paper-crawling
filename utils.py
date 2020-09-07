# -*- coding: utf-8 -*-
__author__ = 'JudePark'
__email__ = 'judepark@kookmin.ac.kr'

import re

from langdetect import detect
from selenium import webdriver


def remove_html_tag(raw_html: str) -> str:
    rule = re.compile('<.*?>')
    res = re.sub(rule, '', raw_html)
    return res


def is_english(s: str) -> str:
    return detect(s)


def switch_to_main_window(driver: webdriver) -> None:
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


