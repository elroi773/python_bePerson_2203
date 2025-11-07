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
detected_neck_length = 0  # 목 길이 저장

# 프레임을 담을 Frame (중앙 정렬)
frame_container = tk.Frame(root, bg="white")
frame_container.place(relx=0.5, rely=0.4, anchor="center")

# Tkinter에 영상 표시용 라벨
video_label = tk.Label(frame_container, bg="black")
video_label.pack()

# 웹캠 객체
cam = cv2.VideoCapture(0)
cam.set(3, 400)
cam.set(4, 350)

def update_frame():
    global captured_frame, detected_faces, detected_neck_length

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
        # 얼굴 박스
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # 목 길이 추정
        neck_length = int(h * 0.35)
        detected_neck_length = neck_length

        # 목 영역 박스
        y_neck_start = y + h
        y_neck_end = min(y + h + neck_length, frame.shape[0])
        cv2.rectangle(frame, (x, y_neck_start), (x + w, y_neck_end), (255, 0, 0), 2)

        # 목 길이 텍스트
        cv2.putText(frame, f"Neck: {neck_length}px", (x, y_neck_end + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    captured_frame = frame.copy()

    # OpenCV -> PIL 변환
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb)

    # 👉 크기를 80%로 축소
    new_w = int(img.width * 0.8)
    new_h = int(img.height * 0.8)
    img = img.resize((new_w, new_h))

    imgtk = ImageTk.PhotoImage(image=img)

    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    root.after(10, update_frame)

def take_photo(userid="testuser"):
    global captured_frame, detected_faces, detected_neck_length

    if captured_frame is None or len(detected_faces) == 0:
        print("⚠ 얼굴이 인식되지 않았습니다.")
        return

    (x, y, w, h) = detected_faces[0]
    neck_length = detected_neck_length

    extended_h = h + neck_length
    y_end = min(y + extended_h, captured_frame.shape[0])

    roi = captured_frame[y:y_end, x:x+w]
    roi = cv2.convertScaleAbs(roi, alpha=1.2, beta=30)

    os.makedirs("./photos", exist_ok=True)
    photo_path = f"./photos/{userid}_photo.jpg"
    cv2.imwrite(photo_path, cv2.cvtColor(roi, cv2.COLOR_RGB2BGR))
    print(f"📸 사진 저장 완료: {photo_path} (목 길이: {neck_length}px)")

    save_photo_to_db(userid, photo_path, neck_length)

def save_photo_to_db(userid, photo_path, neck_length):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        sql = "UPDATE users SET photo_url = %s, neck_length = %s WHERE userid = %s"
        cursor.execute(sql, (photo_path, neck_length, userid))
        conn.commit()

        print(f"✅ DB 업데이트 완료 (userid={userid}, 목 길이={neck_length}px)")
    except Exception as e:
        print("DB 오류:", e)
    finally:
        if conn:
            conn.close()

# 버튼 추가 (화면 아래 중앙)
btn = tk.Button(root, text="사진 촬영", font=custom_font, command=lambda: take_photo("testuser"))
btn.place(relx=0.5, rely=0.9, anchor="center")

# 프레임 업데이트 시작
update_frame()

root.mainloop()

# 종료 시 카메라 해제
cam.release()