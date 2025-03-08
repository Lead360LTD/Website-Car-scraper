from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
from selenium.common.exceptions import TimeoutException

def extract_car_listings(url, browser):
    listings = []
    try:
        browser.get(url)
        time.sleep(5)  # Wait for the page to load
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Adjust the selector to match the HTML structure
        car_elements = soup.find_all('div', class_='g-vehicle-card__description')

        for car_element in car_elements:
            try:
                # Extract data from the correct elements
                title_element = car_element.find('h3', class_='g-vehicle-card__vehicle-title')
                title = title_element.text.strip() if title_element else "N/A"

                price_element = car_element.find('span', class_='df aifs')
                price = price_element.text.strip() if price_element else "N/A"

                # Assuming make and model are in the title
                make = title.split(' ')[1] if len(title.split(' ')) > 1 else "N/A"
                model = title.split(' ')[2] if len(title.split(' ')) > 2 else "N/A"

                # Assuming year is the first element in the title
                year = title.split(' ')[0] if len(title.split(' ')) > 0 and title.split(' ')[0].isdigit() else "N/A"

                kilometers = "N/A"  # Kilometers not found in the provided HTML

                listings.append({
                    "Website": url,
                    "Price": price,
                    "Make": make,
                    "Model": model,
                    "Year": year,
                    "Kilometers": kilometers
                })
            except Exception as e:
                print(f"  Error extracting data from a listing: {e}")

    except TimeoutException:
        print(f"Timeout loading {url}")
    except Exception as e:
        print(f"Error processing {url}: {e}")

    return listings

def scrape_car_listings_from_file(filename="websites.txt", output_filename="car_listings.csv"):
    browser = webdriver.Chrome()
    all_listings = []

    try:
        with open(filename, 'r') as f:
            website_list = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
        return

    for url in website_list:
        print(f"Processing: {url}")
        listings = extract_car_listings(url, browser)
        if listings:
            print(f"  Found {len(listings)} listings.")
            all_listings.extend(listings)
        else:
            print("  No listings found.")

    browser.quit()

    if all_listings:
        with open(output_filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ["Website", "Price", "Make", "Model", "Year", "Kilometers"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_listings)
        print(f"Data written to {output_filename}")
    else:
        print("No data to write to CSV.")

if __name__ == "__main__":
    scrape_car_listings_from_file()
