from flask import Flask
from flask_socketio import SocketIO, emit
from flask import request
from flask_cors import CORS
import database
from flask import jsonify

app = Flask(__name__)
CORS(app, origins=["*"])
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/openDay", methods=["POST"])
def open_day():
    new_day = database.open_day()
    return jsonify({"day": new_day}), 201


@app.route("/attendance/<date>")
def get_attendance(date):
    attendance = database.get_attendance(date)
    return jsonify({"data": attendance}), 200


@app.route("/today", methods=["GET"])
def today():
    day = database.get_today()
    return jsonify({"day": day}), 200


@app.route("/timeStamps", methods=["GET"])
def get_timeStamps():
    time_stamps = database.get_time_stamps()
    return jsonify({"data": time_stamps}), 200


@socketio.on("connect")
def connect():
    print(f"{request.sid} connected")


@socketio.on("disconnect")
def disconnect():
    print(f"{request.sid} disconnected")


@socketio.on("attend")
def attend(regnumber):
    updated_attendance = database.check_attendance(regnumber)
    emit("attend", updated_attendance, broadcast=True, include_self=False)


@socketio.on("stream")
def stream(data):
    emit("stream", data, include_self=False, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0")
