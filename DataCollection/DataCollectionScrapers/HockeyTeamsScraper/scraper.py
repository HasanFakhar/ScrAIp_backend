from pyppeteer.launcher import launch
import asyncio
import json

async def get_hockey_teams_data():
    browser = await launch(headless=True)
    page = await browser.newPage()

    data = []
    page_num = 1
    while page_num <= 6:
        print(f"Navigating to page {page_num}")
        await page.goto(f"https://www.scrapethissite.com/pages/forms/?page_num={page_num}&per_page=100")
        print("Navigation successful")

        team_elements = await page.querySelectorAll('.team')
        for team_element in team_elements:
            team_name_element = await team_element.querySelector('.name')
            team_name = await page.evaluate('(element) => element.innerText', team_name_element)
            year_element = await team_element.querySelector('.year')
            year = await page.evaluate('(element) => element.innerText', year_element)
            wins_element = await team_element.querySelector('.wins')
            wins = await page.evaluate('(element) => element.innerText', wins_element)
            losses_element = await team_element.querySelector('.losses')
            losses = await page.evaluate('(element) => element.innerText', losses_element)
            ot_losses_element = await team_element.querySelector('.ot-losses')
            ot_losses = await page.evaluate('(element) => element.innerText', ot_losses_element)
            win_pct_element = await team_element.querySelector('.pct')
            win_pct = await page.evaluate('(element) => element.innerText', win_pct_element)
            gf_element = await team_element.querySelector('.gf')
            gf = await page.evaluate('(element) => element.innerText', gf_element)
            ga_element = await team_element.querySelector('.ga')
            ga = await page.evaluate('(element) => element.innerText', ga_element)
            diff_element = await team_element.querySelector('.diff')
            diff = await page.evaluate('(element) => element.innerText', diff_element)
            data.append({"Team Name ": team_name, "Year": year, "Wins": wins, "Losses": losses, "OT Losses": ot_losses, "Win %": win_pct, "Goals For (GF) ": gf, "Goals Against (GA)": ga, "+ / -": diff})
        page_num += 1
    await browser.close()
    print(len(data))

    return {"Hockey Teams": data}

# Specify the file path
file_path = 'hockey_teams_data.json'

# Write the dictionary to a JSON file
with open(file_path, 'w') as json_file:
    json.dump(asyncio.get_event_loop().run_until_complete(get_hockey_teams_data()), json_file, indent=4)

print(f"JSON file created at: {file_path}")