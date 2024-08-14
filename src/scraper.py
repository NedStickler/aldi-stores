
import requests
import json
from bs4 import BeautifulSoup


def make_soup(url: str) -> BeautifulSoup:
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup

def snakeify(string: str) -> str:
    return string.lower().replace(" ", "_")


if __name__ == "__main__":
    root = "https://stores.aldi.co.uk/"

    # Find regions
    soup = make_soup(root)
    regions_html = soup.find_all(class_="Directory-listLink")
    regions = [root + region.get("href") for region in regions_html]
    
    # Parse area and store links
    areas = []
    stores = []
    for region in regions:
        soup = make_soup(region)
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
        soup = make_soup(area)
        stores_in_area = soup.find_all(class_="Teaser-titleLink")
        for store in stores_in_area:
            stores.append(root + store.get("href")[3:]) # href includes preceding '../', hence the slice

    # Parse store information
    stores_with_info = []
    for store in stores:
        soup = make_soup(store)

        # Name and address information
        store_name = soup.find(id="location-name").text
        address_line_one = soup.find(class_="Address-line1").text
        address_area = soup.find(class_="Address-city").text
        address_postcode = soup.find(class_="Address-postalCode").text
        full_address = address_line_one + ", " + address_area + ", " + address_postcode

        # Store service offerings
        full_services = {
            "self_checkout": False,
            "parking":  False,
            "customer_toilets": False,
            "wifi": False,
            "click_and_collect": False,
            "bakery": False,
            "electric_vehicle_charging_points": False,
            "shell_50kw_rapid_chargers": False
        }
        raw_services = soup.find_all(class_="Core-servicesListItem")
        services = [snakeify(service.text.replace("\n", "").replace("&", "and")) for service in raw_services]
        for service in full_services.keys():
            if service in services:
                full_services[service] = True

        # Store opening and closing times
        raw_hours = soup.find(class_="c-hours-details-wrapper").get("data-days")
        hours = json.loads(raw_hours)
        formatted_hours = {}
        for day in hours:
            day_name = day.get("day").lower()
            if day.get("isClosed"):
                formatted_hours[f"{day_name}_open"] = None
                formatted_hours[f"{day_name}_close"] = None
            else:
                formatted_hours[f"{day_name}_open"] = day.get("intervals")[0].get("start") / 100
                formatted_hours[f"{day_name}_close"] = day.get("intervals")[0].get("end") / 100

        # Consolidate
        store_info = {
            "name": store_name,
            "full_address": full_address,
            "address_line_one": address_line_one,
            "address_area": address_area,
            "address_postcode": address_postcode,
        }
        store_info.update(full_services)
        store_info.update(formatted_hours)
        stores_with_info.append(store_info)

    with open("./data/scraped_stores.json", "w") as f:
        json.dump(stores_with_info, f)