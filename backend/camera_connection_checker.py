from queue import Queue
import threading
import socketio
from PyQt5 import QtCore


class CameraConnectionThread(threading.Thread):
    def __init__(self, sio, camera_signal):
        threading.Thread.__init__(self)
        self.sio: socketio.Client = sio
        self.camera_signal: QtCore.pyqtSignal = camera_signal

    def run(self):
        @self.sio.on("connect")
        def connect():
            self.sio.emit("connect", "connected")

        @self.sio.on("disconnect")
        def disconnected():
            self.sio.emit("disconnected")

        @self.sio.on("camera_connected")
        def camera_connected(data):
            self.camera_signal.emit(data)
