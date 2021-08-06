#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/7/31 10:10
# software: PyCharm
import time
#使用线程池对应的类
from multiprocessing.dummy import  Pool

if __name__ == '__main__':
    start_time = time.time()
    def get_page(str):
        print("正在下载:",str)
        time.sleep(2)
        print('下载成功:',str)
name_list = ['xiaozi','aa','bb','cc']

#实例化一个线程池对象:
pool =Pool(4)
#将列表中每一个列表元素传递给get_page处理
pool.map(get_page,name_list)

end_time = time.time()
print(end_time-start_time)
