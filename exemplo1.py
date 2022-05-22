import cv2
import time


xml_haar_cascade = 'haarcascade_frontalface_alt2.xml'

faceClassifier = cv2.CascadeClassifier(xml_haar_cascade)

counter = 1

while not cv2.waitKey(20) & 0xFF == ord("q"):

    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    #while not cv2.waitKey(20) & 0xFF == ord("q"):
    ret, frame_color = capture.read()
    gray = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY)
    faces = faceClassifier.detectMultiScale(gray)
    faces_counter = 0
    for x, y, w, h in faces:
        cv2.rectangle(frame_color, (x, y), (x + w, y + h), (0, 0, 255), 2)
        faces_counter += 1
    cv2.imwrite("./frame%d.jpg" % counter, frame_color)
    counter += 1

    #cv2.imshow('color', frame_color)
    #cv2.imshow('gray', gray)
    print("Number the faces detected %d", faces_counter)

    time.sleep(1)