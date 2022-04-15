import sys
#sys.path.append('/home/pi/Git/apriltag')
import cv2
import sys
import os
sys.path.insert(0, '/home/pi/Git/apriltag/python')
#sys.path.append('/usr/local/lib')
#print (sys.path)
import apriltag

vid = cv2.VideoCapture(0)

options = apriltag.DetectorOptions(families='tag36h11', border=1, quad_contours=True)
detector = apriltag.Detector(options)

# Returns the width and height of the video input frames
def get_frame_info():
	return (int(vid.get(3)), int(vid.get(4)))

# Find tags and returns all their resultant data. If display is set to Ture, the live camera
# feed will be shown
def find_tags(frame):
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	results = detector.detect(gray)
	return results
# Reads a frame from the video feed
def get_frame():
	ret, frame = vid.read()
	return frame

# Given all results, returns a list of all tag centers
def extract_centers(results):
	centers = []
	for r in results:
            if (r != None):
                centers.append(r.center)
	return centers

# Returns a list of all tag IDs found in the frame
def extract_ids(results):
	ids = []
	for r in results:
		ids.append(r.tag_id)
	return ids

def end_prgm():
	vid.release()
	cv2.destroyAllWindows()

# Place a circle at the center of each detected tag know to have a robot ID
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

def get_bot_centers(results, nBots):
	ids = extract_ids(results)
	botIndex = []
	i = 0
	for n in ids:
		if (n < nBots):
			botIndex.append(i)
		i = i + 1
	bots = [None] * nBots
	for n in botIndex:
		bots[results[n].tag_id] = results[n]
	centers = extract_centers(bots)
	return centers
	
def get_two_corners(results, nBots):
	ids = extract_ids(results)
	botIndex = []
	i = 0
	for n in ids:
		if (n < nBots):
			botIndex.append(i)
		i = i + 1
	bots = [None] * nBots
	for n in botIndex:
		bots[results[n].tag_id] = results[n]
	corners = [None] * nBots
	for n in bots:
		if (n != None):
			(ptA, ptB, ptC, ptD) = n.corners
			corners[n.tag_id] = (int(ptA[0]), int(ptA[1]), int(ptD[0]), int(ptD[1]))
	return corners



# Draws a box around the border of the tag and display the ID next to the tag 
def mark_tags(results, frame):
	for r in results:
		(ptA, ptB, ptC, ptD) = r.corners
		ptA = (int(ptA[0]), int(ptA[1]))
		ptB = (int(ptB[0]), int(ptB[1]))
		ptC = (int(ptC[0]), int(ptC[1]))
		ptD = (int(ptD[0]), int(ptD[1]))

		cv2.line(frame, ptA, ptB, (0, 255, 0), 1)
		cv2.line(frame, ptB, ptC, (0, 255, 0), 1)
		cv2.line(frame, ptC, ptD, (0, 255, 0), 1)
		cv2.line(frame, ptD, ptA, (0, 255, 0), 1)

		cv2.putText(frame, str(r.tag_id), (ptB[0], ptB[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
	return frame

# Using two tags as corners of the area, create a box showing the
# arena space
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
