import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Constants
GOOGLE_FORM_URL = "YOUR GOOGLE FORM URL"
CITY_ZILLOW_URL = "ZILLOW URL PAGE OF RENTALS"
CHROME_DRIVER_PATH = "YOUR CHROME DRIVER PATH"

# Setting our service variable.
service = Service(CHROME_DRIVER_PATH)


class DataManager:

    def __init__(self):
        # Setting up BeautifulSoup
        self.response = requests.get(url=CITY_ZILLOW_URL, headers={"User-Agent": "YOUR USER AGENT",
                                                                   "Accept-Language": "YOUR ACCEPTED LANGUAGE SETTING"})
        self.response.raise_for_status()
        self.zillow_web_page = self.response.text
        self.soup = BeautifulSoup(self.zillow_web_page, "html.parser")
        # Setting up the selenium driver
        self.driver = webdriver.Chrome(service=service)
        self.driver.get(url=GOOGLE_FORM_URL)
        # Organising our list data
        self.link_list = []
        self.rent_list = []
        self.address_list = []

    def load_lists(self):
        links = self.soup.find_all(name="a", class_="list-card-link")
        for each_tag in links:
            if "zillow" in each_tag["href"]:
                self.link_list.append(each_tag["href"])
        prices = self.soup.find_all(name="div", class_="list-card-price")
        for each_price in prices:
            if "$" in each_price.get_text():
                if "/" in each_price.get_text():
                    just_price = each_price.get_text().split("/")
                    self.rent_list.append(just_price[0])
                elif "+" in each_price.get_text():
                    just_price = each_price.get_text().split("+")
                    self.rent_list.append(just_price[0])
        address_list = self.soup.find_all(name="address", class_="list-card-addr")
        for each_address in address_list:
            just_an_address = each_address.get_text()
            self.address_list.append(just_an_address)

    def transfer_web_scraped_data(self):

        for n in range(len(self.rent_list)):
            time.sleep(6)
            address_input = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div['
                                                               '2]/div/div[1]/div/div[1]/input')
            rental_price_input = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div['
                                                                    '2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            zillow_url_input = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div['
                                                                  '3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            submit_button = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div['
                                                               '1]/div/span/span')
            time.sleep(1)
            address_input.send_keys(self.address_list[n])
            rental_price_input.send_keys(self.rent_list[n])
            zillow_url_input.send_keys(self.link_list[n])
            time.sleep(3)
            submit_button.click()
            time.sleep(4)
            submit_again_link = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
            submit_again_link.click()


# Initialising classes
data = DataManager()

# Calling our methods
data.load_lists()
data.transfer_web_scraped_data()
