import cv2
import numpy as np
import face_recognition
import os


# Function to find encodings of known images
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


path = "knownImages"
images = []
classNames = []
myList = os.listdir(path)

for cl in myList:
    curImg = cv2.imread(f"{path}/{cl}")
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

encodeListKnown = findEncodings(images)

print("Encoding complete")

cap = cv2.VideoCapture(r"http://192.168.0.128:81/stream")

while True:
    success, img = cap.read()

    # Check if the video capture was successful
    if not success:
        print("Failed to read frame from video stream")
        break

    # Resize and convert the image
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Detect faces in the resized image
    facesCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    # Perform face recognition and labeling
    for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
        faceDist = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDist)
        if faceDist[matchIndex] < 0.6:  # Threshold for considering a match
            name = classNames[matchIndex].upper()
            # print(name, " ", datetime.datetime.now(datetime.UTC))
        else:
            name = "Unknown"

        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(
            img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2
        )

    # Display the annotated image
    cv2.imshow("Camera", img)

    # Check for the 'q' key press to quit
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cv2.destroyAllWindows()
