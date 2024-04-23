import requests
from multiprocessing import Pool, Manager, cpu_count
from functools import partial
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
import os
import hashlib
import urllib3
from multiprocessing import Pool
from functools import partial
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time
from datetime import datetime, timedelta
import random


def check_proxy(http):
    http_proxy = "http://" + http
    base_url = "https://shopee.vn/api/v4/search/search_items?"
    url = "by={}&limit=60&match_id={}&newest={}&order={}&page_type=search&scenario=PAGE_OTHERS&version=2"
    new_url = url.format('sale', 100630, 0, 'desc')
    get_url = base_url + new_url
    try:
        headerNoneMatch = hashlib.md5(
            "55b03{}55b03".format(hashlib.md5(new_url.encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest()

        req = requests.get(get_url, headers={
            "If-None-Match-": "55b03-" + headerNoneMatch,
            "Sec-Fetch-Mode": "cors",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
            "X-API-SOURCE": "pc",
            "X-Requested-With": "XMLHttpRequest"
        }, proxies={"http": http_proxy, "https": http_proxy}, timeout=10)
        # v = requests.get("https://httpbin.org/ip",proxies={"http": http_test, "https": http_test},verify=False,
        #                  headers={
        #                      "User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"},timeout=10)
        if req.status_code == 200:
            return http
        else:
            return None

    except Exception as e:
        print("Connection Refused")
        return None

def get_multiprocess(list_manager=None, list_ip=None, process=0):
    query = list_ip[process]
    result = check_proxy(query)
    if result != None:
        list_manager.append(result)
        return


def multi_check(list_ip):
    n_process = 16
    manager = Manager()
    ## Need a manager to help get the values async, the values will be updated after join
    list_manager = manager.list()
    pool = Pool(n_process)
    part_get_clean = partial(get_multiprocess, list_manager, list_ip)
    pool.imap(part_get_clean, list(range(0, len(list_ip))))
    pool.close()
    pool.join()
    product_list = list(list_manager)
    return product_list


def get_proxy_active():
    url = 'https://free-proxy-list.net/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}
    source = requests.get(url, headers=headers, timeout=10)
    df = pd.read_html(source.text)[0]
    df['IP'] = df['IP Address'] + ':' + df['Port'].apply(str)
    list_ip = df['IP'].to_list()
    list_proxy = multi_check(list_ip)
    with open("outfile.txt", "w") as outfile:
        outfile.write("\n".join(list_proxy))
