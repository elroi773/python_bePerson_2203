import cv2
import numpy as np

# DNN 얼굴 검출 모델 로드
prototxt = "deploy.prototxt"
model = "res10_300x300_ssd_iter_140000_fp16.caffemodel"
net = cv2.dnn.readNetFromCaffe(prototxt, model)

# 웹캠 시작
cam = cv2.VideoCapture(0)

# 얼굴 실제 폭 (cm)
KNOWN_WIDTH = 14.0
# 기준 거리 (cm)
KNOWN_DISTANCE = 50.0

# 초점 거리 계산용
focal_length = None
initialized = False

# 경고 이미지 로드
warning_img = cv2.imread("./img/Warning.png")

print("실시간 거리 측정 시작 (종료: q)")

warning_window_open = False  # 창이 열렸는지 추적하는 변수

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

    if show_warning:
        scale = 0.5
        new_w = 400
        new_h = int(warning_img.shape[0] * new_w / warning_img.shape[1])
        resized_warning = cv2.resize(warning_img, (new_w, new_h))
        cv2.imshow("Warning", resized_warning)
        warning_window_open = True
    else:
        if warning_window_open:
            cv2.destroyWindow("Warning")
            warning_window_open = False

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
