from argparse import RawDescriptionHelpFormatter
from operator import truediv
import scrapy, json
from urllib.parse import urlencode
from .logger_me import custom_log
from memory_profiler import profile


class ProductsSpider(scrapy.Spider):
    """
    Usage:
        scrapy crawl products -o output.csv -a token=954
    """
    custom_settings = {
        'DOWNLOAD_DELAY': 0.05,                     # 50 milisecond delay between requests
        'CONCURRENT_REQUESTS': 12,                  # max number of concurrent requests on all domains
        'DOWNLOAD_TIMEOUT': 35,                     # max time in second to wait for a response
        'REACTOR_THREADPOOL_MAXSIZE': 10,           # max size of twisted reactor thread pool
        'LOG_LEVEL': 'INFO',                        # level of logging detail ((DEBUG, INFO, WARNING, ERROR, CRITICAL)): less termnal output
        'COOKIES_ENABLED': False,                   # disable cookie handling to reduce overhead
        'RETRY_ENABLED': False,                     # disable automatic retry of failed requests
        'DOWNLOAD_FAIL_ON_DATALOSS': False,         # handle fail of incomplete responses
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.05,           # initial delay
        'AUTOTHROTTLE_MAX_DELAY': 0.5,              # max delay
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,     # target concurrency
    }
    
    
    name = "products"
    allowed_domains = ["emalls.ir"]
    start_urls = [f"https://emalls.ir/%D9%84%DB%8C%D8%B3%D8%AA-%D9%82%DB%8C%D9%85%D8%AA~shop~2292"]
    
    def __init__(self, token, name: str | None = None, **kwargs: any):
        super().__init__(name, **kwargs)
        self.token = token

    @profile
    def start_requests(self):
        pagenum = 2
        while True:
            form_data = {
                "entekhab": "listitemv2",
                "currenturl": f"https://emalls.ir/%d9%84%db%8c%d8%b3%d8%aa-%d9%82%db%8c%d9%85%d8%aa~shop~{self.token}~page~{pagenum}",
                "attfilters":  "",
                "minprice": "0",
                "maxprice": "0",
                "brandid": "0",
                "findstr":  "",
                "pagenum": str(pagenum),
                "exist":  "",
                "shop": self.token
            }
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

            request = scrapy.Request(
                url="https://emalls.ir/_Search.ashx",
                callback=self.parse,
                headers=headers,
                body=urlencode(form_data),
                method="POST",
                meta={'shop_token': self.token, 'pagenum': pagenum},
                dont_filter=True
            )
            pagenum += 1
            yield request

    @profile
    def parse(self, response):
        data = json.loads(response.body)
        custom_log(data)
        # check if a page does not exist.
        if not data or not data['lstsearchresualt']:
            custom_log(f"Does not find any product in this page: {response.meta['pagenum']}")
            return None

        products = data['lstsearchresualt']
        yield products
