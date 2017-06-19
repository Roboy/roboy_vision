#from imutils.video import VideoStream
from imutils import face_utils
import imutils
import dlib
import cv2


def StartDetection():
	print("[INFO] loading facial landmark predictor...")
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor("models/dlib/shape_predictor_68_face_landmarks.dat")
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	#outVideo = cv2.VideoWriter('outputMouth.mp4',fourcc, 20.0, (400,225))
	vs = cv2.VideoCapture(0)

	while True:
		# grab the frame from the threaded video stream, resize it to
		# have a maximum width of 400 pixels, and convert it to
		# grayscale
		ok,frame = vs.read()
		if not ok:
			break;
		frame = imutils.resize(frame, width=400)
	#	height,width,channel = frame.shape
		#print (height)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	 
		# detect faces in the grayscale frame
		rects = detector(gray, 0)
			# loop over the face detections
		for rect in rects:
			# determine the facial landmarks for the face region, then
			# convert the facial landmark (x, y)-coordinates to a NumPy
			# array
			shape = predictor(gray, rect)
			shape = face_utils.shape_to_np(shape)
	 
			# loop over the (x, y)-coordinates for the facial landmarks
			# and draw them on the image
			count =0;
			for (x, y) in shape:
				count+=1;
				if(count>36 and count <49):
					cv2.circle(frame, (x, y), 8, (0, 0, 0), -1)
				else:
					cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
		  
		# show the frame
		cv2.imshow("Frame", frame)
	#	outVideo.write(frame)
		key = cv2.waitKey(1) & 0xFF
	 
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break