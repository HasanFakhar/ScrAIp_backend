import asyncio
from pyppeteer import launch
from playwright.async_api import async_playwright

async def get_page_text(url: str):
    # Launch a headless browser
    browser = await launch(headless=True)
    # Open a new browser page
    page = await browser.newPage()
    # Navigate to the URL
    await page.goto(url, {'waitUntil': 'load', 'timeout': 0})

    # Evaluate JavaScript on the page to get all inner text
    text = await page.evaluate('''() => {
        return document.body.innerText;
    }''')

    # Close the browser
    await browser.close()

    return text

# Function to run the async part
# def fetch_text(url: str):
#     return asyncio.get_event_loop().run_until_complete(get_page_text(url))
#
# # Example usage
# url = 'https://www.daraz.pk/catalog/?spm=a2a0e.tm80335142.search.d_go&q=mobiles'
# page_text = fetch_text(url)
#
# def write_string_to_file(file_path: str, content: str):
#     with open(file_path, "w", encoding="utf-8") as file:
#         file.write(content)
#
# # Example usage
# file_path = "mobiles.txt"
# write_string_to_file(file_path, page_text)

