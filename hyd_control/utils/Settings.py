from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QTextEdit, QPushButton, QLabel, QFileDialog
from PyQt5 import QtCore
import sys

class StatusBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(5, self.parent().height() - 35, self.parent().width() - 10, 30)
        self.__create_body__()
        self.__add_app_version__()
        self.__add_board_version__()

    def __create_body__(self):
        self.status_bar = QLabel(self)
        self.status_bar.resize(self.width(), self.height())
        self.status_bar.setStyleSheet("background-color: white; "
                                      "font-size: 17px;"
                                      "color: black; padding: 5")

    def __add_info__(self):
        self.ip_label = QLabel(self.status_bar)
        self.ip_label.setText("ip: " + self.parent().SERVER)
        self.ip_label.adjustSize()
        self.ip_label.setGeometry(0, 0, self.ip_label.width(), 30)

        self.port_label = QLabel(self.status_bar)
        self.port_label.setText("port: " + str(self.parent().PORT))
        self.port_label.adjustSize()
        self.port_label.setGeometry(self.ip_label.width(), 0, self.port_label.width(), 30)

    def __add_app_version__(self):
        self.app_version = QLabel(self.status_bar)
        self.app_version.setText("App version: v0.0.1")
        self.app_version.adjustSize()
        self.app_version.setGeometry(0, 0, self.app_version.width(), 30)

    def __add_status__(self):
        self.status = QLabel(self.status_bar)
        self.status.setText("Status: Off")
        self.status.adjustSize()
        self.status.setGeometry(self.ip_label.width() + self.port_label.width() + self.app_version.width(), 0, self.status.width(), 30)

    def __add_board_version__(self):
        self.board_version = QLabel(self.status_bar)
        self.board_version.setText("Board version: v0.0.1")
        self.board_version.adjustSize()
        self.board_version.setGeometry(self.app_version.width(), 0, self.board_version.width(), 30)