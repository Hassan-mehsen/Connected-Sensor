from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
import numpy as np
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import sys

"""
    This "Widget" module is created to develop several widgets with an appealing format to capture users' attention and provide them with a pleasant
    experience while using the application. Its goal is to create utility classes like buttons for managing and navigating within the application,
    ensuring they have a good design. Additionally, it includes a class to graphically display sensor data.

"""

class Button(QPushButton):
    def __init__(self,name, parent=None):
        super().__init__(name, parent)
       
    def close_main_window(self):
        for widget in QApplication.topLevelWidgets():
            widget.close()

class ButtonManager:
    @staticmethod
    def addIcon(button, icon_path):
        icon = QIcon(icon_path)
        button.setIcon(icon)
        button.setIconSize(QSize(23, 23))

class graphe(QWidget):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super(graphe, self).__init__(parent)

        # Initialisation de la figure et de l'axe
        self.figure, self.axe = plt.subplots(figsize=(width, height), dpi=dpi)
        self.canvas = FigureCanvas(self.figure)
        
        # Création de la toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        self.plot_confirmation = False
        self.x_list = [0,0]
        self.y_list = [0,0]

    def plotData(self, data1=None, data2=None,xlim=None, ylim=None):
            self.axe.clear()
            self.plot_confirmation = True

            if xlim is not None and ylim is not None:
                self.axe.set_xlim(0, xlim)
                self.axe.set_ylim(0, ylim)
    
            self.axe.set_xlabel("Temps(demi-s)")
            self.axe.set_ylabel("VIS and IR (lux)")
            self.axe.set_title("Visible and Infrared Light Intensity Over Time")

            if data1 is not None and data2 is not None  and self.plot_confirmation:
                self.x_list.append(data1)
                self.y_list.append(data2)
                self.axe.plot(self.x_list, label='Infra-red')
                self.axe.plot(self.y_list, label='Visible')
                self.axe.legend(loc='upper right', bbox_to_anchor=(1, 1))
                self.axe.grid()

            self.canvas.draw()


    def plot_history(self,list_1,list_2,xlim,ylim):

        self.axe.clear()
        self.plot_confirmation = True

        if xlim is not None and ylim is not None:
            self.axe.set_xlim(0, xlim)
            self.axe.set_ylim(0, ylim)

        self.axe.plot(list_1, label='Infra-red')
        self.axe.plot(list_2, label='Visible')
        self.axe.set_xlabel('Time(demi-seconde)')
        self.axe.set_ylabel('VIS and IR (lux)')
        self.axe.legend(loc='upper right', bbox_to_anchor=(1, 1))
        self.axe.grid()

        self.canvas.draw()
        self.plot_confirmation= False 

    def updateData(self, data1, data2):

            if data1 is not None and data2 is not None and self.plot_confirmation:
                self.x_list.append(data1)
                self.y_list.append(data2)
                self.plotData(data1, data2)
            
            if len (self.x_list) > 150:
                x= self.x_list[100]
                self.x_list = []
                self.x_list.append(x)

                y=self.y_list[100]
                self.y_list = []
                self.y_list.append(y)

                self.clearGraph()
                

            

    def clearGraph(self):
            self.plot_confirmation = False
            self.axe.clear()
            self.x_list=[None]
            self.y_list=[None]
            self.canvas.draw()

    def resize_graph(self, new_width, new_height):
            self.figure.set_size_inches(new_width, new_height)
            self.canvas.draw_idle()

class CircularButton(QPushButton):
    def __init__(self, text="", size=50, parent=None):
        super().__init__(text, parent)
        self.size = size
        self.setFixedSize(self.size, self.size)  # Set a fixed size for the button

    def sizeHint(self):
        return QSize(self.size, self.size)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(0, 128, 255))
        painter.setPen(Qt.NoPen)

        rect = self.rect()
        painter.drawEllipse(rect)

        painter.setPen(Qt.white)
        painter.drawText(rect, Qt.AlignCenter, self.text())  
 



