from bs4 import BeautifulSoup
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib.request
import ssl
import json

ssl._create_default_https_context = ssl._create_stdlib_context


def extract_date(date_str):
    match = re.search(r"\b(\d{1,2}/\d{1,2}/\d{2})\b", date_str)
    return match.group(1) if match else None


class Scraper:
    def __init__(self, test=False):
        self.test = test
        self.data = []
        if self.test is False:
            options = Options()
            options.add_argument("--window-size=1920,1200")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            self.driver = webdriver.Chrome(options=options)

            opener = urllib.request.build_opener()
            opener.addheaders = [
                (
                    "User-Agent",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36",
                )
            ]
            urllib.request.install_opener(opener)

    def scrape_page(self, page=None):
        soup = (
            BeautifulSoup(open("pageauction.html").read(), "html.parser")
            if self.test is True
            else self.make_request(
                f'https://carsandbids.com/past-auctions/{f"?page={page}" if page is not None else ""}'
            )
        )
        ul_tag = soup.find("ul", class_="auctions-list past-auctions")
        li_tags = ul_tag.find_all("li", class_="auction-item")
        i = 0

        for li in li_tags:
            data = {
                "url": li.find("a", class_="hero")["href"],
                "title": li.find("a", class_="hero")["title"],
                "image_url": li.find("img")["src"],
            }
            end_date = li.find("p", class_="auction-loc")
            if end_date:
                date = extract_date(end_date.text)
                if date:
                    data["end_date"] = date
            bid_value = li.find("span", class_="bid-value")
            if bid_value:
                data["sold_price"] = bid_value.text.strip()

            auction_subtitle = li.find("p", class_="auction-subtitle")
            if auction_subtitle:
                details = auction_subtitle.text.strip()
                parsed_entry = {
                    "engine": re.search(
                        r"\b((?:Twin-Turbo|Turbocharged)? ?\d+\.\d+-Liter(?: Turbodiesel)?(?: \d+-Cylinder)?|(?:Twin-Turbo|Turbocharged)? ?(?:V\d+|I\d+|Flat-\d+))\b", details
                    ),
                    "transmission": re.search(
                        r"\b(\d+-Speed Manual|Automatic|PDK)\b", details
                    ),
                    "ownership": re.search(
                        r"\b(\d+ Owner|California-Owned|Southern-Owned)\b", details
                    ),
                    "modifications": re.search(
                        r"\b(Mostly Unmodified|Some Modifications|Highly Modified)\b",
                        details,
                    ),
                    "mileage": re.search(r"~?(\d{1,3}(,\d{3})* Miles)\b", details),
                }

                for key in parsed_entry:
                    match = parsed_entry[key]
                    data[key] = match.group(0) if match else None
                
                data['extra'] = auction_subtitle.text.strip()
            self.data.append(data)
            i += 1
        print(f"Scraped {len(self.data)/page * 50} results from page {page}")

    def make_request(self, url):
        driver = self.driver
        try:
            driver.get(url)
            time.sleep(4)
            driver.execute_script("window.scrollTo(0, 2000)")
            time.sleep(2)
            """driver.execute_script("window.scrollTo(0, 2000)") 
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 2000)") 
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 2000)") 
            time.sleep(2)"""
            driver.execute_script("window.scrollTo(0, 2000)")
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            return soup
        except Exception as e:
            print(e)

    def scrape(self):
        pages = range(1, 2) if self.test is True else range(1, 397)
        for p in pages:
            self.scrape_page(p)


def main():
    s = Scraper(test=False)
    s.scrape()
    with open("scraped_data.g.json", "w") as outfile:
        json.dump(s.data, outfile, indent=4)


if __name__ == "__main__":
    main()
