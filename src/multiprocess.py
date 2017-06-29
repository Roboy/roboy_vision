import os
 
from multiprocessing import Process,Queue
import FaceDetect
import Multitracking
import cv2
import threading
import sys
 
def TestProcess(number):
    proc = os.getpid()
    while True:
        print('{0} doubled to {1} by process id: {2}'.format(number, result, proc))
 
def detectFaces(FrameQueue,RectQueue):
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
	#Start the face detection
    FaceDetect.StartDetection(FrameQueue,RectQueue)
    sys.exit()
    print ("Terminated")


def tracking(RectQueue,TrackQueue):
    #Start tracking code here
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    Multitracking.StartTracking(RectQueue,TrackQueue)


if __name__ == '__main__':
    procs = []
    FrameQueue = Queue();
    RectQueue = Queue();
    TrackQueue = Queue();

    detectFaceProc = Process(target=detectFaces,args=(FrameQueue,RectQueue,))
    trackProc = Process(target=tracking,args=(RectQueue,TrackQueue,))
    procs.append(detectFaceProc)
    procs.append(trackProc)
    for proc in procs:
        proc.start()

    while True:
        cv2.imshow("frame",TrackQueue.get())
        cv2.moveWindow("frame",20,20)
        cv2.waitKey(1)
    detectFaceProc.join()
    trackProc.join()
    