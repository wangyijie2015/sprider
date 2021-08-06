#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/8/1 10:13
# software: PyCharm
url="http://125.35.6.84:81/xk/"
from selenium import webdriver
from lxml import etree
from time import sleep

if __name__ == '__main__':
    page_text_list=[]

driver=webdriver.Chrome()
driver.get("http://scxk.nmpa.gov.cn:81/xk/")
sleep(1)
page_text=driver.page_source
page_text_list.append(page_text)   #第一页

for i in range(3):
    driver.find_element_by_xpath("//*[@id='pageIto_next']").click() #点击下一页
    sleep(1)
    next_text=driver.page_source
    page_text_list.append(next_text)
    sleep(1)

list_name=[]
count=0

for text in  page_text_list:

    tree=etree.HTML(text)
    li_list = tree.xpath('//*[@id="gzlist"]/li')

    for li in li_list:
        name=li.xpath('./dl/@title')[0]
        list_name.append(name)
    if len(list_name)%10==0:
        print(list_name,end="\n")

