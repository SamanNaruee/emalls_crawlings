import scrapy
from colorama import Fore, Style

class BushMeSpider(scrapy.Spider):
    """
    sometimes we must wait to page fully load before crawling, we can use the following:
    we can also add a delay to our spider to make it slower. 
    in crawling, sometimes we need to get an element's attributes.
    but the content might be loaded dynamically via JavaScript
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
        print(Fore.BLUE + f"{response.css('.CommentItem').getall()[0]}" + Style.RESET_ALL)
        shop_informations = {
            'cooperation_status_with_emalls': response.css("#ContentPlaceHolder1_lblshopstatus::text").get(),
            'name_of_person_in_charge': response.css("#ContentPlaceHolder1_lblMasool1::text").get(), 
            'phone_number': response.css("#ContentPlaceHolder1_lblTelephone1::text").get(), 
            'shop_address': response.css("#ContentPlaceHolder1_lblAddress1::text").get(),
            'shop_all_products_target_url': response.css("#DivPartProducts a::attr(href)").get(),
            'shop_comments': [
                    {   
                        'comment_date': comment.css(f"#ContentPlaceHolder1_rptComments_lblDate_{i}::text").get(),
                    }
                for i, comment in response.css(".CommentItem")
            ],
            'shop_crawled_data': response.css("#CtrlFooterLinks_LblDate::text").get(),
            'shop_current_city': response.css("#ContentPlaceHolder1_lblLocation::text").get(),
            'shop_duration_of_cooperation_with_emalls': response.css("#ContentPlaceHolder1_lblHamkariBaEmalls::text").get(),
            'shop_email': response.css("#ContentPlaceHolder1_lblEmail::text").get(),
            'shop_img_icon': response.css("#ContentPlaceHolder1_imgLogo2::attr(src)").get(),
            'shop_name': response.css("h1::text").get().replace(" ", "") if response.css("h1::text").get() else None,
            'shop_score': response.css("#ContentPlaceHolder1_lblRateValue2::text").get(),
            'shop_social_media_handles': response.css("#ContentPlaceHolder1_DivSocial a::attr(href)").getall(),
            'shop_website': response.css("#ContentPlaceHolder1_HlkWebsite1::attr(href)").get(),
            'shop_Enamad_sign': response.css("#ContentPlaceHolder1_lblNamad::text").get(),
        }
        yield shop_informations
        # print(Fore.BLUE + f"{comments}" + Style.RESET_ALL)
            