# -*- coding: utf-8 -*-
__author__ = 'JudePark'
__email__ = 'judepark@kookmin.ac.kr'

import json
import logging
import pandas as pd
import argparse

from selenium import webdriver
from tqdm import tqdm
from modules import search_by_filter, parse_pages

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument("--search_keyword", default='딥러닝', type=str)
    parser.add_argument("--year_start", default=2015, type=int)
    parser.add_argument("--year_end", default=2020, type=int)

    args = parser.parse_args()

    path = './chromedriver_v85'
    driver = webdriver.Chrome(path)
    driver.get('https://www.dbpia.co.kr/')

    search_filter = {
        'keyword': args.search_keyword,
        'year_filter': True,
        'year_start': args.year_start,
        'year_end': args.year_end
    }

    logger.info(driver.window_handles)
    logger.info(json.dumps(search_filter))
    search_by_filter(driver, args=search_filter)
    dataset = parse_pages(driver)
    output_file_name = './{}_{}_{}.json'.format(search_filter['keyword'], search_filter['year_start'],
                                               search_filter['year_end'])

    with open(output_file_name, 'w', encoding='utf-8') as fo:
        for data in tqdm(dataset):
            fo.write("{}\n".format(json.dumps(data)))
        fo.close()
