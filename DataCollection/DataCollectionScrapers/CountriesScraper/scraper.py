from pyppeteer.launcher import launch
import asyncio
import json

async def get_countries_data():
    browser = await launch(headless=True)
    page = await browser.newPage()

    print("Navigating to Countries page")
    await page.goto("https://www.scrapethissite.com/pages/simple/")

    data = []
    country_elements = await page.querySelectorAll('.country')
    for country_element in country_elements:
        country_name_element = await country_element.querySelector('.country-name')
        country_name = await page.evaluate('(element) => element.innerText', country_name_element)
        country_capital_element = await country_element.querySelector('.country-info .country-capital')
        country_capital = await page.evaluate('(element) => element.innerText', country_capital_element)
        country_population_element = await country_element.querySelector('.country-info .country-population')
        country_population = await page.evaluate('(element) => element.innerText', country_population_element)
        country_area_element = await country_element.querySelector('.country-info .country-area')
        country_area = await page.evaluate('(element) => element.innerText', country_area_element)
        data.append({"country-name": country_name, "Capital": country_capital, "Population": country_population, "Area (km2)": country_area})

    await browser.close()
    print(len(data))

    return {"countries": data}

# Specify the file path
file_path = 'countries_data.json'

# Write the dictionary to a JSON file
with open(file_path, 'w') as json_file:
    json.dump(asyncio.get_event_loop().run_until_complete(get_countries_data()), json_file, indent=4)

print(f"JSON file created at: {file_path}")


