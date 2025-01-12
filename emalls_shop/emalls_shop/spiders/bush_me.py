import scrapy


class BushMeSpider(scrapy.Spider):
    name = "bush_me"
    allowed_domains = ["emalls.ir"]
    start_urls = ["https://emalls.ir/Shop/35316"]

    def parse(self, response):
        pass
