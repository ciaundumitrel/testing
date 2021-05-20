from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QTextEdit, QPushButton, QLabel, QFileDialog
from PyQt5 import QtCore
import socket
import sys
import time

"""HEADER = 64
PORT = 12345
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "10.69.56.75"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)"""


class Piston(QWidget):
    """
    Piston class
    """

    def __init__(self, parent=None):
        """ Constructor

            :param parent:
        """
        self.bars = 0.0
        self.script = ""
        self.script_path = "path"
        super().__init__(parent)

    def __display__(self):
        """__display__
            Main function for displaying the piston widget
        :return:None
        """

        self.setGeometry(5, 321, self.parent().width()/2 - 7, self.parent().height() - 361)
        self.piston_label = QLabel("", self)
        self.piston_label.setGeometry(0, 0, self.width(), self.height())
        self.piston_label.setStyleSheet("background-color: white; border: none")
        self.setStyleSheet("background-color: white; font-size: 17px;")

        self.pressure_label = QLabel("Pressure : " + str(self.bars) + " bars", self.piston_label)
        self.pressure_label.setGeometry(0, self.height() - 30, self.width() / 4 + 5, 30)
        self.pressure_label.setStyleSheet("border-top: 5px solid lightgray;"
                                          "border-right: 5px solid lightgray;"
                                          "font-size: 17px;")

        self.print_button_piston = QPushButton("Print file", self.piston_label)
        self.print_button_piston.setGeometry(self.width() * 3 / 4, self.height() - 30, self.width() / 4 + 1, 30)
        self.print_button_piston.setStyleSheet("border-top: 5px solid lightgray;"
                                               "border-left: 2.5px solid lightgray;"
                                               "color: gray;"
                                               "background-color: lightgray;"
                                               "font-size: 17px;")

        self.load_button_piston = QPushButton("Load file", self.piston_label)
        self.load_button_piston.setGeometry(self.width() / 2, self.height() - 30, self.width() / 4, 30)
        self.load_button_piston.setStyleSheet("border-top: 5px solid lightgray;"
                                              "border-right: 2.5px solid lightgray;"
                                              "border-left: 5px solid lightgray;"
                                              "color: black;"
                                              "font-size: 17px;")

        self.load_button_piston.clicked.connect(self.__open_file_name_dialog__)
        self.print_button_piston.clicked.connect(lambda: self.__print_content__())
        self.status = False

        # self.__create_text_area__()
        # self.__spin_box__()
        self.__create_piston_image__()

    def __create_piston_image__(self):
        """__create_piston_image__
            Drawing the piston
            :return:None
        """
        piston_image1 = QPixmap('utils/img/p1.png')
        self.image_label1 = QLabel(self.piston_label)
        self.image_label1.setPixmap(piston_image1)
        self.image_label1.move(-305, 60)
        self.image_label1.setStyleSheet("border:0px")
        piston_image2 = QPixmap('utils/img/p2.png')
        self.image_label2 = QLabel(self.piston_label)
        self.image_label2.setPixmap(piston_image2)
        self.image_label2.move(-630 , 67)
        self.image_label2.setStyleSheet("border:0px")

    def __open_file_name_dialog__(self):
        """__open_file_name_dialog
            Opens the dialog for selecting a file
            :return :None
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                        "All files (*);;Python Files (*.py)", options=options)
        if self.file_name:
            self.f = open(self.file_name, "r")
            self.script = self.f.read()
            self.script_path = str(self.file_name)
            self.load_button_piston.setStyleSheet("border-top: 5px solid lightgray;"
                                                  "border-right: 5px solid lightgray;"
                                                  "background-color: LimeGreen;"
                                                  "border-left: 5px solid lightgray;"
                                                  "font-size: 17px;")
            self.print_button_piston.setStyleSheet("border-top: 5px solid lightgray;"
                                                  "background-color: white;"
                                                   "font-size: 17px;")

            event = "Piston load event : \n \n"
            event = event.encode(self.parent().FORMAT)
            msg_length = len(event)
            send_length = str(msg_length).encode(self.parent().FORMAT)
            send_length += b' ' * (64 - len(send_length))

            self.parent().client.send(send_length)
            self.parent().client.send(event)

            script = self.script.encode(self.parent().FORMAT)
            msg_length = len(script)
            send_length = str(msg_length).encode(self.parent().FORMAT)
            send_length += b' ' * (64 - len(send_length))

            self.parent().client.send(send_length)
            self.parent().client.send(script)


    def __create_text_area__(self):
        """__create_text_area__
            Creates the text area

        :return:None
        """
        self.textArea = QTextEdit(self)
        self.textArea.resize(500, 300)
        self.textArea.move(500, 10)
        self.textArea.setReadOnly(True)
        self.textArea.setLineWrapMode(QTextEdit.NoWrap)
        self.textArea.setStyleSheet("font-size: 17px;")

    def __print_content__(self):
        """__print_content__
                    Updates the valve nr. and the path
                :return:None
        """
        if len(self.script) > 0:
            self.parent().textArea.setText(self.script)
            self.parent().label1.setText("Piston")
            self.parent().label2.setText(self.script_path)

    def __move_piston__(self):
        if 10.0 >= float(self.bars) >= 0.0:
            while self.image_label2.x() != float(self.bars)*45-630:
                interpolant = 0.1
                new_position = int(self.__lerp__(self.image_label2.x(), float(self.bars)*45-630, interpolant))
                self.image_label2.move(new_position, 67)
                if abs(self.image_label2.x() - (float(self.bars) * 45 - 630)) < 10.0:
                    self.image_label2.move(float(self.bars) * 45 - 630, 67)
                time.sleep(0.005)

    def __lerp__(self, a, b, t):
        return a + (b - a) * t

    def __set_bars__(self, bars):
        """__set_bars__
        Sets the value for bars
        :return:
        """
        self.bars = float(bars)
        self.pressure_label.setText("Pressure : " + str(self.bars) + " bars")
        self.__move_piston__()

