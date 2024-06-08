import cv2
import time
import datetime
import cv2.data
import face_recognition
import numpy as np
import threading

camera = cv2.VideoCapture(0)
time_elapsed = 0
start_time = int(time.time())
prev_time = set()
frames = []
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")
faces_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def is_smile(face, landmarks):
    left_lip_edge = np.array(landmarks["top_lip"][0])
    right_lip_edge = np.array(landmarks["top_lip"][6])
    lips_width = np.abs(left_lip_edge[0] - right_lip_edge[0])
    face_width = np.abs(landmarks["chin"][2][0] - landmarks["chin"][14][0])
    return lips_width / face_width >= 0.5


def detect_smile(img, landmarks_collection):
    frame = img.copy()
    smiles = []
    for landmarks in landmarks_collection:
        smiled = is_smile(frame, landmarks)
        smiles.append(smiled)
    return frame, smiles


def process_frames(frames, img):
    results = []
    count = 0

    for frame in frames:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = faces_cascade.detectMultiScale(
            rgb, scaleFactor=1.3, minNeighbors=2, minSize=(100, 100)
        )
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # detecting smiles from detected faces
        # text = ""
        # detect smile
        for x, y, w, h in faces:
            # drawing a rectangle over the face
            cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 255, 0), 2)
            # face_gray = gray[y : y + h, x : x + w]
            # smiles = smile_cascade.detectMultiScale(
            #     face_gray, scaleFactor=1.8, minNeighbors=20
            # )
            landmarks = face_recognition.face_landmarks(frame)
            img, smiles = detect_smile(frame, landmarks)
            if any(smiles):
                results.append([count, True])
            else:
                results.append([count, False])
        count += 1

    print(results)


while True:
    t = len(prev_time)
    prev_time.add(time_elapsed)
    time_elapsed = int(time.time() - start_time)
    success, frame = camera.read()
    if not success:
        break
    frames.append(frame)
    # calculating time elapsed and showing real time
    if len(prev_time) == t + 1:
        value = datetime.timedelta(seconds=time_elapsed)
        prev_time.clear()
    cv2.putText(
        frame,
        f"{value}",
        (100, 100),
        cv2.FONT_HERSHEY_COMPLEX,
        1,
        (0, 255, 0),
    )
    # end time calculation
    if time_elapsed != 0 and time_elapsed % 15 == 0:
        cv2.putText(
            frame,
            "Processing....",
            (500, 100),
            cv2.FONT_HERSHEY_COMPLEX,
            0.0012 * frame.shape[1],
            (0, 255, 123),
            int(0.002 * frame.shape[1]),
            cv2.LINE_AA,
        )
        process_task = threading.Thread(target=process_frames, args=[frames, frame])
        process_task.start()

    # #  detecting faces from a frame
    # rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # faces = faces_cascade.detectMultiScale(
    #     rgb, scaleFactor=1.3, minNeighbors=2, minSize=(100, 100)
    # )
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # # detecting smiles from detected faces
    # text = ""
    # # detect smile
    # for x, y, w, h in faces:
    #     # drawing a rectangle over the face
    #     cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 255, 0), 2)
    #     face_gray = gray[y : y + h, x : x + w]
    #     # smiles = smile_cascade.detectMultiScale(
    #     #     face_gray, scaleFactor=1.8, minNeighbors=20
    #     # )
    #     landmarks = face_recognition.face_landmarks(frame)
    #     img, smiles = detect_smile(frame, landmarks)
    #     if not any(smiles):
    #         text = "No smile"
    #     else:
    #         text = "Smile"
    #     cv2.putText(
    #         frame,
    #         text,
    #         (x, y - 10),
    #         cv2.FONT_HERSHEY_COMPLEX,
    #         0.0012 * frame.shape[1],
    #         (0, 255, 123),
    #         int(0.002 * frame.shape[1]),
    #         cv2.LINE_AA,
    #     )
    # end detecting smile

    cv2.imshow("Camera", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
camera.release()
cv2.destroyAllWindows()
