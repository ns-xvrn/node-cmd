import requests, time, json
from bs4 import BeautifulSoup as bs
from pathlib import Path
import util
import threading
from time import time, sleep

lock = threading.Lock()


URL = 'https://river.com'
delay = int(util.get_conf('info')['price_fetch_delay'])

def save_price(run_forever=True):
    while(True):
        if run_forever: sleep(delay)
        r = requests.get(URL)
        content = bs(r.content, 'html.parser')
        price = content.find('p', {'class':'js-nav-price'})
        price = int(float(price.text.strip().replace(',', '').replace('$', '')))
        data = {"price":price, "timestamp":time()}
        fp = Path('ext_data.json')
        if fp.exists(): fp.unlink()
        lock.acquire()
        with fp.open("w", encoding="UTF-8") as f: 
            json.dump(data, f)
        lock.release()
        if not run_forever: break