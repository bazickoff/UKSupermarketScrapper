import requests
import re
from requests import get
from bs4 import BeautifulSoup

# checker is the controller to decide the starting point for scrapping
r = requests.get('https://www.waitrose.com/content/waitrose/en/bf_home/branch_finder_a-z.html')
r = requests.get('https://www.waitrose.com/content/waitrose/en/bf_home/branch_finder_a-z.html', cookies= r.cookies)
soup = BeautifulSoup(r.text, 'html.parser')
LocList=[]
codeList=[]
shop_detail_info_list =[]
checker = None
for link in soup.select('p a[href]'):
    if link.text=='Abergavenny':
        checker= True
    if checker:
        LocList.append(link.text)
        codeList.append(link['href'][-8:-5])
print(codeList)

# detail match of each store

match_str = 'Please enter some search text or select a branch from the dropdown list.'
for index in codeList:
    r = get('https://www.waitrose.com/content/waitrose/en/bf_home/bf/'+index+'.html')
    r = requests.get('https://www.waitrose.com/content/waitrose/en/bf_home/bf/'+index+'.html', cookies= r.cookies)
    soup = BeautifulSoup(r.text, 'html.parser')
    parse_target = []
    for link in soup.select('p'):
        parse_target.append(link.text)
    for i in range(len(parse_target)):
        if re.match(match_str,parse_target[i]):
            shop_detail_info_list.append(parse_target[i+1])

import csv

with open("../data/out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(shop_detail_info_list)

import pandas as pd
import numpy as np
waitrose_df = pd.DataFrame(np.column_stack([LocList, codeList]),
                               columns=['Location', 'codeList'])
waitrose_df.to_csv('waitrose_data_raw.csv',encoding='utf-8')
waitrose_df.head()