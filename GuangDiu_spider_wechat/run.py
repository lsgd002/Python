#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   run.py
@Time    :   2023/05/27 21:56:45
@Author  :   lsgd002 
@Version :   1.0
@Desc    :   执行文件，已生成.exe文件
'''


import schedule
import time

from gd_spider_wechat import get_gd_item

# 定义关键字
keyword = '三元极致'
count = 0
print(f" {keyword} 爬取+推送开始运行...(每小时运行一次)")

def job():
    global count
    get_gd_item(keyword)
    count += 1

    next_run = schedule.next_run()
    if next_run is not None:
        next_run_str = next_run.strftime("%Y-%m-%d %H:%M:%S")
    else:
        next_run_str = "None"

    print(f'运行中...已运行{count}次，下次运行时间：{next_run_str}')

# 每小时执行一次
# schedule.every().minutes.at(':01').do(job)
schedule.every().hour.at(':01').do(job)   
while True:
    schedule.run_pending() # 运行所有可以运行的任务
    time.sleep(1) 