
from operator import truediv
import io, sys
import requests  
from urllib.parse import urlencode
import json


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

token = "1"  # replace with your actual token of target shop 
pagenum = 1 
 
while pagenum:
    
    form_data = {  
        "entekhab": "listitemv2",  
        "currenturl": f"https://emalls.ir/%d9%84%db%8c%d8%b3%d8%aa-%d9%82%db%8c%d9%85%d8%aa~shop~{token}~page~{pagenum}",  
        "pagenum": str(pagenum),  
        "shop": token,  
        "sort": "1",  
        "order": "1",  
        "view": "1"  
    }  
    headers = {  
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",  
        "X-Requested-With": "XMLHttpRequest",  
        "Accept": "application/json, text/javascript, */*; q=0.01",  
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"  
    }  
    response = requests.post("https://emalls.ir/_Search.ashx", data=urlencode(form_data), headers=headers)  
    print("Status Code:", response.status_code)  
    response_body = response.json()
    
    # save response_body to json file.
    with open(f"Digikala_shop_page_{pagenum}.json", "w", encoding="utf-8") as f:
        json.dump(response_body, f, ensure_ascii=False, indent=4)
        print(f"Successfullycrawled page: {pagenum} at {response_body['pagetitle']}")
        
        
    pagenum = response_body['lstpagingresualt'][-1]['page_number'] if (response_body['lstpagingresualt'] and response_body['lstpagingresualt'][-1]['stat'] == 'next') else None
