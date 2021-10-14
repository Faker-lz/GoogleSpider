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


class GoogleCurl(feapder.AirSpider):
    def __init__(self, query: str = '', page_range: int = 3):
        self.page_range = page_range
        self.url = "https://{domain}/search?q={query}&start={start}"
        self.query = query
        self.pq_content = None
        super().__init__()

    def start_callback(self):
        db = MongoDB()
        db.get_collection(MonGO_TABLE).delete_many({'keyword': self.query})

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
        for page in range(self.page_range):
            yield feapder.Request(
                self.url.format(domain=get_domain(), query=self.query, start=page * 10), page=page*10
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
            request.url = self.url.format(domain=get_domain(), query=self.query, start=request.page)
            raise Exception('请求错误!')        # 改变Google 服务器地址后重新爬取

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
                    judge_date_cn = re.match(r'\d{4}(年|-)\d{1,2}(月|-)\d{1,2}(日|)', span)
                    judge_date_en = re.match(r'\d{1,2} [a-zA-Z]{3} \d{4}', span)
                    url_path = p('div').eq(1).text()
                    text = ppa('div').eq(6).text()
                    text = text.replace(url_path, '').replace('\n', '')
                    result['title'] = head
                    result['keyword'] = self.query
                    result['inserted_time'] = '2021-10-15'
                    result['created_time'] = span if judge_date_cn or judge_date_en else None
                    result['text'] = text
                    result_item = Item(**result)
                    result_item.table_name = MonGO_TABLE
                    yield result_item



if __name__ == "__main__":
    GoogleCurl('孟晚舟').start()