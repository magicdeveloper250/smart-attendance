import cv2
import face_recognition
import threading
import os
import numpy as np
import datetime
import socketio
import time


class Recognizer(threading.Thread):
    treshold = 0.4
    path = os.getcwd()

    def __init__(self, sio, cam_ip):
        threading.Thread.__init__(self)
        self.sio: socketio.Client = sio
        self.path = "knownImages"
        self.images = []
        self.classNames = []
        self.myList = os.listdir(self.path)
        self.knownEncodings = []
        self.cam_ip = cam_ip
        self.camera = cv2.VideoCapture(self.cam_ip)

    def check_camera_status(self):
        self.camera = cv2.VideoCapture(self.cam_ip)
        success, image = self.camera.read()
        if success:
            self.sio.emit("camera_connected", True)
            return image
        else:
            time.sleep(1)
            self.check_camera_status()

    def __findEncodings(self):
        print("finding known encodings...")
        total = len(self.images)
        completed = 0
        for img in self.images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            self.knownEncodings.append(encode)
            completed += 1
            percent = int((completed * 100) / total)
            print(f"completed {percent}%")
        print("Finding encoding complete")
        print("\n")

    def __find_names(self):
        print("finding names...")
        total = len(self.myList)
        completed = 0
        for cl in self.myList:
            curImg = cv2.imread(f"{self.path}/{cl}")
            self.images.append(curImg)
            self.classNames.append(os.path.splitext(cl)[0])
            completed += 1
            percent = int((completed * 100) / total)
            print(f"completed {percent}%")
        print("Finding names complete")
        print("\n")

    def run(self):
        print("FACE RECOGNITION PROGRAM")
        print("________________________")
        print("Please wait while program is starting")
        print("1. Find names")
        print("2. Find Known image encodings")
        self.__find_names()
        self.__findEncodings()
        print("Now program is capturing")
        while True:
            success, img = self.camera.read()
            if not success:
                img = self.check_camera_status()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
                faceDist = face_recognition.face_distance(
                    self.knownEncodings, encodeFace
                )
                matchIndex = np.argmin(faceDist)
                faceMatch = faceDist[matchIndex]
                if faceMatch < self.treshold:
                    name = self.classNames[matchIndex].upper()
                    self.sio.emit("attend", name)
                    cv2.imwrite(
                        os.path.join(self.path, str(datetime.datetime.now()) + ".jpg"),
                        img,
                    )
                else:
                    name = self.classNames[matchIndex].upper()
                percentage = (1 - faceMatch) * 100
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (15, 186, 175), 4)
                cv2.rectangle(img, (x1, y2), (x2, y2 + 70), (15, 186, 175), 4)
                cv2.putText(
                    img,
                    f"{name}",
                    (x1 + 10, y2 + 30),
                    cv2.FONT_HERSHEY_COMPLEX,
                    ((x2 / (x1 + x2)) * 100) / 100,
                    (255, 255, 255),
                    2,
                )
                cv2.putText(
                    img,
                    f"{int(percentage)}%",
                    (x1 + 10, y2 + 60),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                )
            cv2.imshow("FACE RECOGNITION CAMERA", img)
            key = cv2.waitKey(1)
            if key == ord("q"):
                self.sio.emit("camera_connected", False)
                break
        self.camera.release()
        cv2.destroyAllWindows()
        self.sio.disconnect()
        print("Program terminated")
