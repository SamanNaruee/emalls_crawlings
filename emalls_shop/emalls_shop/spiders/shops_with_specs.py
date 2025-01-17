import scrapy
from .logger_me import custom_log
from django.utils import timezone
from memory_profiler import profile

class ShopsWithSpecsSpider(scrapy.Spider):
    custom_settings = {
        'CONCURRENT_REQUESTS': 16,  # Maximum number of concurrent requests across all domains
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,  # Maximum number of concurrent requests per domain
        'DOWNLOAD_DELAY': 1,  # Wait 1 second between consecutive requests to same domain
        'RANDOMIZE_DOWNLOAD_DELAY': True,  # Add random delay between requests to avoid detection
        'MEMUSAGE_ENABLED': True,  # Enable memory usage monitoring
        'MEMUSAGE_LIMIT_MB': 512,  # Stop spider if memory usage exceeds 512MB
        'MEMUSAGE_WARNING_MB': 384,  # Warn when memory usage exceeds 384MB
        'MEMUSAGE_CHECK_INTERVAL_SECONDS': 60,  # Check memory usage every 60 seconds
        'HTTPCACHE_ENABLED': True,  # Enable HTTP caching
        'HTTPCACHE_EXPIRATION_SECS': 3600,  # Cache responses for 1 hour
        'HTTPCACHE_DIR': 'httpcache',  # Directory to store HTTP cache
        'AUTOTHROTTLE_ENABLED': True,  # Enable automatic throttling
        'AUTOTHROTTLE_START_DELAY': 1,  # Initial download delay
        'AUTOTHROTTLE_MAX_DELAY': 3,  # Maximum download delay
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 8  # Target average number of concurrent requests
    }
    name = "sws"
    allowed_domains = ["emalls.ir"]
    start_urls = ["https://emalls.ir/Shops/"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
        )

    @profile
    def parse(self, response):
        final_page = response.css('#ContentPlaceHolder1_rptPagingBottom_hlinkPage_6::text').get()
        total_pages = int(final_page) if final_page and final_page.isdigit() else 3
        for page in range(1, total_pages + 1):
            url = f"https://emalls.ir/Shops/page.{page}"
            yield scrapy.Request(
                url=url,
                callback=self.page_detail_parse,
                meta={'current_page': page}
            )

    def page_detail_parse(self, response):
        current_page = response.meta['current_page']
        shop_divs = response.css('div.row > div')
        
        for id in range(48):
            shop_url_partial = response.css(f"#ContentPlaceHolder1_rptShops_hlkTitle_{id}::attr(href)").get()
            if shop_url_partial:
                full_shop_url = f'https://emalls.ir/{shop_url_partial}'
                
                # First collect basic info
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
                    dont_filter=True
                )

    def parse_shop_details(self, response):
        basic_info = response.meta['basic_info']
        
        detailed_info = {
            'shop_all_products_target_url': response.css("#DivPartProducts a::attr(href)").get(),
            'cooperation_status_with_emalls': response.css("#ContentPlaceHolder1_lblshopstatus::text").get(),
            'name_of_person_in_charge': response.css("#ContentPlaceHolder1_lblMasool1::text").get(),
            'phone_number': response.css("#ContentPlaceHolder1_lblTelephone1::text").get(),
            'shop_address': response.css("#ContentPlaceHolder1_lblAddress1::text").get(),
            'shop_email': response.css("#ContentPlaceHolder1_lblEmail::text").get(),
            'shop_score': response.css("#ContentPlaceHolder1_lblRateValue2::text").get(),
            'shop_social_media_handles': response.css("#ContentPlaceHolder1_DivSocial a::attr(href)").getall(),
            'shop_comments': [
                {
                    'comment_date': comment.css('span.date::text').get(default='').strip(),
                    'name': comment.css('span.name::text').get(default='').strip(),
                    'role': comment.css('span.TheOrange.semat::text').get(default='').strip(),
                    'comment': comment.css('span.Text::text').get(default='').strip(),
                    'comment_star': comment.css('span.rate::text').get(default='').strip(),
                }
                for comment in response.css(".CommentItem")
            ],
            'shop_recieved_date': response.css("#CtrlFooterLinks_LblDate::text").get(),
            'shop_crawled_at': timezone.now(),
            'shop_current_city': response.css("#ContentPlaceHolder1_lblLocation::text").get(),
            'shop_duration_of_cooperation_with_emalls': response.css("#ContentPlaceHolder1_lblHamkariBaEmalls::text").get(),
            'shop_img_icon': response.css("#ContentPlaceHolder1_imgLogo2::attr(src)").get(),
            'shop_name': response.css("h1::text").get().strip() if response.css("h1::text").get() else None,
            'shop_website': response.css("#ContentPlaceHolder1_HlkWebsite1::attr(href)").get(),
            'shop_Enamad_sign': response.css("#ContentPlaceHolder1_lblNamad::text").get(),
        }
        
        yield {**basic_info, **detailed_info}
