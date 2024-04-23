import requests
from functools import partial
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
import os
import hashlib
from functools import partial
from datetime import datetime, timedelta
from io import StringIO

def get_proxy():
    url = 'https://free-proxy-list.net/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}
    source = requests.get(url, headers=headers, timeout=10)
    df = pd.read_html(StringIO(source.text))[0]
    df['IP'] = df['IP Address'] + ':' + df['Port'].apply(str)
    list_ip = df['IP'].to_list()
    # lưu lại danh sách proxy
    with open("list_proxies.txt", "w") as file:
        for ip in list_ip:
            file.write(ip + "\n")

if __name__ == "__main__":
    get_proxy()