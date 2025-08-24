import cv2

# alt 모델 로드
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

# 카메라 실행
cam = cv2.VideoCapture(0)
cam.set(3, 400)  # width
cam.set(4, 350)  # height

while True:
    ret, frame = cam.read()
    if not ret:
        break

    # 흑백 변환 + 명암 대비 향상
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # 얼굴 검출 (정확도 향상 파라미터)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.05,    # 1.05면 정밀도 높음 (기본은 1.1)
        minNeighbors=8,      # 높을수록 오탐 줄어듦
        minSize=(70, 70)     # 최소 얼굴 크기
    )

    print(f"인식된 얼굴 수: {len(faces)}")

    # 얼굴 영역에 사각형 및 밝기 조정
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        roi = frame[y:y+h, x:x+w]
        roi = cv2.convertScaleAbs(roi, alpha=1.2, beta=30)  # 밝기/명암 보정
        frame[y:y+h, x:x+w] = roi

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
