"""
Playwright script to extract all categories from emalls.ir
To run this script you need to have playwright installed, if not
you can install it by running `pip install playwright`

Then you can run this script by running `python urls_extract_playwright.py`

This script will open a browser and go to emalls.ir and wait for the main menu to appear
Then it will click on the main menu and wait for the dropdown to appear
After that it will extract all categories from the dropdown and print their names and links
"""
import asyncio
from playwright.async_api import async_playwright

async def extract_categories():
    links = {}
    url = "https://emalls.ir/"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Go to the website
        await page.goto(url, wait_until="networkidle")

        try:
            await page.wait_for_selector("span[data-cro-id='header-main-menu']", timeout=10000)
            await page.click("span[data-cro-id='header-main-menu']")
            await page.wait_for_timeout(2000)  # Wait for the dropdown to appear
        except Exception as e:
            print(f"Error clicking main menu: {e}")
            await browser.close()
            return

        try:
            categories = await page.query_selector_all('a[href^="/Shops/"]')  # Extract all links that start with /Shops/
            for category in categories:
                name = await category.text_content()
                link = await category.get_attribute("href")
                print(f"{name.strip()}: {link}")
                links[name.strip()] = link
        except Exception as e:
            print(f"Error extracting categories: {e}")

        await browser.close()    


asyncio.run(extract_categories())
