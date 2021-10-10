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
from feapder.utils.log import log
import cchardet
from pyquery import PyQuery as pq
from utils import get_random_user_agent, filter_link


class GoogleCurl(feapder.AirSpider):
    def __init__(self, query: str = '', page_range: int = 3):
        self.page_range = page_range
        self.query = query
        super().__init__()

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
            yield feapder.Request(
                "https://www.google.com/search?q={query}&start={start}".format(query=self.query, start=page * 10))

    def parse(self, request, response):
        content = response.content
        charset = cchardet.detect(content)
        text = content.decode(charset['encoding'])
        pq_content = pq(text)
        result_list = list()
        print(request)

        for p in pq_content.items('a'):
            if p.attr('href').startswith('/url?q='):
                pa = p.parent()
                ppa = pa.parent()
                if ppa.attr('class') is not None:
                    result = dict()
                    head = p('h3').eq(0).text()
                    head_text = p.text()
                    result['title'] = head if head else head_text
                    if result['title'] == '了解详情':
                        log.error(request.headers['User-Agent']+'--非法页面')
                        raise Exception(request.headers['User-Agent']+'--非法页面')
                    elif result['title'] == '':
                        continue
                    result['keyword'] = self.query
                    result['url_path'] = p('div').eq(1).text()
                    href = p.attr('href')
                    if href:
                        url = filter_link(href)
                        result['url'] = url
                    text = ppa('div').eq(0).text()
                    text = text.replace(result['url_path'], '').replace('\n', '')
                    result['text'] = text
                    result.pop('url_path')
                    result_item = Item(**result)
                    result_item.table_name = 'spider_data'
                    result_list.append(result)
                    yield result_item


if __name__ == "__main__":
    GoogleCurl('孟晚舟').start()