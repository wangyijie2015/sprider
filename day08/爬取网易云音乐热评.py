#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/8/3 14:31
# software: PyCharm
#1.找到未加密的参数                     #window.arsea(参数，xxxx,xxxx,xxx)
#2.想办法对参数进行加密（必须参考网易的逻辑），parsms => encTetx,encSecKey => encSecKey
#3.请求网易云，得到评论

from Cryptodome.Cipher import AES
import requests
import json
from base64 import b64encode
#请求方式为post:

# url ='https://music.163.com/#/song?id=1847975477'
url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }

data = {
    "csrf_token": "",
    "cursor": "-1",
    "offset": "0",
    "orderType": "1",
    "pageNo": "1",
    "pageSize": "20",
    "rid": "R_SO_4_1465401422",
    "threadId": "R_SO_4_1465401422",
}

e = '010001'
f  ='00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
g = "0CoJUm6Qyw8W8jud"
i = '0hyFaCNAVzOIdoht'

def get_encSecKey():
    return '4022359ea3110bcd034e0160c3b89e5e172fd0110a3cf765d9f366d9fd09840a1f4a4705ac43719fdb8bfeb44d3b92334733061ad10942131184a4dfba0ac9d2cf867b8b6236523c1ca5f44c0d2d82c1c2665a3137a9241c7373539c1aa8e5e9bb9d33dafc764b5d76c2ab34fc94df85e27a934c8a603fa713f2cf38c2b7bbae'

def get_params(data): #默认这里接收的是字符串
    first = enc_params(data,g)
    second = enc_params(first,i)
    return second #返回就是params

def to_16(data):
    pad  =16-len(data)%16
    data += chr(pad) * pad
    return data

#加密过程
def enc_params(data,key):
   iv = "0102030405060708"
   data = to_16(data)
   aes =  AES.new(key=key.encode('utf_8'),IV=iv.encode('utf_8'),mode=AES.MODE_CBC) #创建加密器
   bs = aes.encrypt(data.encode('utf-8'))  #加密，加密的内容必须是16的倍数
   return  str(b64encode(bs),'utf-8')

#处理加密过程:加密过程
"""
   function a(a) { #随机的16位字符串
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1) #循环16ci
            e = Math.random() * b.length, #随机数
            e = Math.floor(e),  #取整
            c += b.charAt(e); #取字符串中的xxx位置 b
        return c
    }
    function b(a, b) { #a是要加密的内容
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a) #e是数据
          , f = CryptoJS.AES.encrypt(e, c, { #AES是加密的算法 c是加密的密钥
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    function c(a, b, c) {  #c这个算法不产生随机数
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) { # d:就是数据,e:010001，
        var h = {}  #空对象
          , i = a(16); #i就是一个16位的随机值，可以把i设置成定值
        h.encText = b(d, g), #b是密钥，g也是密钥
        h.encText = b(h.encText, i), #返回的就是params
        h.encSecKey = c(i, e, f),  #得到的就是encSeckey,e和f都是固定的值，i是随机值，如果此时我们把i固定,得到的key一定是固定的
        return h
    }
    
    两次加密:
    数据+g => b => 第一次加密+i =>b =>params
 """
if __name__ == '__main__':
  # page = int(input('请输出要查看的页数:'))
  print('开始爬虫了!!!')
  # fp = open('./网易云热评.txt','w',encoding='utf-8')
  # for i in range(1,page+1):
  #    page_num = str(i*20)


  response = requests.post(url, data={
        "params": get_params(json.dumps(data)),
        "encSecKey": get_encSecKey()
  },headers=headers).text
  print(response)
  print('爬虫结束了!!!!')




