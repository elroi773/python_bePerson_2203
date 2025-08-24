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

while True:
    ret, frame = cam.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300),
                                 (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    show_warning = False  # 경고 표시 여부

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

            # 거리 계산
            if focal_length is not None and face_width > 0:
                distance = (KNOWN_WIDTH * focal_length) / face_width
                cv2.putText(frame, f"{distance:.2f}cm", (startX, startY - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                # 30cm 이하이면 경고
                if distance <= 30:
                    show_warning = True

            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

    # 경고 이미지 표시
    if show_warning:
        # 프레임 크기
        fh, fw = frame.shape[:2]

        # 경고 이미지 크기 조정 (예: 프레임 너비의 50%)
        scale = 0.5
        new_w = int(fw * scale)
        new_h = int(warning_img.shape[0] * new_w / warning_img.shape[1])
        resized_warning = cv2.resize(warning_img, (new_w, new_h))

        # 중앙 위치 계산
        x_offset = (fw - new_w) // 2
        y_offset = (fh - new_h) // 2

        # 프레임에 삽입
        frame[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_warning


    cv2.imshow("Distance Measurement", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
