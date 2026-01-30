from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
import sys

class MiniBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Przeglądarka")
        self.setGeometry(100, 100, 1200, 800)

        # --- Widget centralny ---
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # --- Pasek adresu + przycisk ---
        self.top_bar = QHBoxLayout()
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Wpisz URL, np. https://www.example.com")
        self.go_button = QPushButton("Idź")
        self.go_button.clicked.connect(self.load_page)
        self.top_bar.addWidget(self.url_bar)
        self.top_bar.addWidget(self.go_button)
        self.layout.addLayout(self.top_bar)

        # --- Widok przeglądarki ---
        self.browser = QWebEngineView()
        self.layout.addWidget(self.browser)

        # --- Strona startowa ---
        self.browser.setUrl(QUrl("https://www.google.com"))

    def load_page(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MiniBrowser()
    window.show()
    sys.exit(app.exec())
