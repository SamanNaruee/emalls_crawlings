import scrapy, json
from .logger_me import custom_log


class SpSpider(scrapy.Spider):
    name = "sp"
    allowed_domains = ["emalls.ir"]
    start_urls = ["https://emalls.ir/%D9%85%D8%B4%D8%AE%D8%B5%D8%A7%D8%AA_Samsung-Galaxy-S23-FE-8-256GB-Mobile-Phone~id~18644259~"]

    def start_requests(self):
       yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):  
        target_product_title = response.css("#ContentPlaceHolder1_H1TitleDesktop::text").get().strip()
        # Step 1: Navigate to the specific element containing shop listings  
        # Using the selector. The element is not directly used unless you need specific data from it.  
        element = response.css('#ContentPlaceHolder1_DivPartShops').get()  
        
        # Step 2: Navigate to the shop list  
        shop_list = response.css('#ContentPlaceHolder1_DivPartShops > div.shoplist')  

        # Step 3: Iterate through each shop-row inside the shop list  
        for shop in shop_list.css('div.shop-row'):  
            shop_id = shop.attrib.get('data-shopid')  # Getting data-shopid if it exists  
            shop_name = shop.css('span.shop-name::text').get(default='N/A').strip()  # Name of the shop  
            price = shop.css('span.shop-price::text').get(default='N/A').strip()  # Price of the shop  
            
            yield {  
                'shop_id': shop_id,  
                'shop_name': shop_name,  
                'price': price,  
            }  
        
        # If there are more pages to navigate, implement pagination here  
        next_page = response.css('#ContentPlaceHolder1_DivPartShops a.next::attr(href)').get()  
        if next_page:  
            yield response.follow(next_page, self.parse)  
