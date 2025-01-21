# Commented out import for REG_FULL_RESOURCE_DESCRIPTOR from winreg
import scrapy
from .logger_me import custom_log
import datetime
from memory_profiler import profile
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor

class ShopsWithSpecsSpider(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY': 0.0005,                   # 0.5 milisecond delay between requests
        'CONCURRENT_REQUESTS': 200,                 # max number of concurrent requests on all domains
        'DOWNLOAD_TIMEOUT': 35,                      # max time in second to wait for a response
        'REACTOR_THREADPOOL_MAXSIZE': 120,           # max size of twisted reactor thread pool
        'LOG_LEVEL': 'INFO',                        # level of logging detail ((DEBUG, INFO, WARNING, ERROR, CRITICAL)): less termnal output
        'COOKIES_ENABLED': False,                   # disable cookie handling to reduce overhead
        'RETRY_ENABLED': False,                     # disable automatic retry of failed requests
        'DOWNLOAD_FAIL_ON_DATALOSS': False,         # handle fail of incomplete responses
        # try autothrottle for better performance: 
            # manage download delay dynamically depend on concurrent requests and server response time
    }
    
    name = "sws"
    allowed_domains = ["emalls.ir"]
    start_urls = ["https://emalls.ir/Shops/"]

    def __init__(self, pages, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = perf_counter()
        self.page_times = {}
        self.shop_times = {}
        self.pages = pages # all pages that must crawl. Usage: scrapy crawl sws -a pages=100 to crawl 100 pages from 1 to 100.

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            dont_filter=True
        )

    @profile
    def parse(self, response):
        final_page = response.css('#ContentPlaceHolder1_rptPagingBottom_hlinkPage_6::text').get()
        total_pages = int(final_page) if final_page and final_page.isdigit() else 3
<<<<<<< HEAD
        total_pages = 942  # Adjust it for all pages to final_page
=======
        total_pages = int(self.pages)
>>>>>>> 6617313 (update sws spider.)
        
        # Generate all page requests at once
        start_page = max(1, total_pages - 99)
        urls = [f"https://emalls.ir/Shops/page.{page}" for page in range(start_page, total_pages + 1)]
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.page_detail_parse,
                meta={'current_page': urls.index(url) + 1},
                dont_filter=True,
                priority=10
            )

    def page_detail_parse(self, response):
        current_page = response.meta['current_page']
        
        for id in range(48):
            shop_url_partial = response.css(f"#ContentPlaceHolder1_rptShops_hlkTitle_{id}::attr(href)").get()
            if shop_url_partial:
                full_shop_url = f'https://emalls.ir/{shop_url_partial}'
                
                basic_info = {
                    'shop_was_in_page': current_page,
                    'shop_img': response.css(f'#ContentPlaceHolder1_rptShops_imgLogo_{id}::attr(src)').get(),
                    'shop_title': response.css(f"#ContentPlaceHolder1_rptShops_hlkTitle_{id}::text").get(),
                    'shop_url': full_shop_url,
                    'shop_id': shop_url_partial.split('/')[-2],
                    'shop_selling_type': response.css(f'#ContentPlaceHolder1_rptShops_LblShopType_{id}::text').get(),
                }
                
                yield scrapy.Request(
                    url=full_shop_url,
                    callback=self.parse_shop_details,
                    meta={'basic_info': basic_info},
                    dont_filter=True,
                    priority=5
                )

    def parse_shop_details(self, response):
        basic_info = response.meta['basic_info']
        
        detailed_info = {
            'senfi_number': response.css("#ContentPlaceHolder1_lblasnaf::text").get(),
            'shop_all_products_target_url': response.css("#DivPartProducts a::attr(href)").get(),
            'cooperation_status_with_emalls': response.css("#ContentPlaceHolder1_lblshopstatus::text").get(),
            'name_of_person_in_charge': response.css("#ContentPlaceHolder1_lblMasool1::text").get(),
            'phone_number': response.css("#ContentPlaceHolder1_lblTelephone1::text").get(),
            'shop_address': response.css("#ContentPlaceHolder1_lblAddress1::text").get(),
            'shop_email': response.css("#ContentPlaceHolder1_lblEmail::text").get(),
            'shop_score': response.css("#ContentPlaceHolder1_lblRateValue2::text").get(),
            'shop_social_media_handles': response.css("#ContentPlaceHolder1_DivSocial a::attr(href)").getall(),
            'shop_recieved_date': response.css("#CtrlFooterLinks_LblDate::text").get(),
            'shop_crawled_at': datetime.datetime.now(datetime.timezone.utc),
            'shop_current_city': response.css("#ContentPlaceHolder1_lblLocation::text").get(),
            'shop_duration_of_cooperation_with_emalls': response.css("#ContentPlaceHolder1_lblHamkariBaEmalls::text").get(),
            'shop_website': response.css("#ContentPlaceHolder1_HlkWebsite1::attr(href)").get(),
            'shop_Enamad_sign': response.css("#ContentPlaceHolder1_lblNamad::text").get(),
        }
        
        
        yield {**basic_info, **detailed_info}
