import tkinter as tk
from tkinter import PhotoImage, font as tkFont
import cv2
import os
from PIL import Image, ImageTk
from db import connect_db

root = tk.Tk()
root.title("정자세 사진 찍기")

# 배경 이미지
bg_img = PhotoImage(file="./img/takephoto.png")
canvas = tk.Canvas(root, width=bg_img.width(), height=bg_img.height(), highlightthickness=0)
canvas.pack()
canvas.create_image(0, 0, anchor="nw", image=bg_img)

# 폰트
custom_font = tkFont.Font(family="./DungGeunMo.ttf", size=14)

# HaarCascade 모델
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

# 전역 변수
captured_frame = None
detected_faces = []

# Tkinter에 영상 표시용 라벨
video_label = tk.Label(root)
video_label.place(x=100, y=50)

# 웹캠 객체
cam = cv2.VideoCapture(0)
cam.set(3, 400)
cam.set(4, 350)

def update_frame():
    global captured_frame, detected_faces

    ret, frame = cam.read()
    if not ret:
        root.after(10, update_frame)
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=8,
        minSize=(70, 70)
    )
    detected_faces = faces

    for (x, y, w, h) in faces:
        extended_h = int(h * 1.3)
        y_end = min(y + extended_h, frame.shape[0])
        cv2.rectangle(frame, (x, y), (x + w, y_end), (0, 255, 0), 3)

    captured_frame = frame.copy()

    # OpenCV -> PIL -> Tkinter 변환
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb)
    imgtk = ImageTk.PhotoImage(image=img)

    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    root.after(10, update_frame)

def take_photo(userid="testuser"):
    global captured_frame, detected_faces

    if captured_frame is None or len(detected_faces) == 0:
        print("⚠ 얼굴이 인식되지 않았습니다.")
        return

    (x, y, w, h) = detected_faces[0]
    extended_h = int(h * 1.3)
    y_end = min(y + extended_h, captured_frame.shape[0])

    roi = captured_frame[y:y_end, x:x+w]
    roi = cv2.convertScaleAbs(roi, alpha=1.2, beta=30)

    os.makedirs("./photos", exist_ok=True)
    photo_path = f"./photos/{userid}_photo.jpg"
    cv2.imwrite(photo_path, cv2.cvtColor(roi, cv2.COLOR_RGB2BGR))
    print(f"📸 사진 저장 완료: {photo_path}")

    save_photo_to_db(userid, photo_path)

def save_photo_to_db(userid, photo_path):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        sql = "UPDATE users SET photo_url = %s WHERE userid = %s"
        cursor.execute(sql, (photo_path, userid))
        conn.commit()

        print("✅ DB 업데이트 완료")
    except Exception as e:
        print("DB 오류:", e)
    finally:
        if conn:
            conn.close()

# 버튼 추가
btn = tk.Button(root, text="사진 촬영", font=custom_font, command=lambda: take_photo("testuser"))
btn.place(x=200, y=400)

# 주기적으로 프레임 업데이트
update_frame()

root.mainloop()

# 종료 시 카메라 해제
cam.release()
