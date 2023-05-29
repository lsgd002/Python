#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   gd_spider_wechat.py
@Time    :   2023/05/27 15:37:39
@Author  :   lsgd002 
@Version :   1.0
@Desc    :   爬取逛丢【*】的信息并微信推送(Server酱)
'''

import requests
from scrapy.selector import Selector


def get_gd_item(keyword):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'
    }

    gd_url = f'https://guangdiu.com/search.php?q={keyword}'
    response = requests.get(url=gd_url, headers=headers)
    response.encoding = 'utf-8'

    selector = Selector(response)

    title = selector.xpath(  # 标题
        '//*[@id="mainleft"]/div[4]/div/div[2]/h2/a/text()').extract_first()
    price = selector.xpath(  # 价格
        '//*[@id="mainleft"]/div[4]/div/div[2]/h2/a/span/text()').extract_first()
    shop = selector.css(  # 店铺
        '#mainleft > div.zkcontent > div:nth-child(1) > div.rightlinks > div.rightmall > a::text').extract_first()
    goods_filter = selector.css(  # 分类
        '#mainleft > div.zkcontent > div:nth-child(1) > div.rightlinks > div.rightmall > span::text').extract_first()
    last_time = selector.css(  # 最后更新时间 < 1小时
        '#mainleft > div.zkcontent > div:nth-child(1) > div.iteminfoarea > div.timeandfrom > div > a > span::text').extract_first()
    last_time2 = selector.css(  # 最后更新时间 > 1小时
        '#mainleft > div.zkcontent > div:nth-child(1) > div.iteminfoarea > div.timeandfrom > div > a::text').extract_first()
    
    title, price, shop, goods_filter, last_time, last_time2 = map(lambda x: x.strip() 
                                                                  if x is not None else None, 
                                                                  [title, price, shop, goods_filter, last_time, last_time2])

    item = [i.strip() if i is not None else '' 
            for i in [title, price, shop, goods_filter, last_time, last_time2]]
    print(item)

    # 写入本次的item[0]，item[0]为标题
    with open('./gd_item.txt', 'w', encoding='utf-8') as f:
        f.write(item[0])

    # 对比两次标题是否相同，相同则不推送
    # 读取上次的item[0]
    with open('./gd_item.txt', 'r', encoding='utf-8') as f:
        last_item = f.read()
        print('上次标题：' + last_item)

    # 写入本次的item[0]
    with open('./gd_item.txt', 'w', encoding='utf-8') as f:
        f.write(item[0])
        print('本次标题：' + item[0])

    # 判断是否推送
    if item[0] == last_item:
        print('不推送')
    else:
        print('开始推送...')
        # Sever酱推送
        SCKEY = 'SCT211433TzCZcehqfmjJj7UVNz4oxXhMv'
        url = 'https://sctapi.ftqq.com/' + SCKEY + '.send'
        data = {'text': item[0], 'desp': str(item)}  # desp为消息内容,text为消息标题
        response = requests.post(url, data=data)
        print('推送完成')
    return item

#     print('开始推送')
#     # Sever酱推送
#     SCKEY = 'SCT211433TzCZcehqfmjJj7UVNz4oxXhMv'
#     url = 'https://sctapi.ftqq.com/' + SCKEY + '.send'
#     data = {'text': item[0], 'desp': str(item)}  # desp为消息内容,text为消息标题
#     response = requests.post(url, data=data)
#     print('推送完成')
#     return item

# get_gd_item('三元极致')