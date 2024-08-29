import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QTextEdit, QFileDialog, QMessageBox, QSpinBox
from worker import Worker

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Downloader')

        layout = QVBoxLayout()

        self.keywords_label = QLabel('Keywords:')
        self.keywords_input = QLineEdit()
        layout.addWidget(self.keywords_label)
        layout.addWidget(self.keywords_input)

        self.pages_label = QLabel('Number of Pages:')
        self.pages_input = QSpinBox()
        self.pages_input.setValue(5)
        layout.addWidget(self.pages_label)
        layout.addWidget(self.pages_input)

        self.results_label = QLabel('Results per Page:')
        self.results_input = QSpinBox()
        self.results_input.setValue(100)
        layout.addWidget(self.results_label)
        layout.addWidget(self.results_input)

        self.download_folder_label = QLabel('Download Folder:')
        self.download_folder_button = QPushButton('Select Folder')
        self.download_folder_button.clicked.connect(self.select_folder)
        self.download_folder_display = QLabel('')
        layout.addWidget(self.download_folder_label)
        layout.addWidget(self.download_folder_button)
        layout.addWidget(self.download_folder_display)

        self.min_pages_label = QLabel('Minimum PDF Pages:')
        self.min_pages_input = QSpinBox()
        self.min_pages_input.setValue(50)
        layout.addWidget(self.min_pages_label)
        layout.addWidget(self.min_pages_input)

        self.start_button = QPushButton('Start Download')
        self.start_button.clicked.connect(self.start_download)
        layout.addWidget(self.start_button)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.download_folder_display.setText(folder)

    def start_download(self):
        keywords = self.keywords_input.text()
        num_pages = self.pages_input.value()
        results_per_page = self.results_input.value()
        download_directory = self.download_folder_display.text()
        min_pages = self.min_pages_input.value()

        if not keywords or not download_directory:
            QMessageBox.warning(self, "Input Error", "Please provide all required inputs")
            return

        self.worker = Worker(keywords, num_pages, results_per_page, download_directory, min_pages)
        self.worker.progress.connect(self.update_progress)
        self.worker.log.connect(self.update_log)
        self.worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_log(self, message):
        self.log_output.append(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
