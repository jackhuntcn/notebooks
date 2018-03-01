#coding:utf8

import time
import random
import json
import requests
from hashlib import md5

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1',
    'Referer': 'https://image.baidu.com'
}

URL_TEMPLATE = 'https://image.baidu.com/search/wisejsonala?tn=wisejsonala&ie=utf8&cur=result&word=%s&fr=&catename=&pn=%d&rn=30&gsm=1e'

def md5name(strings):
    return md5(strings).hexdigest()

def save_file(file_path, url):
    req = requests.get(url, headers=HEADERS, stream=True)
    with open(file_path, 'wb') as save_file:
        for chunk in req.iter_content(1024):
            save_file.write(chunk)

def fetch_one_page(word, pn=0):
    url = URL_TEMPLATE % (word, pn)
    resp = requests.get(url, headers=HEADERS, timeout=10)
    js = json.loads(resp.text)
    return js['data']

class Worker(object):
    def work(self, word, start, end, seconds):
        for p in range(int(start), int(end)):
            data = fetch_one_page(word=word, pn=30*p)
            for item in data:
                thumburl = item['thumburl']
                save_file('./data/%s.jpg' % md5name(thumburl), thumburl)
                time.sleep(random.randint(1, int(seconds)))
            time.sleep(2)

if __name__ == '__main__':
    import fire
    fire.Fire(Worker)
