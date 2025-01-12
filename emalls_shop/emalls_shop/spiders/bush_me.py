import scrapy


class BushMeSpider(scrapy.Spider):
    """
    we can use SelectorGadget to select an element and then get it's attributes:
        element = response.css("the selected css pattern")
        element.attrib
            {
                'id': 'ContentPlaceHolder1_HlkWebsite1',
                'class': 'ex-link-icon link-website',
                'rel': 'noreferrer noopener nofollow',
                'href': 'https://boschme.com/'
        }
    """
    
    name = "bush_me"
    allowed_domains = ["emalls.ir"]
    start_urls = ["https://emalls.ir/Shop/35316/"]

    def parse(self, response):   
        phone_number = response.css("#ContentPlaceHolder1_lblTelephone1::text").get()  
        cleaned_phone_number = phone_number.strip() if phone_number else None   
        print(f"Phone Number: {cleaned_phone_number}")  
        yield {  
            'phone_number': cleaned_phone_number,  
        }  
        
        if not cleaned_phone_number:  
            print("No phone number found.")  
            
            
        print("\n\ntext: ", response.css("#ContentPlaceHolder1_HlkWebsite1::text").get())
        print("\n\nhref: ", response.css("#ContentPlaceHolder1_HlkWebsite1::attr(href)").get())

        
        