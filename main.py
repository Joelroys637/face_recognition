import face_recognition
import cv2
import numpy as np
import os
import streamlit as st
import sqlite3
from datetime import date
from PIL import Image
#importing my own bg module
import bg_image as bg



# Load DNN model files for face detection
MODEL_PATH = "deploy.prototxt"  # Path to the prototxt file
WEIGHTS_PATH = "res10_300x300_ssd_iter_140000.caffemodel"  # Path to the caffemodel file

def load_dnn_model():
    net = cv2.dnn.readNetFromCaffe(MODEL_PATH, WEIGHTS_PATH)
    return net

def detect_faces_dnn(net, frame):
    """
    Detect faces in the frame using OpenCV DNN.
    Returns bounding boxes of detected faces.
    """
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    face_boxes = []
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # Confidence threshold
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            face_boxes.append((startX, startY, endX, endY))
    return face_boxes

def main():
    a1=st.empty()
    b1=st.empty()
    a=a1.title("Face Recognition Attendance System")
    b=b1.write("Detect faces and mark attendance using your webcam image.")

    # Get lecture name
    try:
        st.markdown(
        """
        <style>
        /* Hide the default checkbox */
        .stCheckbox > div:first-child {
            display: none;
        }

        /* Style the label as a button */
        .stCheckbox > label {
            background-color: #007bff; /* Blue button color */
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            display: inline-block;
            text-align: center;
        }

        /* Change button color on hover */
        .stCheckbox > label:hover {
            background-color: #0056b3; /* Darker blue on hover */
        }

        /* Button active state */
        .stCheckbox > label:active {
            background-color: #003d80; /* Even darker blue when clicked */
        }
        </style>
        """,
        unsafe_allow_html=True
        )
        le=st.empty()
        lecture_name = le.selectbox("SELECT YOU'R HOURE:",("java","bigdata","os","computer Network"),index=None,placeholder="select period",)
        lect=lecture_name+str(date.today())
        check=st.empty()
        if check.checkbox("ok"):
            a1.empty()
            b1.empty()
            le.empty()
            check.empty()
    # Set up database
            safe_table_name = ''.join(e for e in lect if e.isalnum())  # Sanitize table name
            
            conn = sqlite3.connect('attendance_db.db')
            c = conn.cursor()
            c.execute(f"CREATE TABLE IF NOT EXISTS {safe_table_name} (name TEXT, date TEXT)")
            conn.commit()

    # Load known faces from the 'images' folder
            bg.bg_main()
            #st.write("Loading known faces...")
            current_folder = os.getcwd()
            images_folder = os.path.join(current_folder, 'images')
            known_face_encodings = []
            known_face_names = []
    
        if not lecture_name:
            st.write(" ")
            st.stop()
    
        for filename in os.listdir(images_folder):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                image_path = os.path.join(images_folder, filename)
                name = os.path.splitext(filename)[0]  # Name from filename
                image = face_recognition.load_image_file(image_path)
                try:
                    face_encoding = face_recognition.face_encodings(image, model='cnn')[0]  # Use CNN for better accuracy
                    known_face_encodings.append(face_encoding)
                    known_face_names.append(name)
                except IndexError:
                    st.warning(f"No face found in {filename}. Skipping.")
        #st.success("Known faces loaded successfully.")

    # Load DNN model for face detection
        net = load_dnn_model()

    # Capture image with Streamlit
        if st.checkbox("upload image"):

            captured_image = st.file_uploader("Choose a image file", type="jpg")
        else:
            captured_image = st.camera_input("face")

        if captured_image is not None:
        # Convert the image to OpenCV format
            image = Image.open(captured_image)
            frame = np.array(image)

        # Detect faces using DNN
            face_boxes = detect_faces_dnn(net, frame)

        # Perform face recognition
            face_names = []
            for (startX, startY, endX, endY) in face_boxes:
            # Extract the face
                face_frame = frame[startY:endY, startX:endX]
                rgb_face_frame = cv2.cvtColor(face_frame, cv2.COLOR_BGR2RGB)

            # Encode the face
                encodings = face_recognition.face_encodings(rgb_face_frame)
                name = "Unknown"
                if encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, encodings[0])
                    face_distances = face_recognition.face_distance(known_face_encodings, encodings[0])
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

            # Cache attendance and avoid redundant database checks
                face_names.append(name)
                if name != "Unknown":
                    c.execute(f"SELECT * FROM {safe_table_name} WHERE name = ? AND date = ?", (name, str(date.today())))
                    result = c.fetchone()
                    if not result:
                        c.execute(f"INSERT INTO {safe_table_name} (name, date) VALUES (?, ?)", (name, str(date.today())))
                        st.success(f"Attendance marked for {name}")
                        conn.commit()
                    else:
                        st.info(f"Attendance already marked for {name}")

        # Annotate and display the image
            for (startX, startY, endX, endY), name in zip(face_boxes, face_names):
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                cv2.rectangle(frame, (startX, endY - 35), (endX, endY), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (startX + 6, endY - 6), font, 1.0, (255, 255, 255), 1)

        # Display the processed frame
            st.image(frame, channels="BGR")

    # List absent students
        st.write("## Absent Students")
        c.execute(f"SELECT name FROM {safe_table_name} WHERE date = ?", (str(date.today()),))
        present_students = {row[0] for row in c.fetchall()}
        absent_students = [name for name in known_face_names if name not in present_students]

        if absent_students:
            for student in absent_students:
                student_image_path = os.path.join(images_folder, f"{student}.jpg")  # Assuming .jpg format
                if os.path.exists(student_image_path):
                    student_image = Image.open(student_image_path)
                    a=st.button(f"Absent: {student}")
                    if a:
                        st.write(student)
                        c.execute(f"INSERT INTO {safe_table_name} (name, date) VALUES (?, ?)", (student, str(date.today())))
                        st.success(f"ATTENDANCE CHANGED successfully. {student}")
                        conn.commit()
                
                else:
                    st.write(f"Image for {student} not found.")
        else:
            st.write("No absent students today!")

    # Close database connection
        conn.close()
    except:
        st.write(" ")
main()
