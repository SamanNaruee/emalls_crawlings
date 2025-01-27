# from operator import truediv
# import io, sys
# import requests
# from urllib.parse import urlencode
# import json
# import random
# from time import sleep

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# def crawl_emalls(token="1"):
#     pagenum = 1
#     while pagenum:
#         # Sleep for just page
#         sleep(random.randrange(0.9, 2.0))
#         form_data = {
#             "entekhab": "listitemv2",
#             "currenturl": f"https://emalls.ir/%d9%84%db%8c%d8%b3%d8%aa-%d9%82%db%8c%d9%85%d8%aa~shop~{token}~page~{pagenum}",
#             "pagenum": str(pagenum),
#             "shop": token,
#             "sort": "1",
#             "order": "1",
#             "view": "1"
#         }
#         headers = {
#             "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#             "X-Requested-With": "XMLHttpRequest",
#             "Accept": "application/json, text/javascript, */*; q=0.01",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"  # 200 means success
#         }
#         response = requests.post("https://emalls.ir/_Search.ashx", data=urlencode(form_data), headers=headers)
#         print("Status Code:", response.status_code)
#         response_body = response.json()

#         with open(f"Digikala_shop_page_{pagenum}.json", "w", encoding="utf-8") as f:
#             json.dump(response_body, f, ensure_ascii=False, indent=4)
#             print(f"Successfully crawled page: {pagenum} at {response_body['pagetitle']}")

#         pagenum = response_body['lstpagingresualt'][-1]['page_number'] if (
#             response_body['lstpagingresualt'] and response_body['lstpagingresualt'][-1]['stat'] == 'next') else None

# if __name__ == "__main__":
#     crawl_emalls(token="1")
