import scrapy


class OnlyShopsSpider(scrapy.Spider):
    name = "only_shops"
    allowed_domains = ["emalls.ir"]
    start_urls = ["https://emalls.ir/Shops/"]

    def parse(self, response):
        pass
