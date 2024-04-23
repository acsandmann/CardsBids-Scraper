from bs4 import BeautifulSoup
from requests_html import HTMLSession
import cloudscraper
import undetected_chromedriver as uc 
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context


class Scraper:
    def __init__(self): 
        self.data = []
        self.scraper = None
        print('init')

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

    
    def scrape2(self):
        self.scraper = cloudscraper.create_scraper()
        with self.scraper.get('https://carsandbids.com/past-auctions/', stream=True) as x:
            c = BeautifulSoup(x.text)

            print(c.prettify())

    def scrape(self):
        driver = uc.Chrome(headless=True,use_subprocess=False)
        driver.get('https://carsandbids.com/past-auctions/')
        driver.save_screenshot('nowsecure.png')

def main():
    s = Scraper()
    s.scrape()

if __name__ == '__main__':
    main()