import os
 
from multiprocessing import Process,Queue
import FaceDetect
import cv2
 
def doubler(number):
    """
    A doubling function that can be used by a process
    """
    result = number * 2
    proc = os.getpid()
    while True:
        print('{0} doubled to {1} by process id: {2}'.format(number, result, proc))
 
def detectFaces(queue):
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
	#Start the face detection
    FaceDetect.StartDetection(queue)


#def tracking():
    #Start tracking code here

if __name__ == '__main__':
    procs = []
    q = Queue()

    detectFaceProc = Process(target=detectFaces,args=(q,))
    procs.append(detectFaceProc)
    detectFaceProc.start()
    while True:
        cv2.imshow("frame",q.get())
        cv2.waitKey(1)
    detectFaceProc.join()
    # proc = Process(target=doubler,args=(1,))
    # proc.start()
    # proc.join()
 #	trackingProc = Process(target=tracking)
    #Start the face detection:

    # #for index, number in enumerate(numbers):
    #     proc = Process(target=doubler, args=(number,))
    #     procs.append(proc)
    #     proc.start()
