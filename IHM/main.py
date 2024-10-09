from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSerialPort import *
from PyQt5 import QtWidgets 
from PyQt5 import QtCore

import Page
import sys



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bright Tack")

        # Get screen size
        screen_geometry = QDesktopWidget().screenGeometry()

        # Calculate window size (half of screen size)
        window_width = screen_geometry.width() // 2
        window_height = screen_geometry.height() // 2

        # Set window size and center it
        self.setGeometry(
            screen_geometry.width() // 2 - window_width // 2,
            screen_geometry.height() // 2 - window_height // 2,
            window_width,
            window_height
        )
        
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(Page.Page(1))
        self.stacked_widget.addWidget(Page.Page(2))
        self.stacked_widget.addWidget(Page.Page(3))
        #self.stacked_widget.addWidget(Page.Page(4))
        self.setStyleSheet("""background-color: 	#fffaf0;""")
        
        self.setCentralWidget(self.stacked_widget)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
