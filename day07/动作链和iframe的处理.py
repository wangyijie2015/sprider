#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/8/1 10:34
# software: PyCharm
from selenium import webdriver
from time import sleep
#导入动作链对应的类
from selenium.webdriver import ActionChains

bro = webdriver.Chrome(executable_path='./chromedriver.exe')

#如果定位的标签是存在于iframe标签中的则必须通过如下操作进行标签定位
bro.get('https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')
bro.switch_to.frame("iframeResult")#切换浏览器标签定位的作用域

div = bro.find_element_by_id('draggable')

#动作链
#实例化一个ActionChains对象
action  =ActionChains(bro)
#点击长按指定的标签
action.click_and_hold(div)

for i in range(5):
    #perform()立即执行动作链操作
    #move by offset(x,y):x表示水平方向,y表示竖直方向
    action.move_by_offset(17,0).perform()
    sleep(0.3)

#释放动作链
action.release()

bro.quit()
