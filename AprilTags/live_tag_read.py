import cv2
import sys
import os

sys.path.insert(1, '/home/pi/Git/apriltag/python')

import apriltag

#imgStr = "testimg_007_small.jpg"
#print("Loading img: " + imgStr)
#img = cv2.imread(imgStr)
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
vid = cv2.VideoCapture(0)

print("Looking for tags")
options = apriltag.DetectorOptions(families='tag36h11', border=1, quad_contours=True, debug=True)
#print(os.environ)
detector = apriltag.Detector(options)
#results = detector.detect(gray)
#print("[INFO] {} total AprilTags detected".format(len(results)))

while(True):
	ret, frame = vid.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	results = detector.detect(gray)
	print("[INFO] {} total AprilTags detected".format(len(results)))
	input = frame
	#cv2.imshow('input', frame)
	for r in results:
		(ptA, ptB, ptC, ptD) = r.corners
		ptA = (int(ptA[0]), int(ptA[1]))
		ptB = (int(ptB[0]), int(ptB[1]))
		ptC = (int(ptC[0]), int(ptC[1]))
		ptD = (int(ptD[0]), int(ptD[1]))

		cv2.line(frame, ptA, ptB, (0, 255, 0), 2)
		cv2.line(frame, ptB, ptC, (0, 255, 0), 2)
		cv2.line(frame, ptC, ptD, (0, 255, 0), 2)
		cv2.line(frame, ptD, ptA, (0, 255, 0), 2)

		(cX, cY) = (int(r.center[0]), int(r.center[1]))
		cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)

		tagID = str(r.tag_id)
		cv2.putText(frame, tagID, (ptA[0], ptA[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 0), 2)
		#print("[INFO] Tag found with value: " + str(tagID))

	#print(img.shape)
	cv2.imshow("frame", frame)
	if cv2.waitKey(1) & 0xFF == ord('1'):
                break
#cv2.waitKey(5000)
vid.release()
cv2.destroyAllWindows()
