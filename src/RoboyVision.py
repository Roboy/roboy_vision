import os
 
from multiprocessing import Process,Queue
import FaceDetect
import Multitracking
import SpeakerDetect
import RecogniseFace
import cv2
import threading
import sys
#import Visualizer
import imutils 

def detectFaces(FrameQueue,RectQueue,FacePointQueue,SpeakerQueue):
    # print('module name:', __name__)
    # print('parent process:', os.getppid())
    # print('process id:', os.getpid())
	#Start the face detection
    FaceDetect.StartDetection(FrameQueue,RectQueue,FacePointQueue,SpeakerQueue)
    sys.exit()
    print ("Terminated")


def tracking(RectQueue,TrackQueue):
    #Start tracking code here
    # print('module name:', __name__)
    # print('parent process:', os.getppid())
    # print('process id:', os.getpid())
    Multitracking.StartTracking(RectQueue,TrackQueue)

def speakerDetect(FacePointQueue,SpeakerQueue,FrameQueue,VisualQueue):
    # print('module name:', __name__)
    # print('parent process:', os.getppid())
    # print('process id:', os.getpid())
    SpeakerDetect.DetectSpeaker(FacePointQueue,SpeakerQueue,FrameQueue,VisualQueue)


def recogniseFace(RectsQueue):
    # print('module name:', __name__)
    # print('parent process:', os.getppid())
    # print('process id:', os.getpid())
    RecogniseFace.recogniseFace(RectsQueue)    

def visualizer(RectQueue,FacePointQueue,SpeakerQueue,FrameQueue,VisualQueue):
    Visualizer.StartVisualization(RectQueue,FacePointQueue,SpeakerQueue,FrameQueue,VisualQueue)


if __name__ == '__main__':
    procs = []
    FrameQueue = Queue()
    RectQueue = Queue()
    TrackQueue = Queue()
    VisualQueue = Queue()
    SpeakerQueue = Queue()
    FacePointQueue = Queue()
    detectFaceProc = \
    Process(target=detectFaces,args=(FrameQueue,RectQueue,FacePointQueue,SpeakerQueue))
    #trackProc = Process(target=tracking,args=(RectQueue,TrackQueue,))
    SpeakerProc = \
    Process(target=speakerDetect,args=(FacePointQueue,SpeakerQueue,FrameQueue,VisualQueue))
    #recogniseFaceProc = Process(target=recogniseFace,args=(RectQueue,))
 #   visualizerProc =Process( \
   #                         target=visualizer,args=(RectQueue,FacePointQueue,SpeakerQueue,FrameQueue,\
   #                                                 VisualQueue))
    procs.append(detectFaceProc)
    #procs.append(trackProc)
    procs.append(SpeakerProc)
    #procs.append(recogniseFaceProc)
  #  procs.append(visualizerProc)
    for proc in procs:
        proc.start()

    while True:
        cv2.imshow("frame",FrameQueue.get())
        cv2.moveWindow("frame",20,20)
        cv2.waitKey(1)
    detectFaceProc.join()
    SpeakerProc.join()
   # visualizerProc.join()
    #recogniseFaceProc.join()
    #trackProc.join()
    
