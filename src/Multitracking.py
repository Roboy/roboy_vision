"""@package Multitracking
1. Coordinates of the detected object is send though Rects Queue.
2. Currently, MIL tracking algorithm has been employed.
3. A rectangle is drawn over the tracked object andis sent to the main process through TrackQueue
"""

import cv2
import sys
import numpy as np
import dlib
import threading

def StartTracking(RectsQueue,TrackQueue):
	"""
	The co-ords of the object to be tracked is received through the Rects Queue. MIL MultiTracking is used through OpenCV Contrib
	Drawn rectangle is passed over the TrackQueue
    """
	threading.Timer(60, StartTracking).start()
	tracker = cv2.MultiTracker("MIL")
	video = cv2.VideoCapture(0)
	if not video.isOpened():
		print ("Could not open video");
		sys.exit();
	
	x_pixel = 800
	y_pixel = 470
	ok, frame = video.read()
	if not ok:
		sys.exit()
	image = cv2.resize(frame, (int(1*x_pixel),int(1*y_pixel)))
	while True:
		print("Detection again")
		boxes=[]
		for i in range(5):
			rects = RectsQueue.get()
		#fourcc = cv2.VideoWriter_fourcc(*'XVID')
		#outVideo = cv2.VideoWriter('trackingWITHDLIB.mp4',fourcc, 20.0, (800,470))
		for a,rect in enumerate(rects):
			#print ("Rect is:",rect)

			trackpoint = rect.left(),rect.top(),rect.right()-rect.left(),rect.bottom()-rect.top()
			#print (trackpoint)
			tracker.add(image,trackpoint)
		counter = 0

		while counter < 100:
			counter+=1
			ok, frame = video.read()
			img = cv2.resize(frame, (int(1*x_pixel),int(1*y_pixel)))
			found, boxes = tracker.update(img)
			undrawn = img.copy()
			#TrackQueue.put(img)
			print(found)
			if not found:
				TrackQueue.put(undrawn)
			else:
				for newbox in boxes:
					#print (boxes)
					p1 = (int(newbox[0]), int(newbox[1]))
					p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
					#print ("p1: ",newbox[2],"p2:",newbox[3])
					cv2.rectangle(img, p1, p2, (0,0,255,10))
					TrackQueue.put(img)
				#outVideo.write(img)
			
