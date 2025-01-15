import scrapy
import json


class GetAllShopIdSpider(scrapy.Spider):
    name = "get_all_shop_ID"
    allowed_domains = ["emalls.ir"]
    start_urls = ["https://emalls.ir/Shops/"]
    current_shops = []

    def parse(self, response):
        for i in range(0, 48):
            shop_type = response.css(f'#ContentPlaceHolder1_rptShops_LblShopType_{i}::text').get()
            shop_id = response.css(f'#ContentPlaceHolder1_rptShops_LblShopId_{i}::text').get()
            if shop_type:
                self.logger.info(f"Shop Type: {shop_type}")
                self.logger.info(f'shop id: {shop_id}')
                self.current_shops.append((shop_id, shop_type))
        with open('current_shops_ids.json', 'w', encoding='utf-8') as f:
            json.dump(self.current_shops, f, ensure_ascii=False, indent=4)
        
