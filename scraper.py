import requests 
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
import os
import urllib.request
import pandas as pd
import ssl
import json

ssl._create_default_https_context = ssl._create_stdlib_context

class Scraper:
    def __init__(self): 
        self.data = []
        options = Options()
        options.add_argument("--window-size=1920,1200")
        options.add_argument('--disable-blink-features=AutomationControlled')
        #options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)

    def create_session(self, page=None):
        with HTMLSession() as session:
            self.session = session;
            url = f'https://carsandbids.com/past-auctions/{f"?page={page}" if page is not None else ""}'
            header = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
                'referer':'https://carsandbids.com'
            }
            response = session.get(url, headers=header)
            response.html.render(sleep=2, keep_page=True, scrolldown=1, timeout=10000)
            #response.html.render()
            print(response.html.links)
            auctions = response.html.find('.auction-item ')
            links = [auction.absolute_links for auction in auctions]
            return links

    def scrape_page(self, page=None):
        soup = self.make_request(f'https://carsandbids.com/past-auctions/{f"?page={page}" if page is not None else ""}')
        #print(soup.prettify())
        ul_tag = soup.find("ul", class_ = "auctions-list past-auctions")
        li_tags = ul_tag.find_all("li", class_ ="auction-item")


        for li in li_tags:
            data = {
                'url': li.find('a', class_='hero')['href'],
                'title': li.find('a', class_='hero')['title'],
                'image_url': li.find('img')['src'],
                #'sold_price': li.find('span', class_='bid-value').text
            }
            bid_value = li.find('span', class_='bid-value')
            if bid_value:
                data['sold_price'] = bid_value.text.strip()

            auction_subtitle = li.find('p', class_='auction-subtitle')
            if auction_subtitle:
                details = auction_subtitle.text.strip() 
                data['transmission'] = "manual" if "manual" in details.lower() else "automatic" if "automatic" in details.lower() else "Unknown"
                data['mileage'] = re.search(r'\b\d{1,3}(,\d{3})*\b miles', details, re.I)
                data['mileage'] = data['mileage'].group(0) if data['mileage'] else "Unknown"
                data['ownership'] = "Southern-Owned" if "southern-owned" in details.lower() else "Unknown"
                data['modifications'] = "modified" if "modifications" in details.lower() or "modified" in details.lower() else "Unmodified"

            self.data.append(data)

    def make_request(self, url):
        driver = self.driver
        try:
            driver.get(url)
            time.sleep(5)
            driver.execute_script("window.scrollTo(0, 2000)")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 2000)") 
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 2000)") 
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 2000)") 
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 2000)") 
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, 'html.parser') #convert the result into lxml
            return soup
        except Exception as e:
            print(e)

    def scrape(self):
        pages = range(1, 50)  # As an example, if there are 395 pages
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.scrape_page, pages)
def main():
    s = Scraper()
    s.scrape()
    print(s.data)
    with open('scraped_data.json', 'w') as outfile:
        json.dump(s.data, outfile, indent=4)


if __name__ == '__main__':
    main()