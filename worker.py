from PyQt5.QtCore import QThread, pyqtSignal
from search import GoogleSearch
from downloader import PDFDownloader

class Worker(QThread):
    progress = pyqtSignal(int)
    log = pyqtSignal(str)

    def __init__(self, keywords, num_pages, results_per_page, download_directory, min_pages, parent=None):
        super(Worker, self).__init__(parent)
        self.keywords = keywords
        self.num_pages = num_pages
        self.results_per_page = results_per_page
        self.download_directory = download_directory
        self.min_pages = min_pages

    def run(self):
        google_search = GoogleSearch(headless=True)
        all_urls = google_search.search(self.keywords, num_pages=self.num_pages, results_per_page=self.results_per_page)
        google_search.close()

        downloader = PDFDownloader(download_directory=self.download_directory)
        total_urls = len(all_urls)

        for i, url in enumerate(all_urls):
            self.log.emit(f"Downloading {i+1}/{total_urls}: {url}")
            downloader.download_file(url, min_pages=self.min_pages)
            self.progress.emit(int((i+1) / total_urls * 100))
            self.log.emit(f"Finished downloading {i+1}/{total_urls}")
