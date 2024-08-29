from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

class GoogleSearch:
    def __init__(self, headless=True):
        service = Service(executable_path=ChromeDriverManager().install())
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def generate_search_url(self, keywords, page, num_results):
        base_url = "https://www.google.com/search?q="
        encoded_keywords = "+".join(keywords.split())
        filetype_param = "filetype:pdf"
        page_param = "&start=" + str(page)
        num_param = "&num=" + str(num_results)
        return base_url + filetype_param + "+" + encoded_keywords + page_param + num_param

    def search(self, keywords, num_pages=5, results_per_page=100, wait_time=5):
        all_urls = []
        for i in range(num_pages):
            search_url = self.generate_search_url(keywords, 100*i, results_per_page)
            self.driver.get(search_url)
            time.sleep(wait_time)
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            links = soup.find_all("a")
            urls = [link.get("href") for link in links if link.get("href") and link.get("href").startswith('http')]
            all_urls.extend(urls)
        return all_urls

    def close(self):
        self.driver.quit()
