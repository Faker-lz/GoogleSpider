"""
:调用爬虫
@author: lingzhi
* @date 2021/10/10 15:36
"""

from spiders.google_curl import GoogleCurl

spider = GoogleCurl('中国移动', 3)
spider.start()
# spider2 = GoogleCurl('孟晚舟', 3)
# spider2.start()
