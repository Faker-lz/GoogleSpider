# Google爬虫文档
## 一、配置

### 数据库配置

目前储存在MongoDB中，数据库配置在`setting.py ` 文件中15-19行，可自行修改。

```python
# MONGODB
MONGO_IP = "localhost"
MONGO_PORT = 27017
MONGO_DB = "Google_spider"
MONGO_USER_NAME = ""
MONGO_USER_PASS = ""
```



###  日志配置

`setting.py ` 文件中 125-135 行

```python
LOG_NAME = os.path.basename(os.getcwd())
LOG_PATH = "log/%s.log" % LOG_NAME  # log存储路径
LOG_LEVEL = "DEBUG"
LOG_COLOR = True  # 是否带有颜色
LOG_IS_WRITE_TO_CONSOLE = True # 是否打印到控制台
LOG_IS_WRITE_TO_FILE = True  # 是否写文件
LOG_MODE = "w"  # 写文件的模式
LOG_MAX_BYTES = 10 * 1024 * 1024  # 每个日志文件的最大字节数
LOG_BACKUP_COUNT = 20  # 日志文件保留数量
LOG_ENCODING = "utf8"  # 日志文件编码
OTHERS_LOG_LEVAL = "ERROR"  # 第三方库的log等级
```



### 爬虫配置

* 下载时间间隔

  * ```python
    SPIDER_SLEEP_TIME = [0, 1]
    ```

* 最大请求次数（默认100次）

  * ```python
    SPIDER_MAX_RETRY_TIMES = 100
    ```

  * 注：爬取过程中如遇到非法界面，会抛出`User-Agent --非法界面`的异常,之后该爬虫任务会重试直到爬取数据成功或超过100次

## 二、数据结构

| key     | description | value type | example                                                      |
| ------- | ----------- | ---------- | ------------------------------------------------------------ |
| title   | 标题        | str        | “孟晚舟事件”全解析：美国为何在错误道路上疯狂踩油门？ - 中新网 |
| keyword | 搜索关键字  | str        | "孟晚舟"                                                     |
| url     | 链接        | str        | http://www.chinanews.com/gj/2021/10-03/9579359.shtml         |
| text    | 内容        | str        | “孟晚舟事件”全解析：美国为何在错误道路上疯狂踩油门？ - 中新网7天前 · 2018年12月1日，加拿大应美国要求，以“涉嫌违反美国对伊朗制裁”为由，拘捕了华为创始人任正非长女、华为副董事长、首席财务官孟晚舟。2018年3月22日， ... |



## 三、调用方法

爬取关键词为`孟晚舟`的前`3`页内容

```python
from spiders.google_curl import GoogleCurl

spider = GoogleCurl('孟晚舟', 3)
spider.start()

```

* 第一个参数为搜索关键词,第二个参数为爬取页数

