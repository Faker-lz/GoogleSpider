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
from utils import get_random_user_agent, filter_link
import re


class GoogleCurl(feapder.AirSpider):
    def __init__(self, query: str = '', page_range: int = 3):
        self.page_range = page_range
        self.query = query
        self.pq_content = None
        self.data = list()
        super().__init__()

    def start_callback(self):
        db = MongoDB()
        db.delete(MonGO_TABLE, {'keyword': self.query})

    def download_midware(self, request):
        """
        Customize Download midware
        :param request:
        :return:
        """
        request.headers = {'User-Agent': get_random_user_agent(),
                           'Connection': 'close'}

    def start_requests(self):
        for page in range(self.page_range):
            if page == (self.page_range - 1):
                finish = True
            else:
                finish = False
            yield feapder.Request(
                "https://www.google.com/search?q={query}&start={start}".format(query=self.query, start=page * 10),
                finish=finish
            )

    def validate(self, request, response):
        content = response.content
        text = content.decode(cchardet.detect(content)['encoding'])
        judge_re = re.compile(r'[<](.*?)[>]', re.S)
        judge_text = re.findall(judge_re, text)[0]
        if 'Mobile' in judge_text:
            raise Exception('爬取到移动端界面!')
        self.pq_content = pq(text)

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
                    judge_date = re.match(r'\d{4}(年|-)\d{1,2}(月|-)\d{1,2}(日|)', span)
                    url_path = p('div').eq(1).text()
                    text = ppa('div').eq(6).text()
                    text = text.replace(url_path, '').replace('\n', '')
                    result['title'] = head
                    result['keyword'] = self.query
                    result['inserted_time'] = '2021-10-15'
                    result['created_time'] = judge_date.group() if judge_date else None
                    result['text'] = text
                    result_item = Item(**result)
                    result_item.table_name = MonGO_TABLE
                    yield result_item


if __name__ == "__main__":
    GoogleCurl('孟晚舟').start()
