from recognizer import Recognizer
import socketio

sio = socketio.Client()


@sio.on("connect")
def connected():
    print("conneted to the server")


sio.connect("http://localhost:5000")
recognizer = Recognizer(sio)
recognizer.start()
sio.wait()
