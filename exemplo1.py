import cv2
import time
import requests

XML_HAAR_CASCADE = 'haarcascade_frontalface_alt2.xml'

def most_frequent(array):
    counter = 0
    num = array[0]
     
    for i in array:
        curr_frequency = array.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
 
    return num

def send_request_with_number_of_faces(number_of_faces):
    url= 'http://192.168.18.7:8000/api/central/sendNumberPeople'
    data = {
        "numberPeople": number_of_faces,
    }
    response = requests.post(url=url, json=data)
    print("Sending the request to the server...")
    if response.status_code >= 200 and response.status_code <=299:
        print(response.json())
    else:
        print(response)

def scan_most_occurrence_number_of_faces_by_time_window(time_interval, time_end):
    
    face_classifier = cv2.CascadeClassifier(XML_HAAR_CASCADE)
    counter = 1
    limit = int(time_end/time_interval)
    faces_occurrences = []
    capture = cv2.VideoCapture(-1)
    
    while not cv2.waitKey(20) & 0xFF == ord("q") and counter <= limit:
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        ret, frame_color = capture.read()

        gray = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY) # LINUX
        # gray = cv2.cvtColor(frame_color)  # WINDOWS

        faces = face_classifier.detectMultiScale(gray)
        faces_counter = len(faces)
        faces_occurrences.append(faces_counter)

        print(str(counter) + " | Number the faces detected: " + str(faces_counter))
        counter += 1
        time.sleep(time_interval)

    return most_frequent(faces_occurrences)

def main():
    while True:
        number_of_faces = scan_most_occurrence_number_of_faces_by_time_window(1, 60)
        send_request_with_number_of_faces(number_of_faces)

if __name__ == "__main__":
    main()