# PDF-Downloader-Application

Downloading PDF Files with Python
Let’s see how we can automate downloading PDFs from Google search results. 
Code Overview
1.	Generating Google Search URL:
def generate_google_search_url(keywords, page, num_results):
    base_url = "https://www.google.com/search?q="
    encoded_keywords = "+".join(keywords.split())
    filetype_param = "filetype:pdf"
    page_param = "&start=" + str(page)
    num_param = "&num=" + str(num_results)
    return base_url + filetype_param + "+" + encoded_keywords + page_param + num_param
This function constructs a Google search URL for PDF files based on given keywords, page number, and number of results per page.
2.	Setting up Web Scraper:
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

service = Service(executable_path=ChromeDriverManager().install())
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=chrome_options)
This segment initializes the Selenium WebDriver in headless mode for automated web browsing.
3.	Extracting URLs:
all_urls = []
for i in range(5):
    search_url = generate_google_search_url("search query", 100*i, 100)
    driver.get(search_url)
    time.sleep(5)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    links = soup.find_all("a")
    urls = [link.get("href") for link in links]
    for url in urls:
        try:
            if url.startswith('http'):
                all_urls.append(url)
        except:
            pass
driver.quit()
This loop iterates through Google search result pages, 5 pages here for example, extracts URLs, and filters those that start with "http".
4.	Downloading Files:
import os
import re
import requests
import uuid
from tqdm import tqdm
import fitz  # PyMuPDF library for PDF handling

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def download_file(url, directory, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        filename = url.split("/")[-1]
        if '.' not in filename:
            filename = str(uuid.uuid4())[:8] + ".pdf"
        filename = sanitize_filename(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        try:
            doc = fitz.open(filepath)
            doc.close()
            print(f"Successfully downloaded and verified {filename} to {directory}")
        except Exception as e:
            os.remove(filepath)
            print(f"Downloaded file {filename} is not readable or corrupt. Removed from {directory}")
    except requests.RequestException as e:
        print(f"Failed to download {url}. Reason: {e}")

download_directory = "downloaded_files"
for url in tqdm(all_urls):
    download_file(url, './downloads', timeout=10)
This script downloads each PDF, sanitizes filenames, verifies their readability, and stores them in the specified directory.
By integrating these components, you can automate the retrieval of PDFs from Google search results efficiently.
