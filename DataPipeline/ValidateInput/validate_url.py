import requests

import kagglehub

import pandas as pd

# Download latest version
# Download latest version
def validate_url(url: str = None):

    if not url:

        return False
    
    try:
        
        response = requests.head(url, allow_redirects=True, timeout=5)
        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.RequestException:
        return False

# MALICIOUS WEBSITESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS



def load_dataset(path):
    data = pd.read_csv(path)
    return data

def is_url_malicious(url, dataset):
    """Check if a URL is malicious based on the dataset."""
    entry = dataset[dataset['url'] == url]
    if not entry.empty:
        url_type = entry.iloc[0]['type']
        if url_type in ['phishing', 'defacement', 'malware']:  # Define malicious types
            return True, url_type
        return False, url_type
    return False, "not found in dataset"



if __name__ == "__main__":
    # Path to the dataset
    dataset_path = "./malicious_phish.csv"

    # Load the dataset
    dataset = load_dataset(dataset_path)

    # Input URL to check
    test_url = input("Enter a URL to check: ")

    # Check if the URL is malicious
    is_malicious, url_type = is_url_malicious(test_url, dataset)

    if is_malicious:
        print(f"The URL '{test_url}' is malicious. Type: {url_type}.")
    else:
        if url_type == "not found in dataset":
            print(f"The URL '{test_url}' was not found in the dataset.")
        else:
            print(f"The URL '{test_url}' is benign. Type: {url_type}.")
