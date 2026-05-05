from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

try:
    # browser start with auto-managed ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # open Wikipedia
    driver.get("https://en.wikipedia.org")

    # wait setup
    wait = WebDriverWait(driver, 15)

    # search box wait until clickable (current Wikipedia selector)
    search = wait.until(EC.element_to_be_clickable((By.ID, "searchInput")))

    # search and enter (clear + click to fix interactability)
    search.clear()
    search.click()
    search.send_keys("Python programming")
    search.send_keys(Keys.RETURN)

    # wait for article page load
    wait.until(EC.any_of(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h1 span.mw-headline")), 
        EC.url_contains("Python_(programming_language)")
    ))

    # relevant headings filter
    all_headings = driver.find_elements(By.TAG_NAME, "h2")
    headings = [h for h in all_headings if h.text and h.text.strip() and len(h.text.strip()) > 3 and "Contents" not in h.text]

    # intro paragraphs
    paragraphs = driver.find_elements(By.CSS_SELECTOR, ".mw-parser-output > p")[:10]

    # console output
    print("Relevant H2 Headings from Python (programming language):")
    for heading in headings:
        print(f"- {heading.text}")

    # save to file
    with open("python_wikipedia.txt", "w", encoding="utf-8") as file:
        file.write("Headings:\\n")
        for heading in headings:
            file.write(heading.text + "\\n\\n")
        file.write("Intro Paragraphs:\\n")
        for p in paragraphs:
            file.write(p.text + "\\n\\n")

    print("Data saved to python_wikipedia.txt")
finally:
    driver.quit()
    print("Browser closed successfully.")
