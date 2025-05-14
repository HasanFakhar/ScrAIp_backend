from ScraperTests.countries import countries_eval

def run_all_evals():
    differences = {}

    differences['countries_data_differences'] = countries_eval()
    print(differences)