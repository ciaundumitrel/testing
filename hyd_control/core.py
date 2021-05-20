import re
import time

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QTextEdit, QPushButton, QLabel, QFileDialog,QDialog,\
    QInputDialog
from PyQt5.QtCore import Qt
import sys
from utils.Piston import Piston
from utils.Valve import Valve
from utils.Settings import StatusBar
import socket
import threading

class Window(QMainWindow):
    def __init__(self):
        self.HEADER = 64
        self.PORT = 12345
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SERVER = "10.69.56.171"
        self.ADDR = (self.SERVER, self.PORT)

        self.connected = False
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        self.__check_connection__()

        super().__init__()
        self.resize(1275, 750)
        self.setStyleSheet("background-color: lightgray")
        self.piston = Piston(self)
        self.valves = []

        self.textArea = QTextEdit(self)
        self.textArea.setText("No text to be displayed yet.")
        self.textArea.setGeometry(int(self.width()/2) + 3, 321, int(self.width()/2) - 7, int(self.height() - 391))
        self.textArea.setReadOnly(True)
        self.textArea.setLineWrapMode(QTextEdit.WidgetWidth)
        self.textArea.setStyleSheet("background-color: white; "
                                    "font-size: 17px;"
                                    "border: 0px solid black;")

        self.__create_valves__()
        self.piston.__display__()
        self.__details__()
        self.settings = StatusBar(self)

        self.__ip_widget__()
        thread = threading.Thread(target=self.__receive_message__)
        thread.start()

    def closeEvent(self, event):
        client.close()

    def __check_connection__(self):
        try:
            send_length = str(len("[CONNECTION_CHECK]")).encode('utf-8')
            send_length += b' ' * (64 - len(send_length))
            self.client.send(send_length)
            self.client.send(bytes("[CONNECTION_CHECK]", "UTF-8"))
            self.connected = True
        except socket.error:
            self.connected = False

    def __ip_widget__(self):
        self.config = QLabel(self)
        self.config.setGeometry(Valve.label_width * 7 + 5 * 8, Valve.label_height + 10, Valve.label_width * 3 + 10, Valve.label_height)
        self.config.setStyleSheet("background-color: white")
        self.ip_label = QLabel(self.config)
        self.ip_label.move(7, 7)
        self.ip_label.setText("IP : {}".format(str(self.SERVER)))
        self.ip_label.setStyleSheet("font-size:17px;"
                                    "color: black")
        self.port_label = QLabel(self.config)
        self.port_label.setText("PORT : {}".format(str(self.PORT)))
        self.port_label.move(7, 7 + self.ip_label.height())
        self.port_label.setStyleSheet("font-size:17px;"
                                      "color: black;")

        self.status_label = QLabel(self.config)
        self.status_label.setText("STATUS : ON")
        self.status_label.move(7, 7 + self.port_label.height() + self.port_label.height())
        self.status_label.setStyleSheet("font-size: 17px;"
                                        "color: black")

        button = QPushButton(self.config)
        button.setGeometry(-1, Valve.label_height - 31, self.config.width() + 2, 31)
        button.setStyleSheet("border-top: 5px solid lightgray; font-size: 17px;")
        button.setText("Set IP/PORT")
        button.clicked.connect(lambda: self.__dialog__())

    def paintEvent(self, event):
        """paintEvent
            Updates Status Colored Circle
        :return:None
        """
        w = self.status_label.width()
        h = self.status_label.height()
        pix = QPixmap(w, h)
        qp = QPainter(pix)

        pix.fill(Qt.white)
        qp.setRenderHint(QPainter.Antialiasing)
        qp.setPen(Qt.NoPen)

        qp.setBrush(QColor("Tomato"))
        if (self.connected):
            qp.setBrush(QColor("LimeGreen"))
        qp.setPen(Qt.black)
        qp.setFont(QFont("MS Shell Dlg 2", 10))
        qp.drawText(0, h - 5, "STATUS : ")
        qp.setPen(Qt.NoPen)
        qp.drawEllipse(w - h, 0, self.status_label.height() - 1, self.status_label.height() - 1)

        qp.end()
        self.status_label.setPixmap(pix)

    def __dialog__(self):
        text, ok = QInputDialog.getText(self.config, 'Set IP',
                                        'Enter IP:')
        text2, ok = QInputDialog.getText(self.config, 'Set PORT',
                                        'Enter PORT:')

        if ok:
            self.ip_label.setText("IP : {}".format(text))
            self.SERVER = text
            self.port_label.setText("PORT: {} ".format(text2))
            self.PORT = int(text2)
            self.ADDR=(self.SERVER, self.PORT)
            self.client.close()

            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.ADDR)
            self.__check_connection__()

    def __receive_message__(self,):
        while True:
            command_length = self.client.recv(64).decode('utf-8')
            if command_length:
                command_length = int(command_length)
                self.command = self.client.recv(command_length).decode('utf-8')
                if self.command == "!DISCONNECT":
                    connected = False
                self.__analyze_command__()

    def __analyze_command__(self):
        if "valve" in self.command:
            print("this is a command involving valves")
            valve_id=-1
            for i in self.command.split():
                if i.isdigit():
                    valve_id = i
            print(valve_id)
            if valve_id != -1:
                if "open" in self.command:
                    self.valves[int(valve_id)-1].status = True
                elif "close" in self.command:
                    self.valves[int(valve_id)-1].status = False

            self.valves[int(valve_id)-1].update()

        elif "piston" in self.command:
            print("this is a command involving the piston")
            if "open" in self.command:
                self.piston.status = True
            elif "close" in self.command:
                self.piston.status = False

        elif "set bars" in self.command:
            print("this is a command involving the bars")
            bars = 0.0
            for i in self.command.split():
                try:
                    # trying to convert i to float
                    bars = float(i)
                    # break the loop if i is the first string that's successfully converted
                    break
                except:
                    continue
            self.piston.__set_bars__(bars)

        elif "quit" in self.command:
            print("exit")
        else:
            print("Retry! \n Existing command: open valve | close valve | open piston | close piston | set bars | quit")

    def __create_valves__(self):
        """__create_valves__
            Displaying the valve

        :return:None
        """
        total_valves = 17
        for j in range(2):
            for i in range(10):
                if Valve.count < total_valves:
                    self.valves.append(Valve(self, i, j))

    def __details__(self):
        """__details__
            Function for displaying the name and path for each corresponding script

        :return:None
        """
        self.label1 = QLabel(self)
        self.label1.setText("Valve 14")
        self.label1.setStyleSheet("border-right: 5px solid lightgray;"
                                  "border-top: 5px solid lightgray;"
                                  "background-color: white;"
                                  "font-size: 17px;")
        self.label1.setGeometry(self.textArea.x(), self.textArea.y() + self.textArea.height(), 75, 30)

        self.label2 = QLabel(self)
        self.label2.setGeometry(self.textArea.x() + self.label1.width(), self.textArea.y() + self.textArea.height(), self.textArea.width() - self.label1.width(), 30)
        self.label2.setStyleSheet("border-top: 5px solid lightgray;"
                                  "background-color: white;"
                                  "font-size: 17px;")
        self.label2.setText("path")

    def __settings_widget__(self):
        """__setting_widget__
            Function to display the port and the IP address
        :return:None
        """
        label = QLabel(self)
        port = QLabel(label)
        ip = QLabel(label)
        port.setText("12345")
        ip.setText("192.160.0.0")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
