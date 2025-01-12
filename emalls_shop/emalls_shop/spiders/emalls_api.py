import scrapy


class EmallsApiSpider(scrapy.Spider):
    name = "emalls_api"
    allowed_domains = ["emalls.ir"]
    start_urls = ["https://emalls.ir/_Search.ashx"]

    def parse(self, response):
        pass
