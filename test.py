import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# DNN 얼굴 검출 모델 로드
prototxt = "deploy.prototxt"
model = "res10_300x300_ssd_iter_140000_fp16.caffemodel"
net = cv2.dnn.readNetFromCaffe(prototxt, model)

# 웹캠 시작
cam = cv2.VideoCapture(0)

# 얼굴 실제 폭 (cm)
KNOWN_WIDTH = 14.0
KNOWN_DISTANCE = 50.0

# 초점 거리 계산용
focal_length = None
initialized = False

# 경고 이미지 로드
warning_img = cv2.imread("./img/Warning.png")

# ===== Tkinter 창 설정 =====
root = tk.Tk()
root.title("Warning")
root.attributes("-topmost", True)   # 항상 위에
root.withdraw()                     # 처음엔 숨김
root.resizable(False, False)

# 창 크기 설정 (예: 400x200)
win_w, win_h = 400, 200
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
pos_x = (screen_w - win_w) // 2
pos_y = (screen_h - win_h) // 2
root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")

# OpenCV → PIL 변환 (이미지 크기도 창 크기에 맞춤)
img_rgb = cv2.cvtColor(warning_img, cv2.COLOR_BGR2RGB)
img_pil = Image.fromarray(img_rgb).resize((win_w, win_h))
img_tk = ImageTk.PhotoImage(img_pil)

# Label에 이미지 넣기
label = tk.Label(root, image=img_tk)
label.pack()

print("실시간 거리 측정 시작 (종료: q)")

showing = False  # 경고창이 보이는 상태 추적

while True:
    ret, frame = cam.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300),
                                 (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    show_warning = False

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.7:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            face_width = endX - startX

            if not initialized and face_width > 0:
                focal_length = (face_width * KNOWN_DISTANCE) / KNOWN_WIDTH
                initialized = True
                print("초점 거리 계산 완료:", focal_length)

            if focal_length is not None and face_width > 0:
                distance = (KNOWN_WIDTH * focal_length) / face_width
                print(f"현재 거리: {distance:.2f}cm")

                if distance <= 30:
                    show_warning = True

    # 경고창 표시/숨김
    if show_warning and not showing:
        root.deiconify()  # 창 표시
        showing = True
    elif not show_warning and showing:
        root.withdraw()   # 창 숨김
        showing = False

    root.update()  # Tkinter 창 새로고침

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
root.destroy()
