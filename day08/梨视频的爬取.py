#梨视频的爬取
import os

import requests
if __name__ == '__main__':
    #1.拿到contId
    #2.拿到vidoStatus返回的json --> srcURL
    #3.srcURL里面的内容休整
    #4.下载视频
    if not os.path.exists('./lishiping'):
       os.mkdir('./lishiping')
    url = 'https://www.pearvideo.com/video_1737828'
    coutId = url.split("_")[1]

    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        #防盗链:溯源，当前本次请求的上一级是谁
         "Referer":url
    }

    vidooStatusUrl = 'https://www.pearvideo.com/videoStatus.jsp?contId=1737828&mrd=0.2927037982720271'
    response = requests.get(url=vidooStatusUrl,headers=headers)
    # print(response.text)
    dic = response.json()
    srcUrl = dic['videoInfo']['videos']['srcUrl']
    systemTime = dic['systemTime']
    srcUrl = srcUrl.replace(systemTime,f"cont-{coutId}")
    # print(srcUrl)
    #请求得到的url

    #真实的url    https://video.pearvideo.com/mp4/adshort/20210805/cont-1737828-15739290_adpkg-ad_hd.mp4
    #请求得到的url:https://video.pearvideo.com/mp4/adshort/20210805/1628228181017-15739290_adpkg-ad_hd.mp4
    #下载视频
    with open("./lishiping/li.mp4",mode='wb') as fp:
        fp.write(requests.get(srcUrl).content)
    fp.close()