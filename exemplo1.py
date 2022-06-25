import cv2
import time
import requests

xml_haar_cascade = 'haarcascade_frontalface_alt2.xml'

faceClassifier = cv2.CascadeClassifier(xml_haar_cascade)

counter = 1

capture = cv2.VideoCapture(-1)

while not cv2.waitKey(20) & 0xFF == ord("q"):

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    #while not cv2.waitKey(20) & 0xFF == ord("q"):
    ret, frame_color = capture.read()
    # LINUX:
    # gray = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY) 

    # WINDOWS
    gray = cv2.cvtColor(frame_color)
    faces = faceClassifier.detectMultiScale(gray)
    faces_counter = 0
    for x, y, w, h in faces:
        cv2.rectangle(frame_color, (x, y), (x + w, y + h), (0, 0, 255), 2)
        faces_counter += 1
    # cv2.imwrite("./teste2/2faces/teste3/frame%d.jpg" % counter, frame_color)
    counter += 1

    #cv2.imshow('color', frame_color)
    #cv2.imshow('gray', gray)
    print("Number the faces detected %d", faces_counter)

    url= 'http://192.168.18.7:8000/api/central/sendNumberPeople'
    data = {
        "numberPeople": faces_counter,
    }

    response = requests.post(url=url, json=data)

    if response.status_code >= 200 and response.status_code <=299:
        print(response.json())
    else:
        print(response)

    time.sleep(60)