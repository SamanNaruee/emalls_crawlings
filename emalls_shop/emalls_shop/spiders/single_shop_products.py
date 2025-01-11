import scrapy


class SingleShopProductsSpider(scrapy.Spider):
    name = "single_shop_products"
    allowed_domains = ["emalls.ir"]
    start_urls = ["https://emalls.ir"]

    def parse(self, response):
        pass
