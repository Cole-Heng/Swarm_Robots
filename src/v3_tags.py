import sys
#sys.path.append('/home/pi/Git/apriltag')
import cv2
import sys
import os
#sys.path.append('/home/pi/Git/apriltag')
#sys.path.append('/usr/local/lib')
#print (sys.path)
from apriltag import apriltag

vid = cv2.VideoCapture(0)

#options = apriltag.DetectorOptions(families='tag36h11', border=1, quad_contours=True)
detector = apriltag(family = 'tag36h11', threads = 3, decimate = 2.0)

# Find tags and returns all their resultant data. If display is set to Ture, the live camera
# feed will be shown
def find_tags(frame):
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	results = detector.detect(gray)
	return results

def get_frame():
	ret, frame = vid.read()
	return frame

# Given all results, returns a list of all tag centers
def extract_centers(results):
	centers = []
	for r in results:
		centers.append(r['center'])
	return centers

def extract_ids(results):
	ids = []
	for r in results:
		ids.append(r['id'])
	return ids

def end_prgm():
	vid.release()
	cv2.destroyAllWindows()

def mark_bots(results, nBots, frame):
	ids = extract_ids(results)
	botIndex = []
	i = 0
	for n in ids:
		if (n <= nBots):
			botIndex.append(i)
		i = i + 1
	bots = []
	for n in botIndex:
                bots.append(results[n])
	centers = extract_centers(bots)
	for c in centers:
		cv2.circle(frame, (int(c[0]), int(c[1])), 3, (255, 255, 0), 2)
	return frame

def boundary(results, nBots, frame):
	ids = extract_ids(results)
	cornerIndex = []
	i = 0
	for n in ids:
		if (n > nBots):
			cornerIndex.append(i)
		i = i + 1
	corners = []
	if (len(cornerIndex) > 2):
		print ("ERROR: More than 2 tags have been found representing corners")
		return (frame, False)
	for n in cornerIndex:
		corners.append(results[n])
	centers = extract_centers(corners)
	if (len (centers) == 2):
		(topX, topY) = centers[0]
		(botX, botY) = centers[1]
		topX = int(topX)
		topY = int(topY)
		botX = int(botX)
		botY = int(botY)
		cv2.line(frame, (topX, topY), (botX, topY), (0,255,0), 2)
		cv2.line(frame, (botX, topY), (botX, botY), (0,255,0), 2)
		cv2.line(frame, (botX, botY), (topX, botY), (0,255,0), 2)
		cv2.line(frame, (topX, botY), (topX, topY), (0,255,0), 2)
		return (frame, True)
	return (frame, False)
