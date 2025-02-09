import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


def get_browser() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    service = Service(executable_path='src/scrapers/selenium_scrape/chrome_driver/chromedriver.exe')
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('log-level=3')
    options.binary_location = 'src/scrapers/selenium_scrape/chrome/chrome.exe'
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def scrape_all():
    browser = get_browser()
    browser.get('https://assetstore.unity.com/search#nf-ec_price_filter=0...0')
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "article[data-test='search-results-product-card-196526']")))
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()

    links = []
    titles = []

    cards = WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "a[data-test='product-card-name']")))

    for card in cards:
        links.append(card.get_attribute("href"))
        titles.append(card.text)

    results = 96
    pages = 1

    while True:
        try:
            try:
                browser.get(f'https://assetstore.unity.com/search#nf-ec_price_filter=0...0&firstResult={results}')
                browser.refresh()
                pages += 1
            except:
                break

            cards = WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "a[data-test='product-card-name']")))
            
            results += len(cards)
            
            for card in cards:
                titles.append(card.text)
                links.append(card.get_attribute('href'))
        except TimeoutException:
            break

    dictionary = dict(zip(titles, links))
    with open('src/scrapers/parse_results/result_selenium.json', 'w', encoding='utf-8') as file:
        json.dump(dictionary, file, ensure_ascii=False, indent=4)


scrape_all()
