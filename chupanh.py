import cv2
import os

camera = cv2.VideoCapture(0)  # Mở camera
student_id = input("Nhập mã số sinh viên: ")

output_dir = "dataset"
os.makedirs(output_dir, exist_ok=True)

count = 0
while count < 3:  # Chụp 10 ảnh
    ret, frame = camera.read()
    if not ret:
        break

    cv2.imshow("Capture", frame)
    cv2.imwrite(f"{output_dir}/{student_id}_{count}.jpg", frame)
    count += 1

    if cv2.waitKey(200) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
