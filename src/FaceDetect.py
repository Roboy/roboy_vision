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
#import RosMsgUtil
import pickle

def StartDetection(FrameQueue,RectQueue,FacepointQueue,SpeakerQueue):
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("../models/dlib/shape_predictor_68_face_landmarks.dat")
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #outVideo = cv2.VideoWriter('outputRoboy.mp4',fourcc, 20.0, (800,533))
    vs = cv2.VideoCapture(0)
    counter = 0
    while True:
        """
        grab the frame from the threaded video stream, resize it to
        have a maximum width of 800 pixels, and convert it to
        grayscale"""
        ok,frame = vs.read()
        if not ok:
            break;
        frame = imutils.resize(frame, width=800)
        #print(frame.shape[0])
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # detect faces in the grayscale frame
        rects = detector(gray, 0)
        # loop over the face detections
        counter=0
        facepoints = dict()
        SpeakerDict = {}
        try:
            SpeakerDict = SpeakerQueue.get_nowait()
        except:
            pass 
        for rect in rects:
            counter +=1
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,str(counter),(rect.left()-10,rect.top()-10),\
                        font, 2, (200,255,155), 13,\
                       cv2.LINE_AA)
            p1 = (int(rect.left()),int(rect.top()))
            p2 = (int(rect.right()),int(rect.bottom()))
            cv2.rectangle(frame, p1, p2, (0,0,255,10))
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            facepoints[counter] =shape
            #print ("Rect from face_detect:",rect,"Detected face width: ",rect.right()-rect.left()," height:",rect.bottom()-rect.top())
            if SpeakerDict:
                #print("Person:",SpeakerDict[counter])
                try:
                    if SpeakerDict[counter]:
                        for (x, y) in shape:    
                            cv2.circle(frame, (x, y), 2, (0, 255,0), -1)
                    else:
                        for (x, y) in shape:    
                            cv2.circle(frame, (x, y), 2, (0, 0,255), -1)
                except:
                    pass
            else:
                for (x, y) in shape:    
                        cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

        FacepointQueue.put(pickle.dumps(facepoints))
        FrameQueue.put(frame)  
     #   outVideo.write(frame)
        RectQueue.put(rects)
