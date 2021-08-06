#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/7/30 16:35
# software: PyCharm
#编码流程:
#1.验证码的识别,获取验证码图片的文字数据
#2.对post请求进行发送（需要处理请求参数）
#3.对响应数据进行持久化存储
import requests
from lxml import etree

from learn.day05.jianlimoban import yh

if __name__ == '__main__':
    #1.对验证码图片进行捕获和识别
   url = 'http://www.renren.com/login?to=http%3A%2F%2Fwww.renren.com%2F'
   headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
   }
   page_text = requests.get(url=url, headers=headers).text
   tree = etree.HTML(page_text)
   code_img_src = tree.xpath('//div[@class="code"]/img/@src')[2]
   # print(code_img_src)
   # print(type(code_img_src))

   # print(code_img_src)
   code_img_data = requests.get(url=code_img_src, headers=headers).content
   with open('code.jpg', 'wb') as fp:
       fp.write(code_img_data)


# #2.使用示例代码打码对验证码图片进行识别
   code = yh.get_code('./code.jpg', '1005')
   print(code)

#post请求的发送（模拟登录）
   login_url = ''
   data = {

   }
   response = requests.post(url=login_url,headers=headers,data=data)
   print(response.status_code)

   # with open('renren.html','w',encoding='utf-8') as fp:
   #     fp.write(login_page_text)