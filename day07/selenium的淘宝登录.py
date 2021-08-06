#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/8/1 10:34
# software: PyCharm
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
bro = webdriver.Chrome(executable_path='./chromedriver.exe')

bro.get('https://www.taobao.com/')

#实现标签定位
search_input = bro.find_element_by_id('q')
#标签的交互
search_input.send_keys('华为手机')

#执行一组js程序
bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')
sleep(2)
bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')
sleep(2)
#点击搜素按钮
btn = bro.find_element_by_css_selector('.btn-search')
btn.click()

bro.get('https://www.baidu.com')
inputs = bro.find_element_by_id('kw')
inputs.send_keys('安徽工业大学')
inputs.send_keys(Keys.ENTER)
#browser.find_element_by_id("su").click()
sleep(2)
#回退
bro.back()
sleep(2)
#前进
bro.forward()

sleep(5)
bro.quit()