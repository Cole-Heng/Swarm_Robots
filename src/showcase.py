import cv2
import tags
import sys
import os
sys.path.insert(0, '/home/pi/Git/apriltag/python')
import apriltag

nBots = 50
total_frames = 0
good_frames = 0
(frame_width, frame_height) = tags.get_frame_info()
out = cv2.VideoWriter('tag_demo2.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))
while (True):
	frame = tags.get_frame()
	results = tags.find_tags(frame)
	#ids = tags.extract_ids(results)
	cv2.imshow("live", frame)
	#frame = tags.mark_tags(results, frame)
	#print ("IDs found: ")
	#for n in ids:
	#	print (str(n))
	#print ("\n# corners: ")
	#frame = tags.mark_bots(results, nBots, frame)
	(frame, isGood) = tags.boundary(results, nBots, frame)
	#if (len(ids) != 0):
	#	good_frames = good_frames + 1
	#total_frames = total_frames + 1
	#print ("percent good: " + str(float(good_frames / total_frames)*100))
	#cv2.imshow("post", frame)
	cv2.imshow("result", frame)
	out.write(frame)
	if cv2.waitKey(1) & 0xFF == ord('1'):
		break

