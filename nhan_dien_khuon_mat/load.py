import face_recognition
import os
import numpy as np
import sqlite3
from datetime import datetime
import cv2

# Kết nối database
conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

# Load khuôn mặt từ database
known_face_encodings = []
known_face_ids = []

for file in os.listdir("processed_faces"):
    image_path = os.path.join("processed_faces", file)
    student_id = file.split(".")[0]  # Lấy mã số sinh viên từ tên file

    img = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(img)

    if encoding:
        known_face_encodings.append(encoding[0])
        known_face_ids.append(student_id)

print("Đã load dữ liệu khuôn mặt!")

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    if not ret:
        break

    # Chuyển sang RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Tìm khuôn mặt trong khung hình
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
        name = "Unknown"

        if True in matches:
            matched_index = matches.index(True)
            student_id = known_face_ids[matched_index]

            # Kiểm tra nếu sinh viên này chưa được điểm danh trong ngày
            today = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("SELECT * FROM attendance WHERE student_id = ? AND DATE(timestamp) = ?", (student_id, today))
            result = cursor.fetchone()

            if not result:
                cursor.execute("INSERT INTO attendance (student_id, timestamp) VALUES (?, ?)", (student_id, datetime.now()))
                conn.commit()
                print(f"Đã điểm danh: {student_id}")

            name = f"ID: {student_id}"

        # Vẽ khung nhận diện
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()