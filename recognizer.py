import cv2
import face_recognition
import threading
import os
import numpy as np
import datetime


class Recognizer(threading.Thread):
    def __init__(self, sio):
        threading.Thread.__init__(self)
        self.sio = sio
        self.path = "knownImages"
        self.images = []
        self.classNames = []
        self.myList = os.listdir(self.path)
        self.knownEncodings = []
        self.camera = cv2.VideoCapture(0)

    def findEncodings(self):
        print("finding known encodings ...")
        total = len(self.images)
        completed = 0
        for img in self.images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            self.knownEncodings.append(encode)
            completed += 1
            percent = int((completed * 100) / total)
            print(f"completed {percent}%")
        print("finding encoding complete")

    def __find_names(self):
        for cl in self.myList:
            curImg = cv2.imread(f"{self.path}/{cl}")
            self.images.append(curImg)
            self.classNames.append(os.path.splitext(cl)[0])

    def run(self):
        self.__find_names()
        self.findEncodings()
        while True:
            success, img = self.camera.read()
            # Check if the video capture was successful
            if not success:
                print("Failed to read frame from video stream")
                break
            # self.sio.emit("stream", img.tobytes())
            # Resize and convert the image
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            # Detect faces in the resized image
            facesCurFrame = face_recognition.face_locations(imgS)
            encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            # Perform face recognition and labeling
            for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
                faceDist = face_recognition.face_distance(
                    self.knownEncodings, encodeFace
                )
                matchIndex = np.argmin(faceDist)
                if faceDist[matchIndex] < 0.6:  # Threshold for considering a match
                    name = self.classNames[matchIndex].upper()
                    self.sio.emit("attend", name)
                else:
                    name = "Unknown"

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(
                    img,
                    name,
                    (x1 + 6, y2 - 6),
                    cv2.FONT_HERSHEY_TRIPLEX,
                    1,
                    (255, 255, 255),
                    2,
                )

            # Display the annotated image
            cv2.imshow("Camera", img)
            key = cv2.waitKey(1)
            if key == ord("q"):
                break
        self.camera.release()
        cv2.destroyAllWindows()
