import face_recognition
import cv2

# 웹캠 열기 (0은 기본 카메라)
video_capture = cv2.VideoCapture(0)

while True:
    # 프레임 읽기
    ret, frame = video_capture.read()
    if not ret:
        break

    # BGR(OpenCV) → RGB(face_recognition) 변환
    rgb_frame = frame[:, :, ::-1]

    # 얼굴 위치 찾기
    face_locations = face_recognition.face_locations(rgb_frame)

    # 얼굴 영역에 사각형 그리기
    for top, right, bottom, left in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 3)

    # 화면에 표시
    cv2.imshow('Face Recognition', frame)

    # q 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
video_capture.release()
cv2.destroyAllWindows()
