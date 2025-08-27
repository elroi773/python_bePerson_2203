import cv2
import time
import math

###################################################
sensitivity = 8  # 거북목 감지 민감도
###################################################

# FPS 계산용
pTime = 0
cTime = 0

# 웹캠
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("웹캠을 열 수 없습니다!")
    exit()

# 거북목 카운트
turtle_neck_count = 0

while True:
    ret, img = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다!")
        break

    h, w, _ = img.shape

    # --- 임시 랜드마크 생성 (턱, 어깨 위치) ---
    shoulder_x = w // 2
    shoulder_y = int(h * 0.6)  # 화면 하단쪽 어깨
    face_x = shoulder_x
    face_y = int(h * 0.4)      # 화면 상단쪽 턱

    # 목 길이 계산
    length = math.hypot(face_x - shoulder_x, face_y - shoulder_y)

    # 노트북과의 거리(임의값)
    pose_depth = 400
    turtleneck_detect_threshold = abs(math.log2(pose_depth)) * sensitivity

    # 거북목 판단
    if length < turtleneck_detect_threshold:
        turtle_neck_count += 1

    # 경고 표시
    if length < turtleneck_detect_threshold and turtle_neck_count > 50:
        tutleneck_score = int((turtleneck_detect_threshold - length) / turtleneck_detect_threshold * 100)
        cv2.putText(img, f"WARNING! TurtleNeck {tutleneck_score}%", (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        turtle_neck_count = 0

    # 랜드마크 시각화
    cv2.circle(img, (shoulder_x, shoulder_y), 10, (255,0,0), -1)
    cv2.circle(img, (face_x, face_y), 10, (0,255,0), -1)
    cv2.line(img, (shoulder_x, shoulder_y), (face_x, face_y), (0,255,255), 2)

    # FPS 표시
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (10,70), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 2)

    # 화면 출력
    cv2.imshow("Webcam TurtleNeck Detector", img)

    # ESC 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
