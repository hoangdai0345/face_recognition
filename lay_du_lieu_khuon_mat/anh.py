import cv2
import face_recognition
import sqlite3
import os


conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

output_dir = "processed_faces"
os.makedirs(output_dir, exist_ok=True)

for file in os.listdir("dataset"):
    image_path = os.path.join("dataset", file)
    student_id = file.split("_")[0]

    img = cv2.imread(image_path)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_img)
    if face_locations:
        top, right, bottom, left = face_locations[0]
        face_img = img[top:bottom, left:right]
        face_path = f"{output_dir}/{student_id}.jpg"
        cv2.imwrite(face_path, face_img)

        cursor.execute("INSERT OR IGNORE INTO students (student_id, image) VALUES (?, ?)", (student_id, face_path))

conn.commit()
conn.close()
