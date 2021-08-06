#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/8/1 19:01
# software: PyCharm
from selenium import webdriver
from hashlib import md5
import requests
import time
from selenium.webdriver import ActionChains
# bro = webdriver.Chrome(executable_path=./chromedriver)
#     bro.get(https://kyfw.12306.cn/otn/resources/login.html)
#
#     a_tag = bro.find_elements_by_class_name(login-hd-account)【0】
#     print(a_tag)
#     a_tag.click()    img_src = bro.find_element_by_id(J-loginImg)
#     detail_img_src = img_src.get_attribute(src)#获得验证码图片的src，注意是base64类型，需要进行转化
#     #img_data = requests.get(url=detail_img_src,headers=headers).content
#     detail_img_src1 = detail_img_src.split(64,)【-1】#只需要获得64，的字符
#     print(detail_img_src1)
#     imgdata = base64.b64decode(detail_img_src1)#进行转码
#
#     #将验证码图片保存到了本地
#     with open(./code.jpg,wb) as fp:
#         fp.write(imgdata)