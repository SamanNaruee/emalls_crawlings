from argparse import RawDescriptionHelpFormatter
from operator import truediv
import scrapy, json
from urllib.parse import urlencode
from .logger_me import custom_log
from memory_profiler import profile
from colorama import Fore


class ProductsSpider(scrapy.Spider):
    """
    Usage:
        scrapy crawl products -o all_products_of_a_shop.json -a token=50590
    """
    custom_settings = {
        'RETRY_ENABLED': True,  
        'RETRY_TIMES': 3,
        'DOWNLOAD_DELAY': 0.8,                     # 50 milisecond delay between requests
        'CONCURRENT_REQUESTS': 12,                  # max number of concurrent requests on all domains
        'DOWNLOAD_TIMEOUT': 60,                     # max time in second to wait for a response
        'REACTOR_THREADPOOL_MAXSIZE': 10,           # max size of twisted reactor thread pool
        'LOG_LEVEL': 'INFO',                        # level of logging detail ((DEBUG, INFO, WARNING, ERROR, CRITICAL)): less termnal output
        'COOKIES_ENABLED': False,                   # disable cookie handling to reduce overhead
        'RETRY_ENABLED': False,                     # disable automatic retry of failed requests
        'DOWNLOAD_FAIL_ON_DATALOSS': False,         # handle fail of incomplete responses
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.25,           # initial delay
        'AUTOTHROTTLE_MAX_DELAY': 1,              # max delay
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,     # target concurrency
        'DOWNLOADER_MIDDLEWARES': {  
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  
            'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,  
        }, 
    }
    
    
    name = "products"
    allowed_domains = ["emalls.ir"]
    start_urls = [f"https://emalls.ir/%D9%84%DB%8C%D8%B3%D8%AA-%D9%82%DB%8C%D9%85%D8%AA~shop~2292"]
    
    def __init__(self, token, name: str | None = None, **kwargs: any):
        super().__init__(name, **kwargs)
        self.token = token
        self.stop_crawling = False

    @profile
    def start_requests(self):
        pagenum = 200
        while not self.stop_crawling:
            form_data = {
                "entekhab": "listitemv2",
                "currenturl": f"https://emalls.ir/%d9%84%db%8c%d8%b3%d8%aa-%d9%82%db%8c%d9%85%d8%aa~shop~{self.token}~page~{pagenum}",
                "pagenum": str(pagenum),
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
        # check if a page does not exist.
        if not data or not data['lstsearchresualt']:
            custom_log(f"Does not find any product in this page: {response.meta['pagenum']}")
            self.stop_crawling = True
            return None

        products = data['lstsearchresualt']
        for product in products:
            product_start_url = f"https://emalls.ir/{product['link']}"  
            product_data = {
                'product_id': product['id'],
                'product_link': product_start_url,
                'product_details': {},
            }
            yield scrapy.Request(
                url=product_start_url,
                callback=self.parse_product,
                meta={'product': product_data},
            )

    @profile
    def parse_product(self, response):
        target_product_title = response.css("#ContentPlaceHolder1_H1TitleDesktop::text").get()
        target_product_title = target_product_title.strip() if target_product_title is not None else None

        target_product_en_title = response.css("#form1 > div.main > div.container.top-detail > div.part-2 > div.product-title > div.name-en-kala::text").get()
        target_product_en_title = target_product_en_title.strip() if target_product_en_title is not None else None

        target_product_price = response.css("#ContentPlaceHolder1_LblLessPrice::text").get()
        target_product_price = target_product_price.strip() if target_product_price is not None else None
        target_product_url = response.url
        specs =response.css("#DivPartSpec > div.box-tab-custom.openable")
        specs = specs.css("div.info")
        specs_dict = {}
        for spec in specs:
            key = spec.css("div.info >span::text").get()
            key = key.strip() if key is not None else None
            value = spec.css("div.info > span:last-of-type::text").get()
            value = value.strip() if value is not None else None
            specs_dict[key] = value
            
        target_product_specs = json.dumps(specs_dict, ensure_ascii=False)
        product_id = response.url.split("~")[-1]

        product_data = response.meta["product"]

        product_data.update({
            'product_id': product_id,
            'target_product_title': target_product_title,
            'target_product_en_title': target_product_en_title,
            'target_product_price': target_product_price,
            'target_product_url': target_product_url,
            'target_product_specs': target_product_specs
        })

        # To get all data from FormData:
        FormData = {
            "id": product_id,
            "startfrom": 11
        }
                
        yield scrapy.Request(
            url="https://emalls.ir/swservice/webshopproduct.ashx",
            method="POST",
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            body=urlencode(FormData),
            meta={"product": product_data},
            callback=self.similar_products_parse
            
        )
    
    @profile
    def similar_products_parse(self, response):
        product = response.meta["product"]
        
        similars = json.loads(response.body)
        similars = [sim for sim in similars if sim["sort_price_val"] != "9999999999"]
        product['product_details']['similars'] = similars
        yield product
