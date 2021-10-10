# GoogleSpider

Crawl the information of a given keyword on Google search engine

## Config

### DataBase

Currently, data is stored in mongodb, and the database configuration is in line 15-19 of the `setting. py` file, which can be modified by yourself.

```python
# MONGODB
MONGO_IP = "localhost"
MONGO_PORT = 27017
MONGO_DB = "Google_spider"
MONGO_USER_NAME = ""
MONGO_USER_PASS = ""
```



###  Log

```python
LOG_NAME = os.path.basename(os.getcwd())
LOG_PATH = "log/%s.log" % LOG_NAME  # log path
LOG_LEVEL = "DEBUG"
LOG_COLOR = True  
LOG_IS_WRITE_TO_CONSOLE = True 
LOG_IS_WRITE_TO_FILE = True  
LOG_MODE = "w" 
LOG_MAX_BYTES = 10 * 1024 * 1024  # Maximum bytes
LOG_BACKUP_COUNT = 20  # Number of log files reserved
LOG_ENCODING = "utf8"  # code
OTHERS_LOG_LEVAL = "ERROR"  # leval
```



### Spider

* Download interval

  * ```python
    SPIDER_SLEEP_TIME = [0, 1]
    ```

* Maximum number of requests (100 by default)

  * ```python
    SPIDER_MAX_RETRY_TIMES = 100
    ```

    > Note
    >
    > If an illegal interface is encountered during crawling, an exception of 'user agent -- illegal interface' will be thrown, and then the crawler task will retry until the data is successfully crawled or more than 100 times
    



## data structure

| key     | value type | example                                                      |
| ------- | ---------- | ------------------------------------------------------------ |
| title   | str        | “Donald Trump - Wikipedia”                                   |
| keyword | str        | “Trump"                                                      |
| url     | str        | "https://en.wikipedia.org/wiki/Donald_Trump"                 |
| text    | str        | Donald Trump - Wikipedia 1 hour ago · Donald John Trump (born June 14, 1946) is an American politician, media personality, and businessman who served as the 45th president of the United States ... Vice President: Mike Pence In office January 20, 2017 – January 20, 2021: In office; January 20, 2017 – January 20, 2021 Occupation: Politician; businessman; television presenter Parents: Fred Trump; Mary Anne MacLeod" |



## Quick start

Crawl the `3` page data with the keyword 'Trump'

```python
from spiders.google_curl import GoogleCurl

spider = GoogleCurl('Trump', 3)
spider.start()

```

* The first parameter is the search keyword, and the second parameter is the number of pages crawled

