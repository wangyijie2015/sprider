#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/7/30 18:32
# software: PyCharm
import requests
if __name__ == '__main__':

   #创建一个seesion对象
   session = requests.Session()
   detail_url = 'http://www.renren.com/personal/2147565851/details'
   headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'

   }
   #使用seseion对象请求post请求的发送
   response = session.post(url=detail_url,headers=headers,data=data)
   detail_page_text = requests.get(url=detail_url,headers=headers).text
   #手动cookie处理
   headers={
       'Cookie':'taihe_bi_sdk_uid=e3a02f23945da4677f32691ff1307d23; taihe_bi_sdk_session=e22ad0f2a8ccb00590e14c52ce98966f; anonymid=krq1vy4k-97aa76; ick=581af61e-22ff-4c72-b708-9d6edecf1fc8; LOCAL_STORAGE_KEY_RENREN_USER_BASIC_INFO={"userName":"wangzhengjie","userId":2147565851,"headUrl":"","secretKey":"3eeb2e771a622207e5bc7b0fcef370c0","sessionKey":"929gDzpncnynlO3P"}; Hm_lvt_ad6b0fd84f08dc70750c5ee6ba650172=1627632889,1627634640,1627641047,1627641130; Hm_lpvt_ad6b0fd84f08dc70750c5ee6ba650172=1627645123'
   }
   with open('wangyijie.html','w',encoding='utf-8') as fp:
       fp.write(detail_page_text)

