import multiprocessing, os, sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from shops_with_specs import ShopsWithSpecsSpider


"""
This script runs the ShopsWithSpecsSpider using Scrapy's CrawlerProcess.
It allows for concurrent crawling processes based on the number of pages specified.

Usage:
    python sws_runner.py <number_of_pages>

Arguments:
    number_of_pages: The total number of pages to crawl. The script will divide 
    this number into multiple processes to optimize crawling based on the available CPU cores.

Example:
    python sws_runner.py 300

Note:
    Ensure that this script is in the same directory as the ShopsWithSpecsSpider 
    implementation for it to function correctly.
"""



def sws_runner(pages):
    process = CrawlerProcess(get_project_settings())
    process.crawl(ShopsWithSpecsSpider, pages=pages)
    process.start()
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sws_runner.py <number_of_pages>")
        sys.exit(1)
    
    pages = int(sys.argv[1])
    
    # Determine number of processes based on pages and CPU count
    num_processes = min(pages // 100, multiprocessing.cpu_count())
    
    processes = []
    for i in range(num_processes):
        start_page = (i * pages) // num_processes + 1
        end_page = ((i + 1) * pages) // num_processes
        process = multiprocessing.Process(
            target=sws_runner,
            args=(end_page - start_page + 1,),
            kwargs={'pages': end_page - start_page + 1}
        )
        process.start()
        processes.append(process)
        
    for process in processes:
        process.join()
    
    with open(f"sws/{pages // 100}.csv", "w") as f:
        f.write("shop_id,shop_title,shop_url,shop_selling_type,shop_was_in_page,shop_img,shop_score,shop_social_media_handles,shop_recieved_date,shop_crawled_at,shop_current_city,shop_duration_of_cooperation_with_emalls,shop_website,shop_Enamad_sign,name_of_person_in_charge,phone_number,shop_email,shop_address,senfi_number,cooperation_status_with_emalls,shop_all_products_target_url\n")
        for i in range(start_page, end_page + 1):
            with open(f"sws/{i}.json", "r") as f2:
                for line in f2:
                    f.write(line.strip() + "\n")
    
    
    # remove temp json files after merging into one big csv file
    for i in range(start_page, end_page + 1):
        os.remove(f"sws/{i}.json")
