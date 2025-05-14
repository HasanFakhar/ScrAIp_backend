import requests
import json
import os
from deepdiff import DeepDiff

def countries_eval():
    # Get the correct path
    json_path = os.path.join(os.path.dirname(__file__), "../../DataCollection/Data/countries_data.json")
    
    # Load the JSON file
    with open(json_path, "r", encoding="utf-8") as file:
        countries_data = json.load(file)

    # Define test inputss
    test_url = "https://www.scrapethissite.com/pages/simple/"
    test_query = ("i want the following data for all the countries, \"countries\" is the outer most label, then for each country, "
                  "\"country-name\", \"Capital\", \"Population\", \"Area (km2)\" are the sublabels. Change all numbers to strings")
    
    # Run the pipeline asynchronously
    automatic_response = requests.get(f"http://127.0.0.1:6000/scraip?url={test_url}&query={test_query}").json()
    
    # Compare the two responses
    diff = DeepDiff(countries_data, automatic_response, ignore_order=True)
    
    return diff


