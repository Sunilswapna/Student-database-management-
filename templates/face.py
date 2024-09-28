from flask import Flask, render_template, request
import cv2
import numpy as np
import face_recognition

app = Flask(__name__)

# Function to find encodings of images
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# Function to mark attendance using face recognition
def markAttendance(name, course):
    # Your implementation of marking attendance goes here
    pass

# Route for capturing attendance through webcam
@app.route('/attendance', methods=['POST', 'GET'])
def attendance():
    # Get the coursecode from the form
    cours = request.form.get('coursecode')

    # Path to directory containing images of students
    path = 'C\\Users\\Sunil Rathod\\OneDrive\\Desktop\\DBB\\Student-Management-System-master (2)\\Student-Management-System-master\\student management system\\student management\\Training_images'

    # Load images and corresponding class names (student roll numbers)
    images = []
    classNames = []
    # Assuming collection is defined elsewhere
    for doc in collection.find():
        img_data = doc['image']
        img_np = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        images.append(img)
        classNames.append(str(doc['rollno']))

    # Find face encodings of known images
    encodeListKnown = findEncodings(images)

    # Capture video from webcam
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                markAttendance(name, cours)

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Assuming courses is defined elsewhere
    return render_template('vatt.html', courses=courses)

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
