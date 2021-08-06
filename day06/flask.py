#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:$汪贻杰
# datetime:2021/7/31 19:26
# software: PyCharm
from flask import Flask
import time

app =Flask(__name__)

@app.route('wangyijie')
def index_wangyijie():
    time.sleep(2)
    return 'Hello wangyijie'

@app.route('wangyu')
def index_wangyu():
    time.sleep(2)
    return 'hello wangyu'

@app.route('angongda')
def index_angongda():
    time.sleep(2)
    return 'hello angongda'

if __name__ == '__main__':
    app.run(threaded=True)

