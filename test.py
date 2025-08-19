import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontface.xml')
cam = cv2.VideoCapture(0)
cam.set(3,400)
cam.set(4,350)

while(1):
	ret, frame = cam.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # 사진을 흑백으로 바꿔준다
	faces = face_cascade.detectMultiScale(gray, 1.3, 5) # 얼굴 구하기 - 필요한 상수

	print(len(faces)) #인식된 얼굴 갯수를 출력

	    # 인식된 얼굴에 사각형을 출력한
	for (x,y,w,h) in faces:
	    cv2.rectangle(frame,(x,y),(x+w,y+h),(300,300,300),3) # BGR, 선의 두께
	    for i in range(x, x + w):
	    	for j in range(y, y + h):
	    		for k in range(3):
		    		if(frame[j, i, k] + 50 > 255):
		    			frame[j, i, k] = 255
		    		else:
		    			frame[j, i, k] = frame[j, i, k] + 50

	#화면에 출력한다
	cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'): # q가 입력되면 중지
		break

cam.release()
cv2.destroyAllWindows() # 창 닫기
