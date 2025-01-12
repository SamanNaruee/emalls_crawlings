import scrapy  
import json  
from colorama import Fore, Back, Style

class EmallsApiSpider(scrapy.Spider):  
    name = "emalls_api"  
    allowed_domains = ["emalls.ir"]  
    start_urls = ["https://emalls.ir/_Search.ashx"]  
    
    def parse(self, response):  
        response_body = response.text  
        
        try:  
            data = json.loads(response_body)  
            print(Fore.GREEN + str(response.status) + Style.RESET_ALL)  
            print(Fore.BLUE, f"Response data: {str(data)}", Style.RESET_ALL)
        except json.JSONDecodeError:  
            self.logger.error("Failed to decode JSON response")  
        except Exception as e:  
            self.logger.error(f"An error occurred: {e}")  
