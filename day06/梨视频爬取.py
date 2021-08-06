#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/7/31 15:42
# software: PyCharm
import random

# coding:utf-8
import requests
import random
import os
import re
from fake_useragent import UserAgent
from multiprocessing.dummy import Pool

from lxml import etree


class LiVideoSpider:
    '''梨视频爬虫类'''

    def __init__(self):
        self.st_url = 'https://www.pearvideo.com/category_4'  # 首页url
        self.p = Pool(4)  # 创建4个线程的线程池
        self.headers = {
            'ua': UserAgent().random
        }
        self.items = []  # 存储视频相关信息，[{'id':'xxx','video_url':'xxx'...},...]
        self.video_path = './梨视频'  # 视频存储路径

    def start(self):
        '''爬虫入口'''

        # 创建存储文件夹
        if not os.path.exists(self.video_path):
            os.mkdir(self.video_path)

        # 获取主页数据
        response = requests.get(url=self.st_url, headers=self.headers)
        tree = etree.HTML(response.text)
        li_list = tree.xpath('//*[@id="listvideoList"]/ul/li')

        # 解析主页数据，提取id,详情页url，视频标题
        for li in li_list:
            title = li.xpath('.//div[@class="vervideo-title"]/text()')[0]
            detail_url = li.xpath('./div/a/@href')[0]
            id = detail_url.split('_')[-1]
            item = {
                'id': id,
                'title': title + '.mp4',
                'detail_url': detail_url
            }
            self.items.append(item)

            # 构造每个视频ajax请求的url
        for i in range(len(self.items)):
            js_url = 'https://www.pearvideo.com/videoStatus.jsp?contId={}&mrd={}'.format(self.items[i]['id'],
                                                                                         random.random())
            self.items[i]['js_url'] = js_url

        # 通过线程池异步获取每个视频的下载地址url
        items = self.p.map(self.get, self.items)

        # 异步下载每个视频
        self.p.map(self.download, items)

    def get(self, item):
        '''获取视频下载地址'''

        # headers中添上Referer参数
        headers = {
            'ua': UserAgent().random,
            'Referer': item['detail_url']
        }
        json_data = requests.get(url=item['js_url'], headers=headers).json()
        video_url = json_data["videoInfo"]["videos"]["srcUrl"]
        # 修正视频下载地址url
        item['video_url'] = re.sub(r'16\d+-', r'cont-{}-'.format(item['id']), video_url)
        return item

    def download(self, item):
        '''下载视频'''

        video_data = requests.get(url=item['video_url'], headers=self.headers).content
        with open(self.video_path + '/' + item['title'], 'wb') as f:
            f.write(video_data)


if __name__ == '__main__':
    LiVideoSpider().start()