#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/7/31 10:23
# software: PyCharm
import random
import requests
from multiprocessing.dummy import Pool
import re
import os
from lxml import etree

if __name__ == '__main__':
  if not os.path.exists("./video"):
        os.mkdir("./video")
  headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'

  }
  #对下述的url发请求,解析出视频详情页的url和视频的名称
  url = 'https://www.pearvideo.com/category_4'
  page_text = requests.get(url=url,headers=headers).text

  tree = etree.HTML(page_text)
  li_list = tree.xpath('//ul[@id="listvideoListUl"]/li')

  #存储名字和地址的列表
  urls = [] #存储所有视频的连接和名字
  for li in li_list:
      # detail_id = li.xpath('./div/a/@href')[0]
      detail_url = 'https://www.pearvideo.com/'+li.xpath('./div/a/@href')[0]
      video_name = li.xpath('./div/a/div[2]/text()')[0]+'.mp4'
      detail_text = requests.get(url=detail_url, headers=headers).text
      headers = {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
          "Referer": detail_url
      }
      #从详情页中解析出视频的地址(url),返回的是一个列表，则列表中的第0个元素则为想要的结果
      cont_id = re.findall(r"_(.+)", detail_url)[0]
      params = {
          "contId": cont_id,
          "mrd": str(random.random())
      }
      url = "https://www.pearvideo.com/videoStatus.jsp"
      response = requests.get(url=url,headers=headers,params=params).json()
      src_url =response["videoInfo"]["videos"]["srcUrl"]
      src_url_list = src_url.split("/")
      src_url_list_last = src_url_list[-1]

      last_list = src_url_list_last.split("-")
      last_list[0]="cont-"+cont_id
      last = "-".join(last_list)
      src_url_list[-1] = last
      video_url = "/".join(src_url_list)
      dic = {
          "name":video_name,
          "url":video_url
      } #将name和视频的地址一起封装到存储在列表中，则定义一个字典
      urls.append(dic)

#使用线程池对所有视频数据进行请求（较为耗时的阻塞操作）
  def get_video_data(dic):
      headers = {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
      }
  url = dic["url"] #dic中的url取出
  data = requests.get(url=url,headers=headers).content
  with open("./video/"+dic["name"],"wb") as fp:
      fp.write(data)
      print(dic["name"],"视频缓存成功了！！！")

#原则:线程池处理的是阻塞且较为耗时的操作
  pool = Pool(4) #获取到的为4个视频
  pool.map(get_video_data,urls)
  pool.close()
  pool.join() #主线程等子线程结束后在结束

