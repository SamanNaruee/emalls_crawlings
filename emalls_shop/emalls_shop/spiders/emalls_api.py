import scrapy  
import json  

class EmallsApiSpider(scrapy.Spider):  
    name = "emalls_api"  
    allowed_domains = ["emalls.ir"]  
    start_urls = ["https://emalls.ir/_Search.ashx"]  

    def start_requests(self):  
        # Prepare the form data to be sent in the POST request  
        form_data = {  
            "entekhab": "listitemv2",  
            "currenturl": "https://emalls.ir/%D9%84%DB%8C%D8%B3%D8%AA-%D9%82%DB%8C%D9%85%D8%AA~shop~21766",  
            "shop": "21766"  
        }  
        
        # Send a POST request with the form data  
        yield scrapy.FormRequest(  
            url=self.start_urls[0],  
            method='POST',  
            formdata=form_data,  
            callback=self.parse  
        )  

    def parse(self, response):  
        # Load the JSON data from the response  
        data = json.loads(response.body)  
        data = data.get('lstsearchresualt', [])
        product1 = data[0]
        print(product1)
        yield product1
        # Process the JSON data (example: extracting product information)  
        # for product in data.get('lstsearchresualt', []):  # Assuming 'products' is a key in the JSON  
        #     yield {  
        #         'name': product.get('name'),  
        #         'price': product.get('price'),  
        #         'link': product.get('link'),  
        #         # Add other fields as necessary  
        #     }
