import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar, QMenu
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QUrl, QSize
from PyQt6.QtWebEngineWidgets import QWebEngineView
import multiprocessing
import os
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMessageBox
import webbrowser

pyqt_directory = os.path.dirname(os.path.abspath(__file__))

img_abs_path = os.path.join(pyqt_directory, 'static', 'img')
window_icon_path = os.path.join(img_abs_path, 'icon.png')
save_img_path = os.path.join(img_abs_path, 'save.png')
refresh_path = os.path.join(img_abs_path, 'refresh.png')
save_success_icon_path = os.path.join(img_abs_path, 'save_success.png')
open_browser_icon_path = os.path.join(img_abs_path, "open_browser.png")
class MainWindow(QMainWindow):
    def __init__(self, url, title):
        super().__init__()
        self.url = url
        self.title = title
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        width = 800
        height = 400
        if "graph_type=3" not in self.url:
            import tkinter as tk
            root = tk.Tk()
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            width = int(screen_width * 0.6)
            height = int(screen_height * 0.6)
            root.destroy()
        else:
            if "&type" in self.url:
                width = int(width / 2)


        self.setGeometry(300, 300, width, height)

        self.browser = CustomWebEngineView(self.title, self.url)
        self.browser.setUrl(QUrl(self.url))
        self.setCentralWidget(self.browser)
        self.setWindowIcon(QIcon(window_icon_path))

    def add_refresh(self):
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)
        self.toolbar.setIconSize(QSize(12, 12))
        refresh_icon = QIcon(os.path.join(img_abs_path, 'refresh.png'))
        refresh_action = QAction(refresh_icon, "Refresh", self)

        refresh_action.triggered.connect(self.browser.reload)
        self.toolbar.addAction(refresh_action)


class CustomWebEngineView(QWebEngineView):
    def __init__(self, image_name="default_image", url="http://www.google.com", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_name = image_name
        self.url = url

    def setStyle(self, context_menu):
        context_menu.setStyleSheet("""
               QMenu {
                   color: #dcdcdc; 
                   background-color: #333333; 
                   border: 1px solid #444; 
               }
               QMenu::item {
                   padding: 5px 30px 5px 20px; 
                   background-color: transparent; 
                   border-radius: 2px;
               }
               QMenu::item:selected {
                   background-color: #555555;
                   color: #ffffff; 
               }
               QMenu::item:disabled {
                   color: #777; 
               }
               QMenu::icon {
                   margin-right: 5px; 
               }
               QMenu::separator {
                   height: 1px;
                   background: #555; 
                   margin-left: 10px;
                   margin-right: 5px;
               }
               QMenu::indicator {
                   width: 13px;
                   height: 13px;
               }
               """)

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        save_action = context_menu.addAction(QIcon(save_img_path), "Save")
        save_action.triggered.connect(self.prepare_save_page_as_image)
        refresh_action = context_menu.addAction(QIcon(refresh_path), "Refresh")
        refresh_action.triggered.connect(self.reload)
        context_menu.addSeparator()
        open_browser_action = context_menu.addAction(QIcon(open_browser_icon_path), "Browser")
        open_browser_action.triggered.connect(self.open_in_browser)

        context_menu.exec(event.globalPos())
    def open_in_browser(self):
        webbrowser.open(self.url)
    def prepare_save_page_as_image(self):
        QTimer.singleShot(0, self.save_page_as_image)

    def save_page_as_image(self):
        try:
            pixmap = self.grab()
            self.capture_callback(pixmap)
        except Exception as e:
            print(f"Error in save_page_as_image: {e}")

    def save_success_message(self, image_path):
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Image Saved")
        msgBox.setText( f"The page has been saved to {image_path}")
        msgBox.setIconPixmap(QIcon(save_success_icon_path).pixmap(32, 32))
        msgBox.exec()
    def capture_callback(self, image):
        try:
            if not image.isNull():
                save_directory = os.path.join(pyqt_directory, 'img')
                image_path = save_image_with_unique_name(save_directory, self.image_name, image)
                self.save_success_message(image_path)

        except Exception as e:
            QMessageBox.critical(self, "Saving Error", f"An error occurred while saving the image: {e}")


def save_image_with_unique_name(directory, base_name, image):
    """
    Save the image with a unique name in the given directory.
    If the base_name is already taken, add an incrementing number until a unique name is found.

    :param directory: The directory where the image will be saved.
    :param base_name: The base name for the image file (without extension).
    :param image: The QPixmap image to save.
    :return: None
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    path_template = os.path.join(directory, f'{base_name}_{{}}.png')

    number = 0
    while True:
        if number == 0:
            image_path = os.path.join(directory, f'{base_name}.png')
        else:
            image_path = path_template.format(number)

        if not os.path.exists(image_path):
            image.save(image_path, "PNG")
            break

        number += 1
    return image_path

def main(url, title="display"):
    app = QApplication(sys.argv)
    mainWindow = MainWindow(url, title)
    mainWindow.show()
    sys.exit(app.exec())
def start_browser(url, title):
    main(url, title)

def start(url, title=None):
    process = multiprocessing.Process(target=start_browser, args=(url, title))
    process.start()

if __name__ == "__main__":
    start("http://www.baidu.com", "baidu.com")

