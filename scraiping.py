import time
import os

import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging

import settings

logger = logging.getLogger(__name__)

def exec_scraiping(page_num):

    params = {"page": page_num}

    try:
        contents = requests.get(settings.search_url,params=params)
    except Exception as e:
        logger.error(f'action=request error={e}')

    soup = BeautifulSoup(contents.text)

    #各要素取得
    spot_names = soup.find_all('dt', class_='spot-name')
    spot_names_list = [i.text.replace('\n', '').replace('\t', '') for i in spot_names]
    addresses = soup.find_all('dl', class_='spot-detail-section')
    addresses_text = [str(i)[:198] for i in addresses]
    addresses_text2 = [str(i)[184:] for i in addresses_text]
    addresses_links = soup.find_all('a', class_='spot-link-text')
    addresses_links_text = [i.get('href') for i in addresses_links]

    #場所、住所、URLを取得
    list_all = []
    for i, (spot_name,address,address_link) in enumerate(zip(spot_names_list, addresses_text2, addresses_links_text)):
        dict = {}
        dict['spot_name'] = spot_name
        dict['address'] = address
        dict['address_link'] = address_link

        list_all.append(dict)

    return list_all

def dump_csv(list_all, header=None):
    data = pd.DataFrame(list_all)
    data.to_csv('test.csv',index=False,header=header,mode='a')

def exec():
    for i in range(1,3):
        list_all = exec_scraiping(i)
        dump_csv(list_all)

