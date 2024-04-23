import requests 
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import urllib.request
import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context

class Scraper:
    def __init__(self): 
        self.data = []
        options = Options()
        options.add_argument("--window-size=1920,1200")
        options.add_argument('--disable-blink-features=AutomationControlled')
        # options.add_argument('--headless')
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
    
    def get(self, li):
        auction_url = li.find('a', class_='hero')['href']
        auction_title = li.find('a', class_='hero')['title']
        image_url = li.find('img')['src']
        # sold_price = li.find('span', class_='bid-value').text
        # description = li.find('p', class_='auction-subtitle').text.strip()
        # auction_end_date = li.find('p', class_='auction-loc').text.strip()
        """print("Auction URL:", auction_url)
        print("Title:", auction_title)
        print("Image URL:", image_url)
        print("Sold Price:", sold_price)
        print("Description:", description)
        print("Auction End Date:", auction_end_date)"""
        return { 'url': auction_url,  'title': auction_title }  

    def scrape(self):
        soup = self.make_request('https://carsandbids.com/past-auctions/?page=0')
        #print(soup.prettify())
        ul_tag = soup.find("ul", class_ = "auctions-list past-auctions")
        li_tags = ul_tag.find_all("li", class_ ="auction-item")


        for tag in li_tags:
            #print(tag)
            self.data.append(self.get(tag))

def main():
    s = Scraper()
    s.scrape()
    print(s.data)

if __name__ == '__main__':
    main()