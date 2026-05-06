from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time


SEARCH_QUERY = "laptop"
TOTAL_PAGES = 6
OUTPUT_FILE = "daraz.json"

driver = webdriver.Chrome()
wait= WebDriverWait(driver, 15)

all_products=[]

try:
    for page in range(1, TOTAL_PAGES + 1):
        url= f"https://www.daraz.pk/catalog/?q={SEARCH_QUERY}&page={page}"
        driver.get(url)

        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-qa-locator='product-item']")))

        time.sleep(2)
        html= driver.page_source
        soup= BeautifulSoup(html, "html.parser")
        products= soup.find_all("div", {"data-qa-locator": "product-item"})
        print(f"{len(products)} products found on page {page}.")

        for product in products:
            try:
                name= product.find("div", class_='RfADt').get_text(strip=True)
                price= product.find("span", class_='ooOxS').get_text(strip=True)
                rating_tag= product.find("span", class_='_9-ogB Dy1nx')
                rating= rating_tag.get_text(strip=True) if rating_tag else "No rating"

                all_products.append({
                    "Name": name,
                    "Price": price,
                    "Rating": rating
                })
            except AttributeError as e:
                print(f"Error occurred while parsing product: {e}")
                continue
except Exception as e:
    print(f"An error occurred: {e}")
    
finally:
    driver.quit()

df= pd.DataFrame(all_products)
df.to_json(OUTPUT_FILE, orient="records", indent=4, force_ascii=False)
print(f"Data saved to {OUTPUT_FILE}. Total products scraped: {len(all_products)}")