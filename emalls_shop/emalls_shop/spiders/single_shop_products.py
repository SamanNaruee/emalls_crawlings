import scrapy
import json
from ..items import EmallsShopItems

def generate_token():
    return '21766'

class SingleShopProductsSpider(scrapy.Spider):
    name = "single_shop_products"
    allowed_domains = ["emalls.ir"]
    start_urls = [f"https://emalls.ir/%D9%84%DB%8C%D8%B3%D8%AA-%D9%82%DB%8C%D9%85%D8%AA~shop~{generate_token()}"]

    def parse(self, response):
        item = EmallsShopItems()
        item['products'] = []

        products = response.css('div.product-block-parent > div.item.product-block')

        for product in products:
            product_info = {
                'name': product.css('div.item-title a::attr(title)').get(),
                'url': response.urljoin(product.css('div.item-title a::attr(href)').get()),
                'image_url': product.css('div.prd-ax a img::attr(src)').get(),
                'store_count': product.css('a.btn-see span.icon::text').get(),
                'price': product.css('div.prd-price span::text').get()
            }
            item['products'].append(product_info)

        item['token'] = generate_token()
        yield item

