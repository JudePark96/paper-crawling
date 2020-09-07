# -*- coding: utf-8 -*-
__author__ = 'JudePark'
__email__ = 'judepark@kookmin.ac.kr'

import logging
import time
from typing import List, Dict, Union, Any

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils import remove_html_tag, is_english

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def search_by_filter(driver: webdriver, args: dict) -> None:
    logger.info("start searching ...")
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

    # 학술저널과 학술대회자료
    for i in range(1):
        time.sleep(0.5)
        try:
            # btn = WebDriverWait(driver, 20).until(
            #     EC.element_to_be_clickable((By.XPATH, "//*[@id='pub_check_sort3_0']")))
            # driver.execute_script("arguments[0].click()", btn)
            btn2 = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='pub_check_sort3_1']")))
            driver.execute_script("arguments[0].click()", btn2)
        except Exception as e:
            print(e)

    # 더보기
    w_count = 0

    while (True):
        time.sleep(1)
        try:
            more = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='contents']/div[2]/div[3]/div[3]/div[3]/div/a")))
            driver.execute_script("arguments[0].click()", more)
        except:
            logger.info('trying to retry or no more pages. please wait.')
            break
        w_count += 1
        logger.info(" + page [{}]".format(w_count))


def parse_pages(driver: webdriver) -> List[Dict[str, Union[str, Any]]]:
    logger.info("start parsing ...")

    page_source = driver.page_source
    bs = BeautifulSoup(page_source, 'html.parser')
    items = bs.find('div', 'searchListArea').find('div', 'listBody').find('ul').find_all('li', 'item')

    links = []
    dataset = []

    for item in items:
        title = item.find('div', 'titWrap').find('a')
        if 'href' in title.attrs:
            links.append(title.attrs['href'])
        else:
            continue

    for idx, link in enumerate(links):
        time.sleep(1)
        attr = f"//a[@href='{link}']"

        if idx % 20 == 0:
            logger.info(attr)

        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, attr))).click()

    for window in driver.window_handles[1:]:
        driver.switch_to_window(window)
        page = driver.page_source
        bs_ = BeautifulSoup(page, 'html.parser')

        abstract = bs_.select('#pub_abstract > div.thesisDetailArea.eToggleSection > div > p:nth-child(1)')

        if abstract == []:
            driver.close()
            continue

        abstract = remove_html_tag(str(abstract[0]))

        # 한국어 초록이 아니면 창을 닫는다.
        if is_english(abstract) != 'ko':
            driver.close()
            continue

        citation_keyword = bs_.head.find('meta', {'name': 'citation_keywords'})

        # 키워드가 없으면 닫는다.
        if citation_keyword == None:
            driver.close()
            continue

        title = bs_.find('meta', property="og:title")['content']
        citation_keyword = citation_keyword.get('content')

        logger.info(abstract.strip().lower())
        logger.info(citation_keyword.strip().lower())
        logger.info(title.strip().lower())

        dataset.append({
            'abstract': abstract,
            'keyword': citation_keyword,
            'title': title
        })

    logger.info("Number of data -> {}".format(len(dataset)))

    return dataset
