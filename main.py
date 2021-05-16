import time

from bs4 import BeautifulSoup
from selenium import webdriver
import requests

ZILLOW_ENDPOINT = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLScj6Zarr5KqNAmYNiOX9tAUQkno-Z26cox5GHbPoReWPI3DCg/viewform?usp=sf_link"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15",
    "Accept-Language": "en-US"
}
CHROME_DRIVER_PATH = "C:\Development\chromedriver.exe"
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

response = requests.get(ZILLOW_ENDPOINT, headers=HEADERS)
zillow_page = response.text
soup = BeautifulSoup(zillow_page, "html.parser")

card_links = soup.select(".list-card-info .list-card-link")
list_of_links = []
for link in card_links:
    list_of_links.append('https://www.zillow.com' + str(link.get("href")).split('https://www.zillow.com')[-1])
print(list_of_links)

card_addresses = soup.select(".list-card-info .list-card-link .list-card-addr")
list_of_addresses = []
for address in card_addresses:
    list_of_addresses.append(str(address.getText()))
print(list_of_addresses)

card_prices = soup.select(".list-card-info .list-card-heading .list-card-price")
list_of_prices = []
for price in card_prices:
    list_of_prices.append(price.getText())
print(list_of_prices)

for i in range(len(list_of_addresses)):
    driver.get(FORM_LINK)
    time.sleep(3)
    address_of_property = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_of_property.send_keys(list_of_addresses[i])

    price_per_month = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_per_month.send_keys(list_of_prices[i])

    link_of_property = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_of_property.send_keys(list_of_links[i])

    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span')
    submit_button.click()

