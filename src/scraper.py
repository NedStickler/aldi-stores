
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# TODO:
# - Automated analysis of robots.txt

if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("https://www.tesco.com/store-locator/directory")

    stores_and_areas = driver.find_elements(By.CLASS_NAME, "Directory-listLink")
    stores = []
    areas = []

    # Sort stores and areas
    for item in stores_and_areas:
        if int(item.get_attribute("data-count")[1:-1]) == 1:
            stores.append(item.get_attribute("href"))
        else:
            areas.append(item.get_attribute("href"))

    for area in areas:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
        res = requests.get(area, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        area_stores = soup.find_all(class_="Teaser-button")
        for area_store in area_stores:
            stores.append("https://www.tesco.com/store-locator" + area_store.get("href"))