#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/8/1 9:37
# software: PyCharm
#使用aiohttp中的ClientSession
#单线程的异步操作处理
import time
import asyncio
import aiohttp
if __name__ == '__main__':
    stat = time.time()
urls  = ['www.baidu.com',
         'www.sogou.com',
         'www.douban.com']

async def get_page(url):
    async with aiohttp.ClientSession()  as session: #调用aiohttp的一个类ClientSession
        #get:发起的是get请求，请求参数params
        #post（）:发起post请求  请求参数data
        #headers进行UA伪装,proxy='http://ip:port'请求使用代理
        async with await session.get(url) as responsse:
            """
            text()返回以字符串形式的响应数据
            read()返回二进制形式的响应数据
            json()返回json对象
            注意:获取响应数据操作响应数据操作前一定要使用await进行手动挂起
            """
            page_text = await responsse.text()
            print(page_text)

tasks = []
for url in urls:
    c = get_page(url)
    task = asyncio.ensure_future(c)
    tasks.append(task)

loop = asyncio.get_event_loop()
#异步协程固定写法 创建事件循环
loop.run_until_complete(asyncio.wait(tasks))

end = time.time()
print('总耗时：',end-stat)
