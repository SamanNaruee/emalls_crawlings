"""
Playwright script to extract all shop URLs from emalls.ir/Shops/
To run this script you need to have playwright installed, if not
you can install it by running `pip install playwright`

This script will:
1. Open a browser and go to emalls.ir/Shops/
2. Wait for the shop cards to load
3. Extract all shop URLs
"""
import asyncio
import json
from playwright.async_api import async_playwright

async def extract_shop_urls():
    shop_urls = []
    url = "https://emalls.ir/Shops/"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Go to the shops page
        await page.goto(url, wait_until="networkidle")

        try:
            # Wait for shop cards to load
            await page.wait_for_selector("div.shop", timeout=30000)
            
            # Extract all shop URLs and names
            shops = await page.query_selector_all("div.shop")
            
            for shop in shops:
                # Get the shop name
                name_element = await shop.query_selector("h3 a.item-title-text")
                shop_name = await name_element.text_content() if name_element else "Unknown"
                
                # Get the shop URL
                url_element = await shop.query_selector("a.shop-ax")
                if url_element:
                    href = await url_element.get_attribute("href")
                    if href and "/Shop/" in href:
                        full_url = f"https://emalls.ir{href}"
                        # Get additional info
                        shop_type = await shop.query_selector("span.value")
                        shop_type_text = await shop_type.text_content() if shop_type else "Unknown"
                        
                        print(f"Shop: {shop_name.strip()} - Type: {shop_type_text.strip()} - URL: {full_url}")
                        shop_urls.append({
                            "name": shop_name.strip(),
                            "url": full_url,
                            "type": shop_type_text.strip()
                        })
                    
        except Exception as e:
            print(f"Error extracting shop URLs: {e}")
        finally:
            await browser.close()
            
    # Save all urls in a json file to use later
    with open("shop_urls.json", "w", encoding="utf-8") as f:
        json.dump(shop_urls, f, indent=4, ensure_ascii=False)
    return shop_urls

if __name__ == "__main__":
    shop_urls = asyncio.run(extract_shop_urls())
