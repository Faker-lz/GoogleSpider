"""
:调用爬虫
@author: lingzhi
* @date 2021/10/10 15:36
"""

from spiders.google_curl import GoogleCurl

spider = GoogleCurl('Trump', 3)
spider.start()
