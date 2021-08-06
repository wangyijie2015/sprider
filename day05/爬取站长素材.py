#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/7/30 9:25
# software: PyCharm
import requests
from lxml import etree
import os
import time
from requests.adapters import HTTPAdapter

if __name__ == '__main__':
    if not os.path.exists('./jianlimoban'):
        os.mkdir('./jianlimoban')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }

    url = 'https://sc.chinaz.com/jianli/free_%d.html'

    # for i in range(1,10):
    #     url ='https://sc.chinaz.com/jianli/free_%d.html%i'
    #     print(url)
    #     if i == 1:
    #         url = 'https://sc.chinaz.com/jianli/free_%d.html'
    #         print(url)
    page_text = requests.get(url=url,headers=headers).text

    tree = etree.HTML(page_text)
    div_list = tree.xpath('.//div[@id="main"]/div/div')



        #saveData(div_list)
        #实现访问模板概览页面，并进入下载页面，然后在存储的功能
        #访问页面，使用xpath，识别出模板名称，确定存储的路径
    def saveData(div_list):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'

        }
        for div in div_list:
            resume_src  = 'http'+div.xpath('./a/@herf')[0]
            resume_name  = div.xpath('./a/img/@alt')[0]+'.zip'
            #访问页面:
            detail_text  = requests.get(url=resume_src,headers=headers).text

            #xpath解析
            tree1 = etree.HTML(detail_text )
            download_src = tree1.xpath('//div[@class="clearfix mt20 downlist"]/ul/li[1]/a/@href')[0] #xpath得到的是一个列表

            #确定文件名称
            down_load_resume = requests.get(url=download_src, headers=headers).content
            down_load_path = 'resumelibs/' + resume_name

            with open(down_load_path,'wb') as fp:
                fp.write(down_load_resume)
                print(resume_name,'下载成功了！')

            # #确定存储的路径
            # jianli_path = './jianlimoban' + jianli_name

        # #超时重置的设置：
        #     # 超时重置的设置
        #     s = requests.Session()
        #     s.mount('http://', HTTPAdapter(max_retries=5))  # 这里是最大重试次数，重试5次，加最初一次，一共6次
        #     s.mount('https://', HTTPAdapter(max_retries=5))  # 两种访问，都要分别设置

        # #获取文件数据，进行持久化存储
        # jianli_data = s.get(url=url_li,headers=headers,timeout=10).content #timeout是超时的时间限制
        # #存储文件
        # with open(jianli_data,'wb') as fp:
        #     fp.write(jianli_data)
        #     print(jianli_name,'下载成功了！')
        # fp.close()
        # time.sleep(1) #睡眠一分钟后继续，针对反爬的演练