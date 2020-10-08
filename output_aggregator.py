# -*- coding: utf-8 -*-
__author__ = 'JudePark'
__email__ = 'judepark@kookmin.ac.kr'


from glob import glob
from tqdm import tqdm

import json


input_files = list(glob('./output/*.json'))
aggregated_store = []

for file in input_files:
    with open(file, 'r', encoding='utf-8') as f:
        for line in tqdm(f, desc=f'reading {file} file...'):
            aggregated_store.append(json.loads(line))
        f.close()

aggregated_store = [i for n, i in tqdm(enumerate(aggregated_store), desc='remove duplicated element...') 
                    if i not in aggregated_store[n + 1:]]

output_file_name = './output/combine_paper_data.json'

with open(output_file_name, 'w', encoding='utf-8') as f:
    for line in tqdm(aggregated_store, desc=f'writing {output_file_name}...'):
        f.write("{}\n".format(json.dumps(line)))
    f.close()

print('aggregating data done.')