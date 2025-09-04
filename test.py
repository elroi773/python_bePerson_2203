import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import pymysql
from datetime import datetime, timedelta

# ===================== DB 설정 =====================
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "Mysql4344!"
DB_NAME = "bePerson"
USER_ID = 1  # 예시: 사유를 입력하는 사용자 ID

# ===================== 얼굴 검출 모델 =====================
prototxt = "deploy.prototxt"
model = "res10_300x300_ssd_iter_140000_fp16.caffemodel"
net = cv2.dnn.readNetFromCaffe(prototxt, model)

# ===================== 웹캠 =====================
cam = cv2.VideoCapture(0)

# 얼굴 실제 폭 / 거리 계산용
KNOWN_WIDTH = 14.0
KNOWN_DISTANCE = 50.0
focal_length = None
initialized = False

# 경고 이미지
warning_img = cv2.imread("./img/Warning.png")

# ===================== Tkinter 창 =====================
root = tk.Tk()
root.title("Warning")
root.attributes("-topmost", True)
root.withdraw()
root.resizable(False, False)

win_w, win_h = 400, 250
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
pos_x = (screen_w - win_w) // 2
pos_y = (screen_h - win_h) // 2
root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")

# OpenCV → PIL
img_rgb = cv2.cvtColor(warning_img, cv2.COLOR_BGR2RGB)
img_pil = Image.fromarray(img_rgb).resize((win_w, win_h - 50))
img_tk = ImageTk.PhotoImage(img_pil)
label = tk.Label(root, image=img_tk)
label.pack()

# ===================== 버튼 기능 =====================
pause_until = None  # 사유 입력 후 10분 일시정지

def close_warning():
    root.withdraw()

def reason_warning():
    global pause_until
    reason_win = tk.Toplevel(root)
    reason_win.title("사유 입력")
    reason_win.geometry("300x150")
    reason_win.resizable(False, False)

    tk.Label(reason_win, text="사유를 입력하세요:", font=("Arial", 12)).pack(pady=10)
    reason_var = tk.StringVar()
    tk.Entry(reason_win, textvariable=reason_var, width=30, font=("Arial", 12)).pack(pady=5)

    def submit_reason():
        global pause_until
        reason_text = reason_var.get()
        if reason_text.strip():
            try:
                conn = pymysql.connect(
                    host=DB_HOST, user=DB_USER, passwd=DB_PASS,
                    database=DB_NAME, charset="utf8mb4"
                )
                cursor = conn.cursor()
                sql = "INSERT INTO REASONS (user_id, reason_text, created_at) VALUES (%s, %s, %s)"
                cursor.execute(sql, (USER_ID, reason_text, datetime.now()))
                conn.commit()
                conn.close()
                print("사유 DB 저장 완료:", reason_text)

                # 10분 일시정지
                pause_until = datetime.now() + timedelta(minutes=10)
            except Exception as e:
                print("DB 오류:", e)
        reason_win.destroy()

    tk.Button(reason_win, text="제출", command=submit_reason, font=("Arial", 12)).pack(pady=10)

# 버튼 프레임
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)
btn_ok = tk.Button(btn_frame, text="확인", command=close_warning, font=("Arial", 14))
btn_ok.pack(side="left", padx=10)
btn_reason = tk.Button(btn_frame, text="사유", command=reason_warning, font=("Arial", 14))
btn_reason.pack(side="left", padx=10)

# ===================== 얼굴/목 기준 =====================
NECK_THRESHOLD = 100
showing = False
last_show_time = None  # 마지막 알림창 표시 시각

def process_frame():
    global initialized, focal_length, showing, last_show_time

    ret, frame = cam.read()
    if not ret:
        root.after(10, process_frame)
        return

    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300),
                                 (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    show_warning = False
    paused = pause_until is not None and datetime.now() < pause_until

    for i in range(detections.shape[2]):
        if paused:
            break  # 일시정지 중이면 경고 판단 생략

        confidence = detections[0, 0, i, 2]
        if confidence > 0.7:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            face_width = endX - startX
            face_height = endY - startY

            if not initialized and face_width > 0:
                focal_length = (face_width * KNOWN_DISTANCE) / KNOWN_WIDTH
                initialized = True

            if focal_length is not None and face_width > 0:
                distance = (KNOWN_WIDTH * focal_length) / face_width
                print(f"현재 거리: {distance:.2f}cm / 얼굴 높이: {face_height}px")

                if distance <= 30 or face_height <= NECK_THRESHOLD:
                    show_warning = True

    now = datetime.now()
    if not paused:
        if show_warning and not showing:
            root.deiconify()
            showing = True
            last_show_time = now  # 알림창 띄운 시각 기록
        elif not show_warning and showing:
            # 알림창 띄운지 5초 이상 지나야 닫힘
            if last_show_time and (now - last_show_time).total_seconds() >= 5:
                root.withdraw()
                showing = False
    else:
        root.withdraw()
        showing = False

    root.after(30, process_frame)  # 30ms 후 재호출

# ===================== 시작 =====================
root.after(0, process_frame)
root.mainloop()
cam.release()
cv2.destroyAllWindows()
