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


from ctypes import *
import math
import random

import numpy as np

def StartDetection(CameraQueue,FrameQueue,RectQueue,FacepointQueue,SpeakerQueue):
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("../models/dlib/shape_predictor_68_face_landmarks.dat")
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #outVideo = cv2.VideoWriter('outputRoboy.mp4',fourcc, 20.0, (800,533))
    vs = cv2.VideoCapture(0)
    detect_net = load_net("../darknet/cfg/yolo.cfg", "../darknet/yolo.weights", 0)
    detect_meta = load_meta("../darknet/cfg/coco.data")
    counter = 0
    while True:
        """
        grab the frame from the threaded video stream, resize it to
        have a maximum width of 800 pixels, and convert it to
        grayscale"""
        ok,frame = vs.read()
        if not ok:
            break;
        #frame = imutils.resize(frame, width=800)\
	frame = frame[0:376, 0:500]

       	detectObjects(frame,detect_net,detect_meta) 
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



def sample(probs):
    s = sum(probs)
    probs = [a / s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs) - 1


def c_array(ctype, values):
    return (ctype * len(values))(*values)


class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]


class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]

    # lib = CDLL("/home/pjreddie/documents/darknet/libdarknet.so", RTLD_GLOBAL)


lib = CDLL("../darknet/libdarknet.so", RTLD_GLOBAL)
lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

predict = lib.network_predict_p
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

make_boxes = lib.make_boxes
make_boxes.argtypes = [c_void_p]
make_boxes.restype = POINTER(BOX)

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

num_boxes = lib.num_boxes
num_boxes.argtypes = [c_void_p]
num_boxes.restype = c_int

make_probs = lib.make_probs
make_probs.argtypes = [c_void_p]
make_probs.restype = POINTER(POINTER(c_float))

detect = lib.network_predict_p
detect.argtypes = [c_void_p, IMAGE, c_float, c_float, c_float, POINTER(BOX), POINTER(POINTER(c_float))]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network_p
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

free_image = lib.free_image
free_image.argtypes = [IMAGE]

letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)

network_detect = lib.network_detect
network_detect.argtypes = [c_void_p, IMAGE, c_float, c_float, c_float, POINTER(BOX), POINTER(POINTER(c_float))]


def detect(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
    # check if image is an OpenCV frame

    if isinstance(image, np.ndarray):
        # GET C,H,W, and DATA values
        img = image.transpose(2, 0, 1)
        c, h, w = img.shape[0], img.shape[1], img.shape[2]
        nump_data = img.ravel() / 255.0
        nump_data = np.ascontiguousarray(nump_data, dtype=np.float32)

        # make c_type pointer to numpy array
        ptr_data = nump_data.ctypes.data_as(POINTER(c_float))

        # make IMAGE data type
        im = IMAGE(w=w, h=h, c=c, data=ptr_data)

    else:
        im = load_image(image, 0, 0)

    boxes = make_boxes(net)
    probs = make_probs(net)
    num = num_boxes(net)
    network_detect(net, im, thresh, hier_thresh, nms, boxes, probs)
    res = []
    for j in range(num):
        for i in range(meta.classes):
            if probs[j][i] > 0:
                res.append((meta.names[i], probs[j][i], (boxes[j].x, boxes[j].y, boxes[j].w, boxes[j].h)))
    res = sorted(res, key=lambda x: -x[1])
    # free_image(im)
    # free_ptrs(cast(probs, POINTER(c_void_p)), num)

    return res


def draw_results(res, img):

    for element in res:
        box = element[2]
        xmin = int(box[0] - box[2] / 2. + 1)
        xmax = int(box[0] + box[2] / 2. + 1)
        ymin = int(box[1] - box[3] / 2. + 1)
        ymax = int(box[1] + box[3] / 2. + 1)
        rand_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color=rand_color, thickness=3, )
        cv2.putText(img, str(element[0]) + " " + '%.2f' % element[1],
                    (xmin, ymin),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, rand_color, thickness=3)
    return img
DONE = 0
def Initialize():
    DONE = 0
    
	 
def detectObjects(frame,detect_net,detect_meta):


    #ret, frame = CameraFrame.read()
    # RUN OBJECT DETECTION ON FRAME
    frame = frame[0:376, 0:500]
    if detect_net:
        result = detect(detect_net, detect_meta, frame, thresh=0.5)
        img = draw_results(result, frame)
       
