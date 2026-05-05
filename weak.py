from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

try:
    # 1. Browser Setup
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    # 2. Open Wikipedia
    driver.get("https://wikipedia.org")
    wait = WebDriverWait(driver, 15)

    # 3. Search Box - (Aapke diye gaye HTML ke mutabiq Name selector use kiya hai)
    search = wait.until(EC.element_to_be_clickable((By.NAME, "search")))
    
    search.clear()
    search.click()
    search.send_keys("Python (programming language)")
    search.send_keys(Keys.RETURN)

    # 4. Wait for Page Load - Article ki main heading ka wait
    wait.until(EC.presence_of_element_located((By.ID, "firstHeading")))

    # 5. Headings Extract aur Filter karein
    all_headings = driver.find_elements(By.TAG_NAME, "h2")
    # Faltu headings (jaise "Contents") ko nikalne ke liye filter
    headings = [h.text.strip() for h in all_headings if h.text.strip() and "Contents" not in h.text]

    # 6. Intro Paragraphs
    paragraphs = driver.find_elements(By.CSS_SELECTOR, ".mw-parser-output > p")[:5]

    # 7. Console Output
    print("\n--- Found Headings ---")
    for heading in headings:
        print(f"-> {heading}")

    # 8. Save to File (\n fix kar diya gaya hai)
    with open("python_wikipedia.txt", "w", encoding="utf-8") as file:
        file.write("WIKIPEDIA HEADINGS:\n")
        for h in headings:
            file.write(f"- {h}\n")
        
        file.write("\nINTRO PARAGRAPHS:\n")
        for p in paragraphs:
            if p.text.strip():
                file.write(f"{p.text}\n\n")

    print("\n[Success] Data 'python_wikipedia.txt' mein save ho gaya hai.")

except Exception as e:
    print(f"[Error] Kuch masla hua hai: {e}")

finally:
    driver.quit()
    print("Browser closed.")
