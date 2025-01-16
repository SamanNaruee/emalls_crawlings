import scrapy
from .logger_me import custom_log

class ShopsWithSpecsSpider(scrapy.Spider):
    name = "sws"
    allowed_domains = ["emalls.ir"]
    start_urls = ["https://emalls.ir/Shops/"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
        )

    def parse(self, response):
        final_page = response.css('#ContentPlaceHolder1_rptPagingBottom_hlinkPage_6::text').get()
        total_pages = int(final_page) if final_page and final_page.isdigit() else 3
        for page in range(1, 3): #Replace 3 with this: total_pages + 1
            url = f"https://emalls.ir/Shops/page.{page}"
            yield scrapy.Request(
                url=url,
                callback=self.page_detail_parse,
            )

    def page_detail_parse(self, response):
        for id in range(48):
            shop_url_partial = response.css(f"#ContentPlaceHolder1_rptShops_hlkTitle_{id}::attr(href)").get()
            if shop_url_partial:
                full_shop_url = f'https://emalls.ir/{shop_url_partial}'
                shop = {
                    'shop_img': response.css(f'#ContentPlaceHolder1_rptShops_imgLogo_{id}::attr(src)').get(),
                    'shop_title': response.css(f"#ContentPlaceHolder1_rptShops_hlkTitle_{id}::text").get(),
                    'shop_url': full_shop_url,
                    'shop_id': shop_url_partial.split('/')[-2],
                    'shop_selling_type': response.css(f'#ContentPlaceHolder1_rptShops_LblShopType_{id}::text').get(),
                    'shop_all_products_target_url': response.css("#DivPartProducts a::attr(href)").get(),
                }

                yield scrapy.Request(
                    url=full_shop_url,
                    callback=self.shop_detail_specs,
                    meta={'shop_data': shop}
                )

    def shop_detail_specs(self, response):
        shop = response.meta['shop_data']

        shop_details = {
            'cooperation_status_with_emalls': response.css("#ContentPlaceHolder1_lblshopstatus::text").get(),
            'name_of_person_in_charge': response.css("#ContentPlaceHolder1_lblMasool1::text").get(), 
            'phone_number': response.css("#ContentPlaceHolder1_lblTelephone1::text").get(), 
            'shop_address': response.css("#ContentPlaceHolder1_lblAddress1::text").get(),
            'shop_email': response.css("#ContentPlaceHolder1_lblEmail::text").get(),
            'shop_score': response.css("#ContentPlaceHolder1_lblRateValue2::text").get(),
            'shop_social_media_handles': response.css("#ContentPlaceHolder1_DivSocial a::attr(href)").getall(),
            'shop_comments': [
                {
                    'comment_date': comment.css(f"#ContentPlaceHolder1_rptComments_lblDate_{i}::text").get(default='').strip(),
                    'name': comment.css('span.name::text').get(default='').strip(),
                    'role': comment.css('span.TheOrange.semat::text').get(default='').strip(),
                    'comment': comment.css('span.Text::text').get(default='').strip(),
                    'comment_star': comment.css(f'#ContentPlaceHolder1_rptComments_lblRate_{i}::text').get(default='').strip(),
                } 
                for i, comment in enumerate(response.css(".CommentItem"))
            ],
            'shop_crawled_date': response.css("#CtrlFooterLinks_LblDate::text").get(),
            'shop_current_city': response.css("#ContentPlaceHolder1_lblLocation::text").get(),
            'shop_duration_of_cooperation_with_emalls': response.css("#ContentPlaceHolder1_lblHamkariBaEmalls::text").get(),
            'shop_img_icon': response.css("#ContentPlaceHolder1_imgLogo2::attr(src)").get(),
            'shop_name': response.css("h1::text").get().replace(" ", "") if response.css("h1::text").get() else None,
            'shop_website': response.css("#ContentPlaceHolder1_HlkWebsite1::attr(href)").get(),
            'shop_Enamad_sign': response.css("#ContentPlaceHolder1_lblNamad::text").get(),
        }

        shop.update(shop_details)
        yield shop
