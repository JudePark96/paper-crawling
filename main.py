# -*- coding: utf-8 -*-
__author__ = 'JudePark'
__email__ = 'judepark@kookmin.ac.kr'

import json
import logging
import pandas as pd

from selenium import webdriver
from tqdm import tqdm
from modules import search_by_filter, parse_pages

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    path = './chromedriver_v85'
    driver = webdriver.Chrome(path)
    driver.get('https://www.dbpia.co.kr/')

    search_filter = {
        'keyword': '딥러닝',
        'year_filter': True,
        'year_start': 2015,
        'year_end': 2020
    }

    logger.info(driver.window_handles)
    logger.info(json.dumps(search_filter))
    search_by_filter(driver, args=search_filter)
    dataset = parse_pages(driver)

    title = [data['title'] for data in tqdm(dataset)]
    abstract = [data['abstract'] for data in tqdm(dataset)]
    keyword = [data['keyword'] for data in tqdm(dataset)]

    df = dict(title=title, abstract=abstract, keyword=keyword)
    df = pd.DataFrame(df)

    output_file_name = './{}_{}_{}.csv'.format(search_filter['keyword'], search_filter['year_start'],
                                               search_filter['year_end'])
    df.to_csv(output_file_name, encoding='utf-8')
