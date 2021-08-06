#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/8/1 8:58
# software: PyCharm
import requests
import asyncio
import time
if __name__ == '__main__':
  start = time.time()
urls = [
      'http://127.0.0.1:5000/bobo','http://127.0.0.1:5000/jay','http://127.0.0.1:5000/wangyijie'
  ]

async def get_page(url):
      print('正在下载',url)
      #request.get是基于同步,必须要使用基于异步的网络请求模块进行指定url的请求发送
      response = requests.get(url=url)
      print('下载完毕:',response.text)

tasks = []

for url in urls:
      c = get_page(url)
      tasks = asyncio.ensure_future(c)
      tasks.append(tasks)

loop  =asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

end = time.time()

print('总耗时:',end-start)