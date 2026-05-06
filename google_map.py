from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re

SEARCH_QUERY = "restaurants in Johar Town Lahore"
OUTPUT_FILE = "google_maps_restaurants.csv"


def parse_place_text(text: str) -> dict:
    """Extract rating/reviews/category/address from a Google Maps place text block."""
    rating = "No rating"
    reviews = "0"
    address = "N/A"
    category = "N/A"

    lines = [ln.strip() for ln in (text or "").split("\n") if ln.strip()]

    for line in lines:
        # ⭐ Rating (example: 4.5)
        if re.match(r"^\d\.\d$", line):
            rating = line
            continue

        # ⭐ Reviews (attempt: extract last number when line looks review-ish)
        low = line.lower()
        if any(ch.isdigit() for ch in line) and ("," in line or "review" in low):
            nums = re.findall(r"\d+", line)
            if nums:
                reviews = nums[-1]
            continue

        # ⭐ Category + Address (often separated by '·')
        if "·" in line and "open" not in low:
            parts = [p.strip() for p in line.split("·")]
            if len(parts) >= 2:
                category = parts[0]
                addr = parts[1]
                if any(c.isalpha() for c in addr):
                    address = addr
            continue

        # ⭐ Address fallback
        if len(line) > 10 and not any(x in line for x in ["Open", "Closes", "·"]):
            if any(c.isalpha() for c in line):
                address = line

    return {
        "Rating": rating,
        "Reviews": reviews,
        "Category": category,
        "Address": address,
    }


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)
all_restaurants = []

try:
    url = f"https://www.google.com/maps/search/{SEARCH_QUERY.replace(' ', '+')}"
    driver.get(url)
    print(f"Searching for '{SEARCH_QUERY}' on Google Maps...")

    # Wait for results feed
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='feed']")))
    print("----search results loaded----")

    scrollable_div = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")

    for _ in range(5):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
        time.sleep(2)
        print("----scrolled down----")

        listings = driver.find_elements(By.CSS_SELECTOR, "div[role='article']")
        print(f"Found {len(listings)} restaurants so far...")

        for place in listings:
            try:
                name = place.get_attribute("aria-label") or "N/A"
                parsed = parse_place_text(place.text)

                all_restaurants.append(
                    {
                        "Name": name,
                        **parsed,
                    }
                )
            except Exception as e:
                print(f"Error occurred while parsing restaurant: {e}")
                continue

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()

# Build dataframe + dedupe

df = pd.DataFrame(all_restaurants)
if not df.empty:
    df = df.drop_duplicates(subset=["Name"])

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f"\n✅ {len(df)} restaurants saved → {OUTPUT_FILE}")
    print(df.head())
else:
    print("No restaurants extracted.")

