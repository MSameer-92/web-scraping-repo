from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import pandas as pd

driver= webdriver.Chrome()

driver.get("https://quotes.toscrape.com/login")

wait=WebDriverWait(driver, 10)

username= driver.find_element(By.NAME ,"username")
username.send_keys("admin")

password=driver.find_element(By.NAME ,"password")
password.send_keys("admin")

login_btn=driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
login_btn.click()

wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME ,"quote")))

all_quotes=[]

for page in range(1, 4):
    print(f"Scraping page {page}...")

    html=driver.page_source
    soup= BeautifulSoup(html, "html.parser")

    quotes=soup.find_all('span', class_='text')

    for q in quotes:
        text=q.get_text()
        print(text)
        length = len(text)
        words = len(text.split())
        all_quotes.append(text)

    try:
        next_btn=driver.find_element(By.LINK_TEXT ,"Next")
        old_url=driver.current_url
        next_btn.click()
        wait.until(EC.url_changes(old_url))

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "quote")))
    except:
        print("No more pages to scrape.")
        break

driver.quit()

df=pd.DataFrame(all_quotes, columns=["Quote"])
df.to_csv("quotes.csv", index=False, encoding="utf-8") 
print(df.head())
