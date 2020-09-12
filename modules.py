# -*- coding: utf-8 -*-
__author__ = 'JudePark'
__email__ = 'judepark@kookmin.ac.kr'

import logging
import time
from typing import List, Dict, Union, Any

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils import remove_html_tag, is_english, switch_to_main_window

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

    flag = False

    for i in range(1):
        time.sleep(0.5)
        try:
            page_source = driver.page_source
            bs = BeautifulSoup(page_source, 'html.parser')

            for i in range(1, 6):
                try:
                    if '학술저널' in remove_html_tag(str(bs.select(f'#dev_plctType > li:nth-child({str(i)}) > span')[0])):
                        flag = True
                        btn = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, "//*[@id='pub_check_sort3_{}']".format(str(i - 1)))))
                        driver.execute_script("arguments[0].click()", btn)
                except Exception as e:
                    logger.info(str(e))

        except Exception as e:
            logger.info(str(e))

    if flag is False:
        exit(0)

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
        logger.info("page [{}] ...".format(w_count))


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
            logger.info(f'{idx} -> {attr}')

        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, attr))).click()
        except TimeoutException as e:
            time.sleep(0.5)
            logger.info(str(e))

        driver.switch_to_window(driver.window_handles[-1])
        page = driver.page_source
        bs_ = BeautifulSoup(page, 'html.parser')
        abstract = bs_.select('#pub_abstract > div.thesisDetailArea.eToggleSection > div > p:nth-child(1)')

        if abstract == []:
            switch_to_main_window(driver)
            time.sleep(0.5)
            continue

        abstract = remove_html_tag(str(abstract[0]))

        # 초록이 없을 수도 있음.
        try:
            if is_english(abstract) != 'ko':
                switch_to_main_window(driver)
                continue
        except Exception as e:
            logger.info(str(e))
            switch_to_main_window(driver)
            time.sleep(0.5)
            continue

        citation_keyword = bs_.head.find('meta', {'name': 'citation_keywords'})

        # 키워드가 없으면 닫는다.
        if citation_keyword == None:
            switch_to_main_window(driver)
            time.sleep(0.5)
            continue

        citation_keyword = citation_keyword.get('content')

        # 키워드가 영어로만 되어있을 경우 닫는다.
        if citation_keyword.isascii():
            switch_to_main_window(driver)
            time.sleep(0.5)
            continue

        title = bs_.find('meta', property="og:title")['content']
        logger.info(abstract.strip().lower())
        logger.info(citation_keyword.strip().lower())
        logger.info(title.strip().lower())

        dataset.append({
            'abstract': abstract.lower(),
            'keyword': citation_keyword.lower(),
            'title': title.lower()
        })

        time.sleep(1)

        switch_to_main_window(driver)

    logger.info("Number of data -> {}".format(len(dataset)))

    return dataset
