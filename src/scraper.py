
from selenium import webdriver
from selenium.webdriver.common.by import By


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("https://www.tesco.com/store-locator/directory")

    directory_items = driver.find_elements(By.CLASS_NAME, "Directory-listLink")

    stores = []
    locations = []
    for item in directory_items:
        if int(item.get_attribute("data-count")[1:-1]) == 1:
            stores.append(item.get_attribute("href"))
        else:
            locations.append(item.get_attribute("href"))
    
    for location in locations:
        driver.get(location)
        location_stores = driver.find_elements(By.CLASS_NAME, "Teaser-button")
        for location_store in location_stores:
            stores.append(location_store.get_attribute("href"))
