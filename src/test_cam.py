import cv2

vid = cv2.VideoCapture(0)

while (True):
	ret, frame = vid.read()
	cv2.imshow("live", frame)
	if cv2.waitKey(1) & 0xFF == ord('1'):
		break
