from dotenv import load_dotenv, find_dotenv
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from recognizer import Recognizer
from camera_connection_checker import CameraConnectionThread
from queue import Queue
from PyQt5 import QtCore
import queue
import os
import socketio
import sys
import threading


load_dotenv(find_dotenv())

camera_ip = 0


class CameraIpInput(QtWidgets.QWidget):
    camera_connected = pyqtSignal(object)
    camera_status = Queue()

    def __init__(self):

        self.app = QtWidgets.QApplication(sys.argv)
        super().__init__()
        self.sio = None
        self.timer = QtCore.QTimer()
        self.cam_pool = Queue()
        self.main_program_thread = threading.Thread(target=init_main_program)
        # creating app main window and frame
        self.main_window = QtWidgets.QMainWindow()
        self.window_size = QtWidgets.QDesktopWidget().screenGeometry()
        self.main_window.setWindowTitle("Set camera ip")
        self.main_window.setFixedHeight(self.window_size.height() // 3)
        self.main_window.setFixedWidth(self.window_size.width() // 3)

        self.frame = QtWidgets.QFrame()
        # creating app main layout and its widgets
        self.layout = QtWidgets.QGridLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.messageLabel = QtWidgets.QLabel()
        self.messageLabel.setText(
            """
            - SET IP = O : if you want to use computer camera
            - SET IP = https://example.com:port/path_to_stream
            if you want to use external camera
            """
        )
        self.messageLabel.setFont(QtGui.QFont("Arial", 11, 400))
        self.label = QtWidgets.QLabel()
        self.label.setText("Enter camera IP")
        self.label.setFont(QtGui.QFont("Arial", 12, 0))
        self.ipTextInput = QtWidgets.QLineEdit()
        self.ipTextInput.setText("0")
        self.ipTextInput.setFixedHeight(50)
        self.ipTextInput.setFont(QtGui.QFont("Arial", 12, 0))
        self.savePushButton = QtWidgets.QPushButton()
        self.savePushButton.setText("connect")
        self.savePushButton.setFont(QtGui.QFont("Arial", 12, 0))
        self.savePushButton.clicked.connect(
            lambda: self.set_camera_ip(self.ipTextInput.text())
        )
        # creating confirm dialog and its widget
        self.confirm_dialog = QtWidgets.QDialog(self.main_window)
        self.confirm_layout = QtWidgets.QVBoxLayout()
        self.btn_layout = QtWidgets.QHBoxLayout()
        self.message = QtWidgets.QLabel()
        self.message.setText(
            "Your camera ip is corrrect and connected to same network as yours?"
        )
        self.confirm_btn = QtWidgets.QPushButton()
        self.confirm_btn.setText("Yes")
        self.confirm_btn.clicked.connect(
            lambda: self.confirm_ip(self.ipTextInput.text())
        )
        self.reject_btn = QtWidgets.QPushButton()
        self.reject_btn.setText("No")
        self.reject_btn.clicked.connect(lambda: self.confirm_dialog.hide())

        # adding widget to confirm dialog and setting its title
        self.confirm_dialog.setWindowTitle("Confirm deletion.")
        self.confirm_layout.addWidget(self.message)
        self.btn_layout.addWidget(self.confirm_btn)
        self.btn_layout.addWidget(self.reject_btn)
        self.confirm_layout.addLayout(self.btn_layout)
        self.confirm_dialog.setLayout(self.confirm_layout)

        # adding widget to main layout
        self.layout.addWidget(self.messageLabel, 0, 0)
        self.layout.addWidget(self.label, 1, 0)
        self.layout.addWidget(self.ipTextInput, 2, 0)
        self.layout.addWidget(self.savePushButton, 3, 0)
        self.frame.setLayout(self.layout)
        self.main_window.setCentralWidget(self.frame)
        self.camera_connected.connect(lambda data: self.update_ui(data))
        self.connect_socketio()
        self.main_window.show()
        self.app.exec_()

    def start_timer(self):
        self.timer.timeout.connect(self.update_ui)
        self.timer.setInterval(100)
        self.timer.start()

    def connect_socketio(self):
        self.sio = socketio.Client()
        self.sio.connect("http://localhost:5000")
        socketThread = CameraConnectionThread(self.sio, self.camera_connected)
        if self.sio.connected:
            socketThread.start()

    def update_ui(self, data=None):
        if data == None:
            return
        connected = data
        if connected:
            self.main_window.setWindowTitle("Camera connected")
        else:
            self.main_window.setWindowTitle("Camera disconnected")

    # slot for confirming string ip address and terminate a program
    def confirm_ip(self, ip):
        global camera_ip
        camera_ip = ip
        self.start_main()

    # slot for confiming int ip address and and confirm ip dialog if string ip provided
    def set_camera_ip(self, ip):
        global camera_ip
        if not ip:
            QtWidgets.QMessageBox.critical(None, "required", "ip address required")
        else:
            try:
                camera_ip = int(ip)
                self.start_main()
            except ValueError:
                self.confirm_dialog.show()

    def start_main(self):
        self.main_program_thread.start()
        self.start_timer()
        self.savePushButton.setEnabled(False)


def init_main_program():
    sio = socketio.Client()

    @sio.on("connect")
    def connected():
        print("connected")

    print("Connecting...")
    sio.connect(os.environ.get("SERVER_URL"))
    recognizer = Recognizer(sio, camera_ip)
    recognizer.start()
    recognizer.join()
    sio.wait()


def main():
    CameraIpInput()
    # init_main_program()


if __name__ == "__main__":

    main()
