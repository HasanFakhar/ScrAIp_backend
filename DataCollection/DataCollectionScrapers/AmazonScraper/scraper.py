from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import time
import json

# Function to extract Product Title
def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        title_value = title.text.strip()
    except AttributeError:
        title_value = ""
    return title_value

# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("span", attrs={'id': 'priceblock_ourprice'}).string.strip()
    except AttributeError:
        try:
            price = soup.find("span", attrs={'id': 'priceblock_dealprice'}).string.strip()
        except:
            price = ""
    return price

# Function to extract Product Rating
def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = ""
    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()
    except AttributeError:
        review_count = ""
    return review_count

# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip()
    except AttributeError:
        available = "Not Available"
    return available

# Function to extract product links from a page
def get_links(soup):
    links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})
    links_list = []
    for link in links:
        links_list.append("https://www.amazon.ae" + link.get('href'))
    return links_list

if __name__ == '__main__':
    HEADERS = ({'User-Agent': '', 'Accept-Language': 'en-US, en;q=0.5'})
    
    # Define a base URL for pagination
    base_url = "https://www.amazon.ae/s?k=perfumes&crid=3KDXHCZHM2G83&sprefix=perfumes%2Caps%2C263&ref=nb_sb_noss_1"
    
    # Initialize dictionary to hold product details
    d = {"title": [], "price": [], "rating": [], "reviews": [], "availability": []}

    # Loop over pages
    for page in range(1, 6):  # Adjust the range to scrape more or fewer pages
        URL = base_url + str(page)
        print(f"Scraping page {page}")
        
        # HTTP Request
        webpage = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")

        # Extract product links from the current page
        links_list = get_links(soup)

        # Loop for extracting product details from each product link
        for link in links_list:
            new_webpage = requests.get(link, headers=HEADERS)
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")

            # Function calls to extract and store product information
            d['title'].append(get_title(new_soup))
            d['price'].append(get_price(new_soup))
            d['rating'].append(get_rating(new_soup))
            d['reviews'].append(get_review_count(new_soup))
            d['availability'].append(get_availability(new_soup))

        # Pause for a few seconds to avoid overwhelming the server
        time.sleep(2)
    
    # Create DataFrame from dictionary
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    
    # Display the DataFrame
    print(amazon_df)

    # Convert DataFrame to JSON format and save it as a file
    amazon_df.to_json("amazon_data.json", orient='records', indent=4)
    print("JSON file saved as 'amazon_data.json'.")

