"""
:调用爬虫
@author: lingzhi
* @date 2021/10/10 15:36
"""
import time
start = time.time()
from spiders.google_curl import GoogleCurl
test_tag = [
            '吴亦凡','河南', '奥运',
            '大连', '郑州', '塔利班', '吴亦凡',
            '钱枫', '吴亦凡', '陈平', '山西怀仁',
]
for tag in test_tag:
    spider = GoogleCurl(tag, 8)
    spider.start()