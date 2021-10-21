"""
:调用爬虫
@author: lingzhi
* @date 2021/10/10 15:36
"""
import time
from spiders.google_curl import google_spider

test_tag = [
            '吴亦凡','河南', '奥运','大连', '郑州', '塔利班', '谭维维','钱枫', '吴亦凡', '陈平',
            '中国移动', '台积电', '三星', '万达', 'Trump', 'Biden', 'NLP', 'steam', 'Colab', '山西怀仁',
            '台湾', '外交', '邱少云郑爽林培瑞', '航母', '人民日报最高人民检查院', '广东', 'zhouyutong', 'feel',
            '董建华', '仪式', '江西', '电商', '合作社', '宝妈',
]
google_spider(test_tag)
