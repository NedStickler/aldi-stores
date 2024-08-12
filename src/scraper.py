
import requests
from bs4 import BeautifulSoup

# TODO:
# - Automated analysis of robots.txt

if __name__ == "__main__":
    root = "https://stores.aldi.co.uk/"
    res = requests.get(root)

    # Find regions
    soup = BeautifulSoup(res.text, "html.parser")
    regions_html = soup.find_all(class_="Directory-listLink")
    regions = [root + region.get("href") for region in regions_html]
    
    # Parse area and store links
    areas = []
    stores = []
    for region in regions:
        res = requests.get(region)
        soup = BeautifulSoup(res.text, "html.parser")
        areas_and_stores = soup.find_all(class_="Directory-listLink")

        for area_or_store in areas_and_stores:
            store_count = int(area_or_store.get("data-count")[1:-1]) # data-count is wrapped in brackets, hence the slice
            if store_count > 1:
                areas.append(root + area_or_store.get("href"))
            elif store_count == 1:
                stores.append(root + area_or_store.get("href"))
            else:
                raise ValueError("data-count HTML tag attribute is not greater than or equal to 1.")
    
    # Parse areas further
    for area in areas:
        res = requests.get(area)
        soup = BeautifulSoup(res.text, "html.parser")
        stores_in_area = soup.find_all(class_="Teaser-titleLink")
        for store in stores_in_area:
            stores.append(root + store.get("href")[3:]) # href includes preceding '../', hence the slice

    # Parse store information
    stores_with_info = []
    for store in stores:
        res = requests.get(store)
        soup = BeautifulSoup(res.text, "html.parser")

        store_name = soup.find(id="location-name").text
        address_line_one = soup.find(class_="Address-line1").text
        address_area = soup.find(class_="Address-city").text
        address_postcode = soup.find(class_="Address-postalCode").text
        full_address = address_line_one + ", " + address_area + ", " + address_postcode 

        stores_with_info.append([{
            "name": store_name,
            "full_address": full_address,
            "address_line_one": address_line_one,
            "address_area": address_area,
            "address_postcode": address_postcode,
            "url": store
        }])
        