from operator import truediv
import scrapy
from .logger_me import custom_log

class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["emalls.ir"]
    start_urls = [f"https://emalls.ir/%D9%84%DB%8C%D8%B3%D8%AA-%D9%82%DB%8C%D9%85%D8%AA~shop~2292"]
    
    def __init__(self, token, name: str | None = None, **kwargs: any):
        super().__init__(name, **kwargs)
        self.token = token
        
    def start_requests(self):
        yield scrapy.Request(
            url=f"https://emalls.ir/%D9%84%DB%8C%D8%B3%D8%AA-%D9%82%DB%8C%D9%85%D8%AA~shop~{self.token}",
            callback=self.parse,
        )


    def parse(self, response):
        custom_log(response.css("#mainlist > div.paging-wrapper > a.paging_number.paging_hyperlink.page-next::attr(href)").get())
        
        while True:
            # there is no next page
            
            pass
