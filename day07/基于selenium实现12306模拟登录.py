#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/8/1 17:03
# software: PyCharm
import time
from tkinter import Image

import requests
from hashlib import md5
from selenium.webdriver import ActionChains

from selenium.webdriver.chrome.options import Options
from time import sleep
#实现规避检测
from selenium.webdriver import ChromeOptions

class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


# if __name__ == '__main__':
# 	chaojiying = Chaojiying_Client('wangzhengjie', 'wang124yi309ji', '920327')	#用户中心>>软件ID 生成一个替换 96001
# im = open('img.png', 'rb').read()													#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
# print( chaojiying.PostPic(im, 9004)['pic_str'])										#1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()

#使用selenium打开登录页面
from selenium import webdriver
import time
bro = webdriver.Chrome(executable_path='./chromedriver.exe')
bro.maximize_window()
# bro.get('https://kyfw.12306.cn/otn/login/init')
bro.get('https://kyfw.12306.cn/otn/resources/login.html')
time.sleep(2)

#点击登录按钮
a_tag = bro.find_element_by_class_name('login-hd-account')[0]
print(a_tag)
#save screenshot就是对当前页面进行截图并保存
bro.save_screenshot("aa.png")

#确定验证码图片对应的左上角和右下角的坐标(裁剪的区域就确定了）
code_img_else = bro.find_element_by_xpath('//*[@id="loginForm"]/div/ul[2]/li[4]/div/div/div[3]/img"]')
location = code_img_else.location #验证码图片左上角的坐标 x,y
print('location:',location)
size = code_img_else.size #验证码标签对应的长和宽
print('size:',size)
#验证码左上角和右下角的坐标
rangle = (
    int(location['x']), int(location['y']), int(location['x']+size['width']), int(location['y']+size['height']))
#至此验证码图片区域就确定下来了

i = Image.open('aa.png')
code_img_name = './code.png'
#crop根据指定区域进行图片裁剪
frame = i.crop(rangle)
frame.save(code_img_name)

#将验证码图片提交给超级鹰
chaojiying = Chaojiying_Client('wangzhengjie', 'wang124yi309ji', '920327')	#用户中心>>软件ID 生成一个替换 96001
im = open('code.png', 'rb').read()													#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
result =  chaojiying.PostPic(im, 9004)['pic_str']

print(result)
# 这里就是处理超级鹰返回坐标的方法了
all_list = []
# 通过判断超级鹰返回坐标的格式进行坐标处理，
# 返回的坐标有两种形式，一种是以|隔开的，一种是用,隔开的，对应下面两种处理方式
# 处理好的坐标存入list
if '|' in result:
    list = result.split('|')
    for i in range(len(list)):
        x_y = []
        x = int(list[i].split(',')[0])
        y = int(list[i].split(',')[1])
        x_y.append(x)
        x_y.append(y)
        all_list.append(x_y)
else:
    x_y = []
    x = int(result.split(',')[0])
    y = int(result.split(',')[1])
    x_y.append(x)
    x_y.append(y)
    all_list.append(x_y)
print(all_list)
# 处理好的坐标进行循环，并带入selenium进行点击点击
for l in all_list:
    x = l[0]
    y = l[1]
    ActionChains(bro).move_to_element_with_offset(
        im, x, y).click().perform()
    time.sleep(0.5)
# 图片点击好以后，向表单内发送账户密码
bro.find_element_by_xpath('//*[@id="J-userName"]').send_keys('账号')
bro.find_element_by_xpath('//*[@id="J-password"]').send_keys('密码')
# 进行点击登录按钮
bro.find_element_by_xpath('//*[@id="J-login"]').click()
time.sleep(2)
# 下面就是滑动模块了
# 上面已经更改过selenium的滑动模块，所以这里就可以直接定位到按钮的位置，进行点击滑动
span = bro.find_element_by_xpath('//*[@id="nc_1_n1z"]')
action = ActionChains(bro)
# 这里是selenium的方法，按住点击不放
action.click_and_hold(span)
# 下面就是滑动了
action.drag_and_drop_by_offset(span, 400, 0).perform()
# 这里加了个循环，就是滑动不行，一直刷新继续滑动，直到成功
# 其实这里也只是为了保险起见，因为上面改了滑动框，基本上都会成功
while True:
    try:
        info = bro.find_element_by_xpath('//*[@id="J-slide-passcode"]/div/span').text
        print(info)
        if info == '哎呀，出错了，点击刷新再来一次':
            # 点击刷新
            bro.find_element_by_xpath('//*[@id="J-slide-passcode"]/div/span/a').click()
            time.sleep(0.2)
            # 重新移动滑块
            span = bro.find_element_by_xpath('//*[@id="nc_1_n1z"]')
            action = ActionChains(bro)
            # 点击长按指定的标签
            action.click_and_hold(span).perform()
            action.drag_and_drop_by_offset(span, 400, 0).perform()
            time.sleep(5)
    except:
        print('ok!')
        break
# 完成后，松开鼠标
action.release()

time.sleep(5)
# 退出
bro.quit()
