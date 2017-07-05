import os
 
from multiprocessing import Process,Queue
import FaceDetect
import Multitracking
import SpeakerDetect
import RecogniseFace
import cv2
import threading
import sys
import imutils 
import pickle

def StartVisualization( 
                    RectQueue,\
                    FacePointQueue,\
                    SpeakerQueue,\
                    FrameQueue,VisualQueue):
#    vs = cv2.VideoCapture(0)
#    while True:
#        ok,frame = vs.read()
#        frame = FrameQueue.get()
#        if not frame.any():
#            break
#        frame = imutils.resize(frame, width=800)
#
#        if FacePointQueue.get():
#            Facepoints = pickle.loads(FacePointQueue.get())
#            face_ids = Facepoints.keys()
#            for id in face_ids:
#                shape = Facepoints[id]
#                for (x, y) in shape:    
#                    cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
#  
#        if RectQueue.get():
#            rects = RectQueue.get()
#            counter = 0
#            for rect in rects:
#                counter += 1
#                font = cv2.FONT_HERSHEY_SIMPLEX
#                cv2.putText(frame,str(counter),(10,500), font, 6, (200,255,155), 13,
#                            cv2.LINE_AA)
#                p1 = (int(rect.left()),int(rect.top()))
#                p2 = (int(rect.right()),int(rect.bottom()))
#                cv2.rectangle(frame, p1, p2, (0,0,255,10))
#        VisualQueue.put(frame)
