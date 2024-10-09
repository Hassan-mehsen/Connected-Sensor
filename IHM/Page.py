from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout, QSpacerItem, QSizePolicy, QDesktopWidget,QScrollArea,QDialog
from PyQt5.QtGui import QPixmap, QIcon 
from PyQt5.QtCore import Qt, QSize, QRect, QPropertyAnimation, QTimer
from PyQt5 import QtCore, QtGui, QtWidgets

import sys
import widget
import serial_link
import time
from datetime import datetime



class Page(QWidget):

    """
        This module is designed to create a sidebar navigation bar and different pages containing widgets, ultimately serving the user. 
        The graphical interface is kept simple, with each feature of this GUI housed on its own specific page. Users can navigate between these pages using 
        the sidebar, activate links, and animate buttons.
    """
    def __init__(self, page_number):
        super().__init__()
        

        # intialize the serial communication 
        self.port_name="/dev/ttyACM0"
        self.baude_rate=115200
        self.serial_link=serial_link.serial_link(self.port_name,self.baude_rate)
        self.serial_link.serialReadThread()

        # this variable is for setting the bulb photo in a fonction of IR value
        self.presence = False
        
        # Button size
        button_width = 110
        button_height = 40
        extra_space = 15
        container_width = button_width + extra_space
        
        # Container widget for navigation buttons
        button_container = QWidget()
        button_container.setFixedWidth(container_width)
        button_layout = QVBoxLayout(button_container)
        
        
        # Add a label and putting a icon inside these label
        header_label = QLabel(" ")
        header_label.setMaximumSize(QSize(75, 75))
        pixmap = QPixmap("embarquer_icon/Robot.png")  
        header_label.setPixmap(pixmap)
        button_layout.addWidget(header_label)

        # Add space between the label and navigation buttons
        button_layout.addSpacerItem(QSpacerItem(15, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)) 

        # set the style of the navigation bar (button_container)
        button_container.setStyleSheet("""
                                    QPushButton{     
                                                     background-color: #007099;
                                                     border : none ; 
                                                     padding-left:20px;   
                                                     height:40px;   
                                                     border-radius: 12px; 
                                                     text-align:left; 
                                                     color : white;
                                                     font-size: 15px 
                                                }
                                    
                                       
                                    QWidget {background-color: #007099;  padding: 5px; border-radius: 15px; color:white }
                            
                                       
                                                """)
        
        # create the buttons an adding them to to the navigation bar
        self.create_buttons(button_layout, button_width, button_height)
        
        # Add flexible space between navigation buttons and the footer button
        button_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Add a button at the bottom of the VBox
        footer_button = widget.Button("Exit")
        footer_button.setFixedSize(button_width, button_height)
        footer_button.clicked.connect(footer_button.close_main_window)
        widget.ButtonManager.addIcon(footer_button,"embarquer_icon/exit.png")
        button_layout.addWidget(footer_button)

        # Main layout for the page content
        main_layout = QHBoxLayout()
        page_layout = QHBoxLayout()
        self.title_layout = QVBoxLayout()
        self.center_layout = QVBoxLayout()

        # widgets of page 1
        if page_number == 1:
            #Building A World More Connected !
            self.title_label = QLabel("""                                                 
SI1151 Grove Sensor Application
                                 
With this app you can :
                                      
                                 
    \u2022 Measure The IR and Visibale Light
                                      
    \u2022 Detect The presence of a human
                                      
    \u2022 View the data in real-time and other features
                                 

We wish you a perfect exprience !
                                                                                                                                  
                                                                                                                         
The ProEmbed Team
                                 """)
            
            self.title_label.setStyleSheet(  
                                        "font-size : 20px ;"
                                        " color : #007099;"
                                        "font-weight : bold;"
                                        "text-align: center;"
                                        "padding-left:10px;"
                                        
                                   )
            self.title_label.setAlignment( Qt.AlignLeft)
            hbox=QHBoxLayout()
            hbox.addWidget(self.title_label)
            hbox.addSpacerItem(QSpacerItem(300,0, QSizePolicy.Expanding, QSizePolicy.Minimum))
            self.title_layout.addSpacerItem(QSpacerItem(0, 50, QSizePolicy.Minimum, QSizePolicy.Fixed))
            self.title_layout.addLayout(hbox)
            
         
            # Placeholder for photo in Page 1
            photo_label = QLabel()
            pixmap = QPixmap("embarquer_icon/IR.png")  
            photo_label.setPixmap(pixmap)
            photo_label.setAlignment(Qt.AlignRight| Qt.AlignBottom )  # Align to bottom right
            self.title_layout.addWidget(photo_label)
            page_layout.addLayout(self.title_layout)
          

        # widgets of page 2
        elif page_number == 2:
            # Add buttons for robot control in Page 2
            self.hzbox=QHBoxLayout()
            self.ampoule_off_photo = QLabel()
            pixmap = QPixmap("embarquer_icon/ampoule.png")  
            self.ampoule_off_photo.setPixmap(pixmap)
            self.ampoule_off_photo.setAlignment(Qt.AlignLeft| Qt.AlignCenter )  # Align to bottom right
            self.hzbox.addWidget(self.ampoule_off_photo)

            self.ampoule_on_photo = QLabel()
            pixmap = QPixmap("embarquer_icon/ampoule_on.png")  
            self.ampoule_on_photo.setPixmap(pixmap)
            self.ampoule_on_photo.setAlignment(Qt.AlignLeft| Qt.AlignCenter )  # Align to bottom right
            self.hzbox.addWidget(self.ampoule_on_photo)
            
            self.ampoule_off_photo.setHidden(self.presence)
            self.ampoule_on_photo.setHidden(not self.presence)

            self.hzbox.addSpacerItem(QSpacerItem(150,0, QSizePolicy.Fixed, QSizePolicy.Minimum))
            self.create_measure_button(self.hzbox)
            page_layout.addLayout(self.hzbox)

        #widget for page 3
        elif page_number == 3:
            #horizental layout to adjust the position of the toolbar and the plot and clear button on the same lign
            horzbox=QHBoxLayout()
            # add a self.graphe to plot the data in a function of real time
            self.graphe = widget.graphe() #111 
            self.plot_button=widget.CircularButton("Plot",70) 
            self.clear_button=widget.CircularButton("Clear",70)
            self.save_button=widget.CircularButton("Save",70)
            self.history_button = widget.CircularButton("History",70)
            self.export_data_button = widget.CircularButton("""Export                          
as CSV""",70)
            self.plot_history_button = widget.CircularButton("""Plot                          
History""",70)
            self.plot_button.clicked.connect(self.plot) #111
            self.clear_button.clicked.connect(self.graphe.clearGraph) #111
            self.save_button.clicked.connect(self.start_Save)
            self.history_button.clicked.connect(self.show_data)
            self.export_data_button.clicked.connect(self.export_as_csv)
            self.plot_history_button.clicked.connect(self.plot_history)

             # sleep 5 s to enure that the application has received all the data from the robot and save it in the csv file
            time.sleep(1)
            
            #setting a timer to update data on the self.graphe 
            self.data_timer = QTimer()
            self.data_timer.start(1000) 
            

            self.plot_button.setStyleSheet("""

                                            background-color: #007099;
                                            border : none ; 
                                            padding-left:20px;   
                                            height:40px;   
                                            border-radius: 12px; 
                                            text-align:left; 
                                            color : white;
                                            font-size: 15px
                                           
                                            """)
            
            horzbox.addWidget(self.graphe.toolbar)
            horzbox.addSpacerItem(QSpacerItem(0,0, QSizePolicy.Fixed, QSizePolicy.Minimum))
            horzbox.addWidget(self.plot_button)
            horzbox.addWidget(self.clear_button)
            horzbox.addWidget(self.save_button)
            horzbox.addWidget(self.history_button)
            horzbox.addWidget(self.export_data_button)
            horzbox.addWidget(self.plot_history_button)
            self.title_layout.addLayout(horzbox)
            self.title_layout.addWidget(self.graphe.canvas)
            page_layout.addLayout(self.title_layout)

        # Add layouts to the main horizontal layout
        main_layout.addWidget(button_container)
        main_layout.addLayout(page_layout)

        # setting the main layout of the widget
        self.setLayout(main_layout)

    # function to create the buttons of the navigation bar
    def create_buttons(self, layout, width, height):
        button1 = QPushButton("Home")
        button1.setFixedSize(width, height)
        button1.clicked.connect(lambda: self.parentWidget().setCurrentIndex(0))
        widget.ButtonManager.addIcon(button1,"embarquer_icon/home.png")
        layout.addWidget(button1)

        layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        button2 = QPushButton("Measure")
        button2.setFixedSize(width, height)
        button2.clicked.connect(lambda: self.parentWidget().setCurrentIndex(1))
        widget.ButtonManager.addIcon(button2,"embarquer_icon/measure.png")
        layout.addWidget(button2)

        # Increase space between buttons
        layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        button3 = QPushButton("Data")
        button3.setFixedSize(width, height)
        button3.clicked.connect(lambda: self.parentWidget().setCurrentIndex(2))
        widget.ButtonManager.addIcon(button3,"embarquer_icon/data.png")
        layout.addWidget(button3)

        layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        


    def create_measure_button(self,layout):
        self.button_IR = widget.CircularButton("""Recover 
IR value""")  # Up
        self.button_VIS = widget.CircularButton("""Recover 
VIS value""")  # Stop
        self.button_IR_value = widget.CircularButton("""press the 
button below""")  # Left
        self.button_VIS_value = widget.CircularButton("""press the 
button below""")  # Right
        
        self.button_IR.setFixedSize(125,125)
        self.button_VIS.setFixedSize(125,125)
        self.button_IR_value.setFixedSize(125,125)
        self.button_VIS_value.setFixedSize(125,125)


        self.button_IR.clicked.connect(self.switch_bulb_onPresence)
        self.button_IR.clicked.connect(self.show_IR_value)
        self.button_VIS.clicked.connect(self.show_VIS_value)

        
        grid_layout = QGridLayout()


        grid_layout.addWidget(self.button_IR, 0, 0, Qt.AlignCenter|Qt.AlignRight)
        grid_layout.addWidget(self.button_VIS, 0,3, Qt.AlignCenter|Qt.AlignRight)
        grid_layout.addWidget(self.button_IR_value, 3, 0, Qt.AlignCenter|Qt.AlignRight)
        grid_layout.addWidget(self.button_VIS_value, 3, 3, Qt.AlignCenter|Qt.AlignRight)
        grid_layout.setVerticalSpacing(50)


        layout.addLayout(grid_layout)
        layout.setAlignment(Qt.AlignCenter)


    def switch_bulb_onPresence(self):

        """
        for i in range (self.serial_link.List_size):
            try:
                if int(self.serial_link.IR_List[i]) > 380:
                    self.ampoule_off_photo.setHidden(not self.presence)
                    self.ampoule_on_photo.setHidden( self.presence)
                    break

                else : 
                    self.ampoule_off_photo.setHidden(self.presence)
                    self.ampoule_on_photo.setHidden(not self.presence)
            except ValueError :
                print(f"Élément non convertible en entier : {self.serial_link.IR_List[i]}")
        """

        
        try:
                if self.serial_link.IR_current_value > 100:
                    self.ampoule_off_photo.setHidden(not self.presence)
                    self.ampoule_on_photo.setHidden( self.presence)
                   
                else : 
                    self.ampoule_off_photo.setHidden(self.presence)
                    self.ampoule_on_photo.setHidden(not self.presence)

        except ValueError :
                print(f"Élément non convertible en entier : {self.serial_link.IR_current_value}")

    def show_IR_value(self):
        
        self.button_IR_value.setText(str(self.serial_link.IR_current_value))


    def show_VIS_value(self):

        self.button_VIS_value.setText(str(self.serial_link.VIs_current_value))

    def start_Save(self):
         self.data_timer.timeout.connect(lambda:(self.serial_link.save_data_to_db()))




    def show_data(self):
        data = self.serial_link.get_all_data()

        if data is not None:
            dialog = QDialog(self)
            dialog.setWindowTitle("Données de la table SI1151")

            layout = QVBoxLayout()
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)

            content_widget = QWidget()
            scroll_area.setWidget(content_widget)

            grid_layout = QGridLayout()
            content_widget.setLayout(grid_layout)

            grid_layout.addWidget(QLabel("Date de Mesure"), 0, 0)
            grid_layout.addWidget(QLabel("Valeur Infrarouge"), 0, 4)
            grid_layout.addWidget(QLabel("Valeur Visible"), 0, 8)

            row_index = 1
            for row in data:
                date_creation = row[1]
                infrared_value = row[2]
                visible_value = row[3]

                grid_layout.addWidget(QLabel(str(date_creation)), row_index, 0)
                grid_layout.addWidget(QLabel(str(infrared_value)), row_index, 4)
                grid_layout.addWidget(QLabel(str(visible_value)), row_index, 8)

                row_index += 1

            layout.addWidget(scroll_area)

            close_button = QPushButton("Fermer")
            close_button.clicked.connect(dialog.close)
            layout.addWidget(close_button)

            dialog.setLayout(layout)
            dialog.exec_()


    def export_as_csv(self):
         self.serial_link.export_data()


    def plot_history(self):
         
        data = self.serial_link.get_all_data()
        ir  = []
        vis = []
        x_lim = 0
        if data is not None:
            for row in data :
                ir.append(int(row[2]))
                vis.append(int(row[3]))
                x_lim += 1

        while len(ir) != len(vis) :

            if (len(ir) > len(vis)) :
                del ir[-1]

            elif (len(ir) < len(vis)) :
                del vis[-1]
            
        print("irrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr : ",ir)
        print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvviiiiis : ",vis)

        self.graphe.clearGraph()
        self.graphe.plot_history(ir,vis,x_lim,800)
        
    def plot(self):
        self.plot_button.clicked.connect(lambda:self.graphe.plotData(self.serial_link.IR_current_value,self.serial_link.VIs_current_value,100,750)) #111
        self.data_timer.timeout.connect(lambda:self.graphe.updateData(self.serial_link.IR_current_value,self.serial_link.VIs_current_value))   #1111
