import tkinter as tk
from tkinter import PhotoImage, font as tkFont
import cv2
import os
import mysql.connector
from db import connect_db  # 이 함수는 (host, user, password, database) 연결 반환한다고 가정

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

def take_photo(userid="testuser"):
    cam = cv2.VideoCapture(0)
    cam.set(3, 400)  # width
    cam.set(4, 350)  # height

    photo_path = None

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=8,
            minSize=(70, 70)
        )

        for (x, y, w, h) in faces:
            # 얼굴 + 목 부분까지 포함
            extended_h = int(h * 1.3)  # 얼굴 높이보다 조금 아래까지
            y_end = min(y + extended_h, frame.shape[0])

            cv2.rectangle(frame, (x, y), (x + w, y_end), (0, 255, 0), 3)

            roi = frame[y:y_end, x:x+w]
            roi = cv2.convertScaleAbs(roi, alpha=1.2, beta=30)  # 밝기 보정

            # 저장
            os.makedirs("./photos", exist_ok=True)
            photo_path = f"./photos/{userid}_photo.jpg"
            cv2.imwrite(photo_path, roi)
            print(f"사진 저장 완료: {photo_path}")

            # DB 저장
            save_photo_to_db(userid, photo_path)

        cv2.imshow("촬영 화면", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

def save_photo_to_db(userid, photo_path):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        sql = "UPDATE users SET photo_url = %s WHERE userid = %s"
        cursor.execute(sql, (photo_path, userid))
        conn.commit()

        print("DB 업데이트 완료")
    except Exception as e:
        print("DB 오류:", e)
    finally:
        if conn:
            conn.close()

# 버튼 추가
btn = tk.Button(root, text="사진 찍기", font=custom_font, command=lambda: take_photo("testuser"))
btn.place(x=200, y=400)

root.mainloop()
