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
        
        for page in range(1, 6):  
            form_data["currenturl"] += f"~page~{page}"  

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
        products = []   
        for product in data:
            sent_product = {
                'id': product.get('id'),  
                'title': product.get('title'),  
                'titlefa': product.get('titlefa'),  
                'link': product.get('link'),  
                'image': product.get('image'),  
                'category': product.get('category'),  
                'rate': product.get('rate'),  
                'offcount': product.get('offcount'),  
                'price': product.get('price'),  
                'pprice': product.get('pprice'),  
                'discountpercent': product.get('discountpercent'),  
                'maxprice': product.get('maxprice'),  
                'lupdate': product.get('lupdate'),  
                'buyTitle': product.get('buyTitle'),  
                'buyLink': product.get('buyLink'),  
                'spec': product.get('spec'),  
                'used': product.get('used'),                  
            }
            
            products.append(sent_product)
        yield {
            'products': products,
        }
