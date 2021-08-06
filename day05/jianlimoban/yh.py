#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/7/30 15:01
# software: PyCharm
#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5

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


# 在这里调用的时候把相应的信息放进去（账号密码软件id，就不用重复的放了）
# 留两个参数使其调用更加灵活
# code_path是验证码的图片的路径
# code_type是验证码的类型
def get_code(code_path,code_type):
	chaojiying = Chaojiying_Client('wangzhengjie', 'wang124yi309ji', '920327')	#用户中心>>软件ID 生成一个替换 96001
	im = open(code_path, 'rb').read()													#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
	return (chaojiying.PostPic(im, code_type))


