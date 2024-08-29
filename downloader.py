import os
import re
import requests
import uuid
from tqdm import tqdm
import fitz  # PyMuPDF library for PDF handling

class PDFDownloader:
    def __init__(self, download_directory="downloaded_files"):
        self.download_directory = download_directory
        if not os.path.exists(self.download_directory):
            os.makedirs(self.download_directory)

    def sanitize_filename(self, filename):
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)[:50]
        if not sanitized.endswith('.pdf'):
            sanitized += '.pdf'
        return sanitized

    def download_file(self, url, min_pages=50, timeout=10):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            filename = url.split("/")[-1]
            if '.' not in filename:
                filename = str(uuid.uuid4())[:8] + ".pdf"
            filename = self.sanitize_filename(filename)
            filepath = os.path.join(self.download_directory, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            self.verify_pdf(filepath, min_pages)
        except requests.RequestException as e:
            print(f"Failed to download {url}. Reason: {e}")

    def verify_pdf(self, filepath, min_pages):
        try:
            doc = fitz.open(filepath)
            if doc.page_count > min_pages:
                doc.close()
                print(f"Successfully downloaded and verified {os.path.basename(filepath)}")
            else:
                doc.close()
                os.remove(filepath)
                print(f"Downloaded file {os.path.basename(filepath)} has less than {min_pages} pages. Removed.")
        except Exception as e:
            os.remove(filepath)
            print(f"Downloaded file {os.path.basename(filepath)} is not readable or corrupt. Removed.")

    def download_all(self, urls, min_pages=50, timeout=10):
        for url in tqdm(urls):
            self.download_file(url, min_pages=min_pages, timeout=timeout)
