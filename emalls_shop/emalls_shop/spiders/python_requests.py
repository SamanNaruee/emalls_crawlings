import io, sys
import requests  
from urllib.parse import urlencode
import json

# Tell Python to use UTF-8 encoding when printing the response body
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


token = "1"  # replace with your actual token  
pagenum = 20  

 
for page in range(1, pagenum + 1):
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
    # print("Response Body:", response.json())

    response_body = response.json()

    print(response_body['pagetitle'], page)
    
    # save response_body to json file.
    with open(f"Digikala_shop_page_{page}.json", "w", encoding="utf-8") as f:
        json.dump(response_body, f, ensure_ascii=False, indent=4)

