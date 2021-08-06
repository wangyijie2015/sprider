#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/7/31 9:48
# software: PyCharm
import requests, random, re, os
from threading import Thread
def getUrl(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en-GB;q=0.7,en;q=0.6,ja;q=0.5',
        'Referer': url
    }
    contId = url.split('_')[-1]
    mrd = '%.16f' % random.random()
    jspurl = f'https://www.pearvideo.com/videoStatus.jsp?contId={contId}&mrd={mrd}'
    res = requests.get(jspurl, headers=headers).json()
    srcUrl = res['videoInfo']['videos']['srcUrl']
    src = re.sub(r'\d{13}', f'cont-{contId}', srcUrl)
    videoDown(contId, src)
    return

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    }
    url = 'https://www.pearvideo.com/'
    res = requests.get(url, headers=headers).content.decode()
    # print(res)
    urlList = re.findall(r'video_\d{7}', res)
    print(urlList)
    works = []
    for videoUrl in urlList:
        baseUrl = 'https://www.pearvideo.com/' + videoUrl
        # getUrl(baseUrl)
        work = Thread(target=getUrl, args=(baseUrl, ))
        work.start()
        works.append(work)
    for work in works:
        work.join()
    print('所有视频下载完毕')


def videoDown(name, url):
    try:
        type = url.split('.')[-1]
        if f'{name}.{type}' in os.listdir('./videos'):
            print(f'{name}.{type}已下载')
            return
        content = requests.get(url).content
        with open(f'./videos/{name}.{type}', 'wb') as f:
            f.write(content)
            print(f'视频{name}.{type}下载完成！')
    except Exception:
        print('视频下载失败')


if __name__=='__main__':
    if not os.path.exists('./videos'):
        os.mkdir('./videos')
    main()