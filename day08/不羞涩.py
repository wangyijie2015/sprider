#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$wangyijie
# datetime:2021/8/5 14:37
# software: PyCharm
import os

import requests
import random
import time

from bs4 import BeautifulSoup

if __name__ == '__main__':
    if not os.path.exists('./image'):
       os.mkdir('./image')
    #有颜值板块的多页图片爬取
    url_list = ['https://www.buxiuse.com/?cid=4&page={}'.format(page) for page in range(1,4)]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }

    #在函数中遍历url列表，并用request方法获取响应内容，并用BeautifulSoup来解析页面，并获取所有的<img>标签，保存在src_list列表中
    i = 0
    for url in url_list:
        response = requests.get(url=url,headers=headers).text

        soup = BeautifulSoup(response,'lxml')
        scr_list = soup.find_all('img')

    #遍历src_list，获取其中的src和alt属性（获取了图片的连接和图片的名称），用with open方法保存，设置随机的停顿，防止被识别为爬虫
    for img in scr_list:
        src = img.get('src')
        name = img.get('alt')
        with open('./image/{}-img.jpg'.format(name),'wb') as fp:
            fp.write(requests.get(src,headers=headers).content)
        time.sleep(random.random())
        print('图片正在下载中.jpg'.format(name))

        fp.close()