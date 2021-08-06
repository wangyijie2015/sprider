#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/8/1 18:23
# software: PyCharm
from selenium import webdriver
from PIL import Image
from time import sleep
from selenium.webdriver import ActionChains
# 实现规避检测
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


# 超级鹰
def Codemode(path, mode):
    Path = path
    Mode = mode
    chaojiying = Chaojiying_Client('wangzhengjie', 'wang124yi309ji', '920327')  # 用户中心>>软件ID 生成一个替换 96001
    im = open(Path, 'rb').read()  # 图片文件路径  有时WIN系统须要//
    return chaojiying.PostPic(im, Mode)['pic_str']


if __name__ == '__main__':
    # 实现规避检测
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 隐藏window.navigator.webdriver
    option.add_argument("--disable-blink-features=AutomationControlled")
    # 添加user-agent
    option.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')

    # 实例化一个浏览器对象
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=option)

    # 防止12306禁止selenium
    script = 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined,configurable: true});'
    driver.execute_script(script)

    try:
        driver.get('https://kyfw.12306.cn/otn/resources/login.html')
        # driver.maximize_window()  # 最大化浏览器
        sleep(2)

        # 账号登陆页面
        xpath = driver.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[2]/a')
        xpath.click()
        sleep(3)

        # 输入用户名密码
        user_text = driver.find_element_by_id('17854117105')
        user_text.send_keys('username_12306')
        pwd_text = driver.find_element_by_id('wang124yi309ji')
        pwd_text.send_keys('pwd_12306')
    except Exception as e:
        print(e)

    # 页面截图
    # 获取页面的宽高
    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    # 设置页面的宽高
    driver.set_window_size(width, height)

    # 获取截图方法一：
    # code_img_ele = driver.find_element_by_xpath('//*[@id="J-loginImg"]').screenshot('code.png')

    # 获取截图方法二：
    # save_screenshot将当前页面进行截图且保存
    driver.save_screenshot('shot.png')
    # 确定验证码图片对应的左上角和右下角的坐标（裁剪的区域就确定）
    code_img_ele = driver.find_element_by_xpath('//*[@id="J-loginImg"]')
    location = code_img_ele.location  # 验证码左上角坐标
    size = code_img_ele.size  # 验证码标签对应的长宽
    # 左上角和右下角坐标
    k = 1.24
    rangle = (
        int(location['x']) * k - 35, int(location['y']) * k + 5,
        int(location['x']) * k - 18 + int(size['width']) * k + 5,
        int(location['y']) * k + int(size['height']) * k + 5)

    # 实例化Image类
    image_open = Image.open('./shot.png')
    # 根据指定区域进行图片裁剪
    crop = image_open.crop(rangle)
    crop.save('code.png')

    # 将验证码图片提交给超级鹰进行识别
    try:
        answer = Codemode('code.png', 9004)
        print(answer)
        all_list = []
        if '|' in answer:
            list_1 = answer.split('|')
            list_len = len(list_1)
            for i in range(list_len):
                xy_list = []
                x = int(list_1[i].split(',')[0])
                y = int(list_1[i].split(',')[1])
                xy_list.append(x)
                xy_list.append(y)
                all_list.append(xy_list)
        else:
            x = int(answer.split(',')[0])
            y = int(answer.split(',')[1])
            xy_list = [x, y]
            all_list.append(xy_list)
        for list_2 in all_list:
            x = list_2[0] * 0.8
            y = list_2[1] * 0.8
            ActionChains(driver).move_to_element_with_offset(code_img_ele, x, y).click().perform()
            sleep(0.5)

        # 点击登陆
        login_button = driver.find_element_by_css_selector('#J-login')
        login_button.click()
    except Exception as e:
        print(e)

    sleep(2)
    # 完成滑块验证
    action = ActionChains(driver)
    try:
        # 点击指定的标签
        slider = driver.find_element_by_css_selector('#nc_1_n1z')
        action.click_and_hold(slider)
        action.move_by_offset(300, 0).perform()  # 移动滑块
        sleep(1)
        action.release()
    except Exception as e:
        print(e)
