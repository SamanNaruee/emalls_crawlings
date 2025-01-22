import scrapy  
import json  
from .logger_me import custom_log
import datetime  


class EmallsApiSpider(scrapy.Spider):  
    name = "similars"  
    allowed_domains = ["emalls.ir"]  
    start_urls = ["https://emalls.ir"]  

    def __init__(self, shop_token, name = None, **kwargs):
        """
        To run this spider in terminal you should execute the following command:
        scrapy crawl similars -a shop_token=3273596
        Replace 3273596 with the shop_token you want to crawl.
        """
        super().__init__(name, **kwargs)
        self.token = shop_token

    def start_requests(self):  
        # Prepare the form data to be sent in the POST request  
        send_data = {  
            "entekhab": "listitemv2",  
            "currenturl": f"https://emalls.ir/%D9%84%DB%8C%D8%B3%D8%AA-%D9%82%DB%8C%D9%85%D8%AA~shop~{self.token}",
            "shop":str(self.token)
        }  
        
        yield scrapy.Request(  
            url=send_data["currenturl"],  
            callback=self.parse  
            
        )
        
    def parse(self, response): 
        custom_log("response", response)
        product = response.css(".product-block::text").get()
        custom_log("product", product)
        yield {
            'product_id': 'pass',
            'name': 'pass',
            'url': 'pass',
            'image_url': 'pass',
            'price': 'pass',
            'stores': 'pass',
            }

        # Pagination
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
