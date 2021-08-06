#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/7/30 10:55
# software: PyCharm
import requests
from lxml import etree

#封装识别验证码图片的函数
from learn.day05.jianlimoban import yh
from learn.day05.jianlimoban.yh import Chaojiying_Client

if __name__ == '__main__':

  url = 'https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx'
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'

}
  page_text = requests.get(url=url,headers=headers).text

  #解析验证码图片img中src属性值
  tree = etree.HTML(page_text)
  code_img_src = 'https://so.gushiwen.org'+tree.xpath('//*[@id="imgCode"]/@src')[0]
  img_data = requests.get(url=code_img_src,headers=headers).content
  #已经将验证码图片保存到了本地
  with open('./code.jpg','wb') as fp:
    fp.write(img_data)

  # #调用第三方进行解析：
  # chaojiying = Chaojiying_Client('wangzhengjie', 'wang124yi309ji', '920327')
  # im = open('./code.jpg', 'rb').read()
  # print(chaojiying.PostPic(im, 1902))

  #调用第三方进行一个解析：
  code = yh.get_code('./code.jpg','1004')
  print(code)




