"""@package FaceDetect
1. Face is detected using Dlib library
2. 68 landmarks are located on the face and circles are drawn over the landmarks.
3. The position(rect) of the face is sent to the main process throught the RectQueue.
4. Frame queue is as a future reference to send data to the main process
"""

from imutils import face_utils
import imutils
import dlib
import cv2
import RosMsgUtil


def StartDetection(FrameQueue,RectQueue):
	print("[INFO] loading facial landmark predictor...")
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor("models/dlib/shape_predictor_68_face_landmarks.dat")
	#fourcc = cv2.VideoWriter_fourcc(*'XVID')
	#outVideo = cv2.VideoWriter('outputMouth.mp4',fourcc, 20.0, (400,225))
	vs = cv2.VideoCapture(0)

	counter = 0
	while counter<10:
		"""
		grab the frame from the threaded video stream, resize it to
		have a maximum width of 800 pixels, and convert it to
		grayscale"""
		counter+=1
		ok,frame = vs.read()
		if not ok:
			break;
		frame = imutils.resize(frame, width=800)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# detect faces in the grayscale frame
		rects = detector(gray, 0)
		RectQueue.put(rects)
		# loop over the face detections
		for rect in rects:
			shape = predictor(gray, rect)
			shape = face_utils.shape_to_np(shape)
			#print ("Rect from face_detect:",rect,"Detected face width: ",rect.right()-rect.left()," height:",rect.bottom()-rect.top())
			for (x, y) in shape:
					cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
		#FrameQueue.put(frame)
		RectQueue.put(rects)

