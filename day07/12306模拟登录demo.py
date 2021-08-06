from selenium import webdriver
from hashlib import md5
import requests
import time
from selenium.webdriver import ActionChains


#  这个类是超级鹰平台写的调用服务的接口代码，也是比较容易看懂的
class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')
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
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
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


#   这里进入模拟登录的主程序

# 实例化浏览器，并且最大化。然后请求12306主网站，我这里是从首页请求的，大家可以直接从登陆页面请求
browser = webdriver.Chrome()
browser.maximize_window()
browser.get('http://12306.cn/')
time.sleep(5)
# 因为是从首页请求的，所以下面有两个点击的动作，都是为了点进登陆页面
browser.find_element_by_xpath('//*[@id="J-header-login"]/a[1]').click()
time.sleep(0.3)
# 这里比较重要了，这里就是利用这个代码，来更改selenium中的滑动功能，让网站不报错
script = 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined,});'
browser.execute_script(script)
time.sleep(1)
# 这里进入帐号登录
browser.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[2]/a').click()
time.sleep(0.3)
#  这里直接定位验证码的png文件，然后保存
img = browser.find_element_by_xpath('//*[@id="J-loginImg"]')
img.screenshot('cde.png')
# 调用超级鹰的参数
chaojiying = Chaojiying_Client('wangzhengjie', 'wang124yi309ji', '920327')  # 这个在超级鹰的实例代码中有解释
im = open('../12306/cde.png', 'rb').read()
# 注意，这里返回的是一个字典格式，所以直接取要用的key，来返回坐标
result = chaojiying.PostPic(im, 9004)['pic_str']
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
    ActionChains(browser).move_to_element_with_offset(
        img, x, y).click().perform()
    time.sleep(0.5)
# 图片点击好以后，向表单内发送账户密码
browser.find_element_by_xpath('//*[@id="J-userName"]').send_keys('17854117105')
browser.find_element_by_xpath('//*[@id="J-password"]').send_keys('wang124yi309ji')
# 进行点击登录按钮
browser.find_element_by_xpath('//*[@id="J-login"]').click()
time.sleep(2)
# 下面就是滑动模块了
# 上面已经更改过selenium的滑动模块，所以这里就可以直接定位到按钮的位置，进行点击滑动
span = browser.find_element_by_xpath('//*[@id="nc_1_n1z"]')
action = ActionChains(browser)
# 这里是selenium的方法，按住点击不放
action.click_and_hold(span)
# 下面就是滑动了
action.drag_and_drop_by_offset(span, 400, 0).perform()
# 这里加了个循环，就是滑动不行，一直刷新继续滑动，直到成功
# 其实这里也只是为了保险起见，因为上面改了滑动框，基本上都会成功
while True:
    try:
        info = browser.find_element_by_xpath('//*[@id="J-slide-passcode"]/div/span').text
        print(info)
        if info == '哎呀，出错了，点击刷新再来一次':
            # 点击刷新
            browser.find_element_by_xpath('//*[@id="J-slide-passcode"]/div/span/a').click()
            time.sleep(0.2)
            # 重新移动滑块
            span = browser.find_element_by_xpath('//*[@id="nc_1_n1z"]')
            action = ActionChains(browser)
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
browser.quit()
