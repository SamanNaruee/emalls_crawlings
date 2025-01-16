import scrapy
from .logger_me import custom_log
from scrapy.crawler import Crawler
from .shop_spider import ShopSpecSpider

class OnlyShopsSpider(scrapy.Spider):
    name = "only_shops"
    allowed_domains = ["emalls.ir"]
    start_urls = ["https://emalls.ir/Shops/"]
    
    def start_requests(self):
        url = self.start_urls[0]
        
        yield scrapy.Request(
            url=url,
            callback=self.parse,
        )

    def parse(self, response):
        final_page = response.css('#ContentPlaceHolder1_rptPagingBottom_hlinkPage_6::text').get()
        for page in range(1, 3): # len(final_page) + 1
            url = f"https://emalls.ir/Shops/page.{page}"
            yield scrapy.Request(
                url=url,
                callback=self.page_detail_parse,
            )
    
    def page_detail_parse(self, response):
        shops = {}
        for id in range(48):
            shop = {}
            shop[f'shop_img'] = response.css(f'#ContentPlaceHolder1_rptShops_imgLogo_{id}::attr(src)').get()
            shop['shop_title'] = response.css(f"#ContentPlaceHolder1_rptShops_hlkTitle_{id}::text").get()
            shop['shop_url'] = f'https://emalls.ir/{response.css(f"#ContentPlaceHolder1_rptShops_hlkTitle_{id}::attr(href)").get()}'
            shop['shop_id'] = shop['shop_url'].split('/')[-2]
            shop['shop_selling_type'] = response.css(f'#ContentPlaceHolder1_rptShops_LblShopType_{id}::text').get()
            shop['specs'] = scrapy.Request(
                url=shop['shop_url'],
                callback=self.shop_detail_specs,
                meta={'shop_token': shop['shop_id']}
            )
            shops[shop['shop_title']] = shop

        
        yield shops
    
    def shop_detail_specs(self, response):
        shop_token = response.meta['shop_token']
        crawler = Crawler(ShopSpecSpider, shop_token=shop_token)
        product_specs = crawler.crawl(return_value=True)
        return {
            'shop_token': shop_token,
            'product_specs': product_specs,
        }
