#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/8/1 15:59
# software: PyCharm
from selenium import webdriver
from time import sleep

bro = webdriver.Chrome(executable_path='./chromedriver.exe')
bro.get('https://qzone.qq.com/')
bro.maximize_window()
bro.switch_to.frame('login_frame')

a_tag = bro.find_element_by_id("switcher_plogin")
a_tag.click()

userName_tag = bro.find_element_by_id('u')
password_tag = bro.find_element_by_id('p')
sleep(1)
userName_tag.send_keys('1243097542')
sleep(1)
password_tag.send_keys('youjihuaxue')
sleep(1)
btn = bro.find_element_by_id('login_button')
btn.click()

sleep(5)

bro.quit()

