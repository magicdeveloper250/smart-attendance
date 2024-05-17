from recognizer import Recognizer
import socketio
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

sio = socketio.Client()


@sio.on("connect")
def connected():
    print("conneted")


print("Connecting...")
sio.connect(os.environ.get("SERVER_URL"))
recognizer = Recognizer(sio)
recognizer.start()
sio.wait()
