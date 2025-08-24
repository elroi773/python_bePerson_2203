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

focal_length = None
initialized = False  # 초점 거리 한 번만 계산

print("실시간 거리 측정 시작 (종료: q)")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300),
                                 (104.0, 177.0, 123.0))

    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.7:  # 신뢰도 70% 이상
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            face_width = endX - startX

            # 기준 거리에서 focal_length 자동 계산 (처음 한 번만)
            if not initialized and face_width > 0:
                focal_length = (face_width * KNOWN_DISTANCE) / KNOWN_WIDTH
                initialized = True
                print("초점 거리 계산 완료:", focal_length)

            # 거리 계산
            if focal_length is not None and face_width > 0:
                distance = (KNOWN_WIDTH * focal_length) / face_width
                cv2.putText(frame, f"{distance:.2f}cm", (startX, startY - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # 얼굴 박스 그리기
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

    cv2.imshow("Distance Measurement", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
