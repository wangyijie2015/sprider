#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/8/5 9:09
# software: PyCharm
# -*- coding：utf-8 -*-
import requests
import re
import os
import time
from urllib.request import urlretrieve
from queue import Queue
import threading


def Productor(q, urls):
    for i in range(0, 200):
        base_url = ("https://www.buxiuse.com/?page={}".format(i))
        urls.append(base_url)
        headers = {
            'headers': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36'
        }
        response = requests.get(base_url, headers=headers)
        regx = re.compile(r'<img class="height_min" title=".*?" alt=".*?".*?src="(.*?)"')
        image_urls = re.findall(regx, response.text)
        for item in image_urls:
            q.put(item)


def Consumer(q, urls):
    if not os.path.exists('image'):
        os.mkdir('image')
    if len(urls) == 200 and q.empty():
        exit('爬取完成')
    else:
        while True:
            image_url = q.get()
            if image_url:
                name = image_url.rsplit('/', 1)[1]
                time.sleep(0.2)
                urlretrieve(image_url, "image/%s" % name)


if __name__ == '__main__':
    q = Queue(maxsize=1000)
    urls = []
    for i in range(4):
        p = threading.Thread(target=Productor, args=(q, urls))
        p.start()
    for x in range(5):
        c = threading.Thread(target=Consumer, args=(q, urls))
        c.start()


