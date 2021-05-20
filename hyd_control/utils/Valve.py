from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QTextEdit, QPushButton, QLabel, QFileDialog
from PyQt5.QtCore import Qt
import sys
import socket

"""HEADER = 64
PORT = 12345
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "10.69.56.75"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)"""


class Valve(QWidget):
    """ Valve class
    """
    count = 0
    label_width = 122
    label_height = 153
    valve_center_radius = 17
    valve_wing_length = 37

    def __init__(self, parent=None, x_offset=0, y_offset=0, margin=5):
        """__init__
            Main constructor
        :return:None
        """
        super().__init__(parent)
        label_x = (self.label_width + margin) * x_offset + margin
        label_y = (self.label_height + margin) * y_offset + margin


        '''if y_offset ==1:
            label_x += self.label_width
        else:
            label_x += + self.label_width/2'''

        #if y_offset == 1:
        #    label_x += self.label_width + self.label_width / 2 + 2 + margin

        self.setGeometry(label_x, label_y, self.label_width, self.label_height)
        self.setStyleSheet("background-color: white;"
                           "font-size: 17px;")
        self.__create_body__()
        self.__create_footer__()
        self.id = Valve.count + 1
        self.script = ""
        self.script_path = "path"
        Valve.count += 1

        self.status = False

        self.id_label = QLabel(self)
        self.id_label.setText(str(self.id))
        self.id_label.adjustSize()
        self.id_label.move(7, 7)
        self.id_label.setStyleSheet("color: gray")

    def __create_body__(self):
        pass

    def paintEvent(self, event):
        """__paint_event__
            Function for drawing the design for each valve

            :return: None

        """
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        qp.setPen(Qt.NoPen)
        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(0, 0, self.label_width, self.label_height - 31)

        valveForm = QPainterPath()
        valveForm.moveTo(self.width() / 10, (self.height() - 31) / 2 - 1)
        valveForm.lineTo(self.width() / 4, (self.height() - 31) / 2 - 1)
        valveForm.lineTo(self.width() / 4, (self.height() - 31) / 2 - 20)
        valveForm.lineTo(self.width() / 2, (self.height() - 31) / 2 - 3)
        valveForm.lineTo(self.width() / 2, (self.height() - 31) / 2 + 3)
        valveForm.lineTo(self.width() / 4, (self.height() - 31) / 2 + 20)
        valveForm.lineTo(self.width() / 4, (self.height() - 31) / 2 + 1)
        valveForm.lineTo(self.width() / 10, (self.height() - 31) / 2 + 1)
        qp.fillPath(valveForm, QBrush(QColor("black")))

        valveForm.moveTo(self.width() * 9 / 10, (self.height() - 31) / 2 - 1)
        valveForm.lineTo(self.width() * 3 / 4, (self.height() - 31) / 2 - 1)
        valveForm.lineTo(self.width() * 3 / 4, (self.height() - 31) / 2 - 20)
        valveForm.lineTo(self.width() / 2, (self.height() - 31) / 2 - 3)
        valveForm.lineTo(self.width() / 2, (self.height() - 31) / 2 + 3)
        valveForm.lineTo(self.width() * 3 / 4, (self.height() - 31) / 2 + 20)
        valveForm.lineTo(self.width() * 3 / 4, (self.height() - 31) / 2 + 1)
        valveForm.lineTo(self.width() * 9 / 10, (self.height() - 31) / 2 + 1)
        qp.fillPath(valveForm, QBrush(QColor("black")))

        if self.status == True:
            valveForm.clear()
            valveForm.moveTo(self.width() / 4 + 4, (self.height() - 31) / 2 - 13)
            valveForm.lineTo(self.width() / 2 - 5, (self.height() - 31) / 2)
            valveForm.lineTo(self.width() / 4 + 4, (self.height() - 31) / 2 + 13)
            valveForm.moveTo(self.width() * 3 / 4 - 4, (self.height() - 31) / 2 - 12)
            valveForm.lineTo(self.width() / 2 + 5, (self.height() - 31) / 2)
            valveForm.lineTo(self.width() * 3 / 4 - 4, (self.height() - 31) / 2 + 12)
            qp.fillPath(valveForm, QBrush(QColor("white")))

        qp.end()

    def __create_footer__(self, parent=None):
        """__create_footer__
            Function for creating footer with load and print buttons

            :return:None

        """
        self.load_button = QPushButton(self)
        self.print_button = QPushButton(self)
        self.load_button.setText("Load")
        self.print_button.setText("Print")

        self.load_button.setGeometry(-1, self.height() - 30, self.width() / 2 + 1, 31)
        self.print_button.setGeometry(self.width() / 2, self.height() - 30, self.width() / 2 + 1, 31)
        self.load_button.setStyleSheet("border-top: 5px solid lightgray; "
                                       "font-size: 17px;"
                                       "border-right: 2px solid lightgray; color: black;")
        self.print_button.setStyleSheet("border-top: 5px solid lightgray; "
                                        "font-size: 17px;"
                                        "border-left: 2px solid lightgray; color: gray;background-color:lightgray")

        self.load_button.clicked.connect(lambda: self.__open_file_name_dialog__())
        self.print_button.clicked.connect(lambda: self.__print_content__())

    def __print_content__(self):
        """__print_content__
            Updates the valve nr. and the path
        :return:None
        """
        if len(self.script) > 0:
            self.parent().textArea.setText(self.script)
            self.parent().label1.setText("Valve {}".format(str(self.id)))
            self.parent().label2.setText(self.script_path)

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
            self.load_button.setStyleSheet("border-top: 5px solid lightgray;"
                                           "border-right: 2px solid lightgray; color: black; background-color: LimeGreen")
            self.print_button.setStyleSheet("border-top: 5px solid lightgray;"
                                            "border-left: 2px solid lightgray; color: black; background-color: white")

            event = "Valve {} load event : \n \n".format(self.id)
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
