from cgitb import text
import scrapy, json
from .logger_me import custom_log
from urllib.parse import urlencode


class SpSpider(scrapy.Spider):
    name = "sp"
    allowed_domains = ["emalls.ir"]
    start_urls = ["https://emalls.ir/%D9%85%D8%B4%D8%AE%D8%B5%D8%A7%D8%AA_Samsung-Galaxy-S23-FE-8-256GB-Mobile-Phone~id~18644259~"]

    def start_requests(self):
       yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):  
        target_product_title = response.css("#ContentPlaceHolder1_H1TitleDesktop::text").get().strip()
        target_product_en_title = response.css("#form1 > div.main > div.container.top-detail > div.part-2 > div.product-title > div.name-en-kala::text").get().strip()
        target_product_price = response.css("#ContentPlaceHolder1_LblLessPrice::text").get().strip()
        target_product_url = response.url
        specs =response.css("#DivPartSpec > div.box-tab-custom.openable")
        specs = specs.css("div.info")
        specs_dict = {}
        for spec in specs:
            key = spec.css("div.info >span::text").get().strip()
            value = spec.css("div.info > span:last-of-type::text").get().strip()
            specs_dict[key] = value
            
        target_product_specs = json.dumps(specs_dict, ensure_ascii=False)
        product_id = response.url.split("~")[-2]

        product = {
            'product_id': product_id,
            'target_product_title': target_product_title,
            'target_product_en_title': target_product_en_title,
            'target_product_price': target_product_price,
            'target_product_url': target_product_url,
            'target_product_specs': target_product_specs
        }

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
            meta={"product": product},
            callback=self.similar_products_parse
            
        )
    
    def similar_products_parse(self, response):
        similars = json.loads(response.body)
        similars = [sim for sim in similars if sim["sort_price_val"] != "9999999999"]
        product_details = response.meta["product"]
        product_details["similars"] = similars
        yield product_details



























        # other suggested shops prices:
        # other_shops = response.css("#ContentPlaceHolder1_DivPartShops > div.shoplist")
        # similar_prices_by_shops = {}
        # for shop in other_shops:
        #     selector = "div.shop-row.exId-300366910.shoptype-1.special-shop > div.shop-logo-wrapper > span:nth-child(1) > a"
        #     shop_title = shop.css(f"{selector}::text").get().strip()
        #     product_url = response.css("#ContentPlaceHolder1_DivPartShops > div.shoplist > div.shop-row.exId-300366910.shoptype-1.special-shop > div.shop-prd-price > div.flx-berooz > div > span.shop-price.esrever::attr(href)").get().strip()
        #     price = response.css("#ContentPlaceHolder1_DivPartShops > div.shoplist > div.shop-row.exId-300366910.shoptype-1.special-shop > div.shop-prd-price > div.flx-berooz > div > span.shop-price.esrever::text").get().strip()
        #     shop_score = response.css("#ContentPlaceHolder1_DivPartShops > div.shoplist > div.shop-row.exId-258156676.shoptype-0.special-shop > div.shop-logo-wrapper > span:nth-child(1) > div > span.shop-rate.star-icon-gold.desktop.esrever > span::text").get().strip()
            
            
        #     similar_prices_by_shops[shop_title] = {
        #         "shop_titel": shop_title,
        #         "shop_url": product_url,
        #         "shop_price": price,
        #         "shop_score": shop_score
        #     }
        
        
        # yield similar_prices_by_shops
        
