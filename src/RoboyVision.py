import os
 
from multiprocessing import Process,Queue
import FaceDetect
import Multitracking
import SpeakerDetect
import RecogniseFace
import cv2
#import ObjectRecognition
import sys
import Visualizer

def detectFaces(CameraQueue,FrameQueue,RectQueue,FacePointQueue,SpeakerQueue):
    # print('module name:', __name__)
    # print('parent process:', os.getppid())
    # print('process id:', os.getpid())
	#Start the face detection
    FaceDetect.StartDetection(CameraQueue,FrameQueue,RectQueue,FacePointQueue,SpeakerQueue)
    sys.exit()
    print ("Terminated")


def tracking(RectQueue,TrackQueue):
    Multitracking.StartTracking(RectQueue,TrackQueue)

def speakerDetect(FacePointQueue,SpeakerQueue,FrameQueue,VisualQueue):
    SpeakerDetect.DetectSpeaker(FacePointQueue,SpeakerQueue,FrameQueue,VisualQueue)


def recogniseFace(RectsQueue):
    RecogniseFace.recogniseFace(RectsQueue)

def visualizer(CameraQueue,RectQueue,FacePointQueue,SpeakerQueue,FrameQueue,VisualQueue):
    Visualizer.StartVisualization(CameraQueue,RectQueue,FacePointQueue,SpeakerQueue,FrameQueue,VisualQueue)


def ObjectRecognise(ObjectsQueue):
    #ObjectRecognise().detectObjects(ObjectsQueue)
    print("as")





if __name__ == '__main__':
    procs = []
    CameraQueue = Queue()
    FrameQueue = Queue()
    RectQueue = Queue()
    TrackQueue = Queue()
    VisualQueue = Queue()
    SpeakerQueue = Queue()
    FacePointQueue = Queue()
    ObjectsQueue = Queue()
    #visualizerProc = Process( \
    #    target=visualizer, args=(CameraQueue,RectQueue, FacePointQueue, SpeakerQueue, FrameQueue, \
    #                             VisualQueue))

    detectFaceProc = \
    Process(target=detectFaces,args=(CameraQueue,FrameQueue,RectQueue,FacePointQueue,SpeakerQueue))
    #trackProc = Process(target=tracking,args=(RectQueue,TrackQueue,))
    SpeakerProc = \
    Process(target=speakerDetect,args=(FacePointQueue,SpeakerQueue,FrameQueue,VisualQueue))
    recogniseFaceProc = Process(target=recogniseFace,args=(RectQueue,))
    #detectObjectsProc = Process(target=ObjectRecognition,args=(ObjectsQueue,))
    procs.append(detectFaceProc)
    #procs.append(trackProc)
    procs.append(SpeakerProc)
    procs.append(recogniseFaceProc)
    #procs.append(visualizerProc)
    #procs.append(detectObjectsProc)
    for proc in procs:
        proc.start()

    while True:
        cv2.imshow("frame",FrameQueue.get())
        cv2.moveWindow("frame",20,20)
        cv2.waitKey(2)
    detectFaceProc.join()
    SpeakerProc.join()
    #visualizerProc.join()
    #detectObjectsProc.join()
    recogniseFaceProc.join()

    #trackProc.join()
    
