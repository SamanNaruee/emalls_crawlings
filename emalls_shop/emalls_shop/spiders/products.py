from argparse import RawDescriptionHelpFormatter
from operator import truediv
import scrapy, json
from urllib.parse import urlencode
from .logger_me import custom_log

class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["emalls.ir"]
    start_urls = [f"https://emalls.ir/%D9%84%DB%8C%D8%B3%D8%AA-%D9%82%DB%8C%D9%85%D8%AA~shop~2292"]
    
    def __init__(self, token, name: str | None = None, **kwargs: any):
        super().__init__(name, **kwargs)
        self.token = token
        
    def start_requests(self):
        pagenum = 1
        form_data = {
            "entekhab": "listitemv2",
            "currenturl": f"https://emalls.ir/%d9%84%db%8c%d8%b3%d8%aa-%d9%82%db%8c%d9%85%d8%aa~shop~{self.token}",
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

        yield scrapy.Request(
            url="https://emalls.ir/_Search.ashx",
            callback=self.parse,
            headers=headers,
            body=urlencode(form_data),
            method="POST",
            meta={'shop_token': self.token, 'pagenum': pagenum},
            dont_filter=True
        )


    def parse(self, response):
        data = json.loads(response.body)
        data = data['lstsearchresualt']
        custom_log(data)


        next_page = None
        while True:
            if not next_page:
                break
            
