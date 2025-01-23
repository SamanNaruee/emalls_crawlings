import token
import scrapy


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["emalls.ir"]
    start_urls = [f"https://emalls.ir/%D9%84%DB%8C%D8%B3%D8%AA-%D9%82%DB%8C%D9%85%D8%AA~shop~{self.token}"]
    
    def __init__(self, token, name: str | None = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        self.token = token
        
    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
        )


    def parse(self, response):
        pass
