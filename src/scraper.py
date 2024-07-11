
from selenium import webdriver
from selenium.webdriver.common.by import By


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("https://www.tesco.com/store-locator/directory")

    directory_items = driver.find_elements(By.CLASS_NAME, "Directory-listLink")

    locations = []
    for item in directory_items:
        locations.append(item.get_attribute("href"))
    print(locations)