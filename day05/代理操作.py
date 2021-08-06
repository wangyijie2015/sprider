#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/7/30 20:05
# software: PyCharm
import requests
if __name__ == '__main__':
  url = 'http://www.baidu.com/s?wd=ip'
  headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'

  }
  page_tetx = requests.get(url=url,headers=headers,proxies={"https":'121.232.148.51:3256'}).text
  with open('ip.html','w',encoding='utf-8') as fp:
      fp.write(page_tetx)