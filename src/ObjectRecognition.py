"""@package ObjectRecognition
1. This is a python wrapper for the YOLO implementation in C.
2. uses Ctypes as a way to access C module.
3. libdarknet.so is a pre compiled library which works only on Linux!

"""
from __future__ import print_function

import logging
import asyncio
import websockets
import json as json

from ctypes import *
import math
import random
import cv2
import numpy as np

detect_net=0
detect_meta = 0



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
        print("Object is :",element[1]," coords are: ",element[2])
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
    detect_net = load_net("../darknet/cfg/yolo.cfg", "../darknet/yolo.weights", 0)
    detect_meta = load_meta("../darknet/cfg/coco.data")
	 
def detectObjects(frame):

    if not detect_net:
       Initialize()	
    # print("Its empty")
    # LOAD DETECTION NET
    # ret, frame = CameraFrame.read()
    # RUN OBJECT DETECTION ON FRAME
    frame = frame[0:376, 0:500]
    if detect_net:
        global result
        result = detect(detect_net, detect_meta, frame, thresh=0.5)
        print(str(result[0][0]))
        img = draw_results(result, frame)
        cv2.imshow('frame', img)
        cv2.waitKey(1)


async def describescene_service_callback(frame):
    async with websockets.connect('ws://localhost:9090') as websocket:

        # advertise the service
        await websocket.send("{ \"op\": \"advertise_service\",\
                      \"type\": \"roboy_communication_cognition/DescribeScene\",\
                      \"service\": \"/roboy/cognition/vision/DescribeScene\"\
                    }")

        i = 1  # counter for the service request IDs

        # wait for the service request, generate the answer, and send it back
        while True:
            try:
                # pdb.set_trace()
                request = await websocket.recv()

                srv_response = {}
                answer = {}
                # describe scene function must be called here
                result = detectObjects(frame)
                answer["objects_detected"] = str(result[0][0])
               
                srv_response["values"] = answer
                srv_response["op"] = "service_response"
                srv_response["id"] = "service_request:/roboy/cognition/vision/DescribeScene:" + str(i)
                srv_response["result"] = True
                srv_response["service"] = "/roboy/cognition/vision/DescribeScene"
                i += 1

                await websocket.send(json.dumps(srv_response))

            except Exception as e:
                logging.exception("Oopsie! Got an exception in DescribeSceneSrv")

def startDescribeSceneSrv(frame):
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(describescene_service_callback(frame))