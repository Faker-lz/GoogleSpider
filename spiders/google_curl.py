# -*- coding: utf-8 -*-
"""
Created on 2021-10-10 10:45:14
---------
@summary:
---------
@author: wlz
"""

import feapder
from feapder import Item
from feapder.db.mongodb import MongoDB
from setting import MonGO_TABLE
import cchardet
from pyquery import PyQuery as pq
from utils import get_random_user_agent, filter_link, get_domain
import re
import time
import datetime


class GoogleCurl(feapder.AirSpider):
    def __init__(self, query_list: list, page_range: int = 3):
        self.page_range = page_range
        self.url = "https://{domain}/search?q={query}&start={start}"
        self.query_list = query_list
        self.pq_content = None
        super().__init__()

    def start_callback(self):
        """
        Mark old data
        """
        for query in self.query_list:
            db = MongoDB()
            db.get_collection(MonGO_TABLE).update_many({
                'keyword': query,
            },
                {'$set': {'flag': 'old'
                          }
                 }
            )

    def download_midware(self, request):
        """
        Customize Download midware
        :param request:
        :return:
        """
        # request.proxies = {
        #     "http": "http://3.211.65.185:80",
        #     "https": "https://10.245.142.209:1089"
        # }
        request.headers = {'User-Agent': get_random_user_agent(),
                           'Connection': 'close'}

    def start_requests(self):
        for query in self.query_list:
            for page in range(self.page_range):
                yield feapder.Request(
                    self.url.format(domain=get_domain(), query=query, start=page * 10), page=page*10, query=query
                )

    def validate(self, request, response):
        content = response.content
        text = content.decode(cchardet.detect(content)['encoding'])
        self.pq_content = pq(text)
        judge_re = re.compile(r'[<](.*?)[>]', re.S)
        judge_text = re.findall(judge_re, text)[0]
        if 'Mobile' in judge_text:
            raise Exception('非法界面!')
        if response.status_code != 200:
            request.url = self.url.format(domain=get_domain(), query=request.query, start=request.page)
            raise Exception('请求错误!')        # 改变Google 服务器地址后重新爬取
        elif response.status_code == 429:
            time.sleep(60)                     # 检测到最大连接数,等待1分钟


    def parse(self, request, response):
        for p in self.pq_content.items('a'):
            if p.attr('href').startswith('/url?q='):
                pa = p.parent()
                ppa = pa.parent()
                if ppa.attr('class') is not None:
                    result = dict()
                    head = p('h3').eq(0).text()
                    if head is None or head == '':
                        continue
                    href = p.attr('href')
                    if href:
                        url = filter_link(href)
                        result['url'] = url
                    span = ppa('span').eq(0).text()
                    judge_date = re.match(r'([[a-zA-Z]{3}|\d{1,2}|\d{4}])(年|-|\s)([a-zA-Z]*?'
                                          r'|\d{1,2})(,*?)(\s|月|-|)(|\d{4}|\d{1,2})(日|ago|)\s', span)
                    url_path = p('div').eq(1).text()
                    text = ppa('div').eq(6).text()
                    text = text.replace(url_path, '').replace('\n', '')
                    result['title'] = head
                    result['keyword'] = request.query
                    result['inserted_time'] = datetime.datetime.now()
                    result['created_time'] = span if judge_date else None
                    result['text'] = text
                    result['flag'] = 'new'
                    result_item = Item(**result)
                    result_item.table_name = MonGO_TABLE
                    yield result_item

    def end_callback(self):
        """
        delete old data
        """
        db = MongoDB()
        for query in self.query_list:
            db.get_collection(MonGO_TABLE).delete_many({'keyword': query, 'flag': 'old'})


if __name__ == "__main__":
    keywords = ['Trump', 'Biden', 'NLP']
    spider = GoogleCurl(keywords, 3)
    spider.start()
