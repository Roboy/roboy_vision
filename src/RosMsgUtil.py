"""@package RosMsgUtil
1. This module has Util functions to send out ROS messages.
2. The send functions here are called from different modules.
"""
import websocket
import json as json
import numpy as np
ws = websocket.WebSocket();
ws.connect('ws://localhost:9999')   

def AdvertiseNewFacialFeatures():
    ws.send("{ \"op\": \"advertise\",\
                          \"type\": \"roboy_communication_cognition/NewFacialFeatures\",\
                          \"topic\": \"/roboy/cognition/vision/NewFacialFeatures\"\
                        }")    

def AdvertiseFaceCoordinates():
    ws.send("{ \"op\": \"advertise\",\
                          \"type\": \"roboy_communication_cognition/FaceCoordinates\",\
                          \"topic\": \"/roboy/cognition/vision/FaceCoordinates\"\
                        }")   

def AdvertiseFindObject():
    ws.send("{ \"op\": \"advertise_service\",\
                          \"type\": \"roboy_communication_cognition/FindObjects\",\
                          \"service\": \"/roboy/cognition/vision/FindObjects\"\
                        }")  

def AdvertiseDescribeScene():
    ws.send("{ \"op\": \"advertise_service\",\
                          \"type\": \"roboy_communication_cognition/DescribeScene\",\
                          \"service\": \"/roboy/cognition/vision/DescribeScene\"\
                        }")  

def AdvertiseLookAtSpeaker():
    ws.send("{ \"op\": \"advertise_service\",\
                          \"type\": \"roboy_communication_cognition/LookAtSpeaker\",\
                          \"service\": \"/roboy/cognition/vision/LookAtSpeaker\"\
                        }")  


def AdvertiseContinously():
    AdvertiseNewFacialFeatures()
    AdvertiseFaceCoordinates()
    AdvertiseFindObject()
    AdvertiseDescribeScene()
    AdvertiseLookAtSpeaker()
    ReceiveServiceRequests()

    
def SendNewFacialFeatures(ff, speaking, i):
    try:
        msg = {}
        msg["ff"] = ff
        msg["speaking"] = speaking

        message = {}
        message["msg"] = msg
        message["op"] = "publish"
        message["id"] = "message:/roboy/cognition/vision/NewFacialFeatures:" + str(i)
        message["topic"] = "/roboy/cognition/vision/NewFacialFeatures"

        ws.send(json.dumps(message))
    except Exception as e:
            logging.exception("Something went wrong in SendNewFacialFeatures in RosMsgUtil.py")

def SendFaceCoordinates(id, speaking, position, i):
    try:
        msg = {}
        msg["id"] = id
        msg["speaking"] = speaking
        msg["x"] = position[0]
        msg["y"] = position[1]
        msg["z"] = position[2]
        
        message = {}
        message["msg"] = msg
        message["op"] = "publish"
        message["id"] = "message:/roboy/cognition/vision/FaceCoordinates:" + str(i)
        message["topic"] = "/roboy/cognition/vision/FaceCoordinates"

        ws.send(json.dumps(message))
    except Exception as e:
            logging.exception("Something went wrong in SendFaceCoordinates in RosMsgUtil.py")

def FindObject(type, i):
    try:
        msg = {}
        #msg = #function to find object and return "found": bool, 3d position in float32

        msg["objects_detected"] = objects_detected

        message = {}
        message["values"] = msg
        message["op"] = "service_response"
        message["id"] = "service_response:/roboy/cognition/vision/FindObject:" + str(i)
        message["service"] = "/roboy/cognition/vision/FindObject"
        
        ws.send(json.dumps(message))
    except Exception as e:
        logging.exception("Something went wrong in FindObject in RosMsgUtil.py")

def DescribeScene(i):
    try:
        msg = {}
        #objects_detected = #get Object Queue here

        msg["objects_detected"] = objects_detected

        message = {}
        message["values"] = msg
        message["op"] = "service_response"
        message["id"] = "service_response:/roboy/cognition/vision/DescribeScene:" + str(i)
        message["service"] = "/roboy/cognition/vision/DescribeScene"
        
        ws.send(json.dumps(message))

    except Exception as e:
        logging.exception("Something went wrong in DescribeScene in RosMsgUtil.py")

def LookAtSpeaker(i):
    try:
       a = i
        ##
    except Exception as e:
        logging.exception("Something went wrong in LookAtSpeaker in RosMsgUtil.py")


def ReceiveServiceRequests():
    try:
        request = ws.recv()
        request_type = json.loads(request)["op"]
        if request_type == "call_service":
            service = json.loads(request)["service"]
            if service == "/roboy/cognition/vision/FindObjects":
                FindObject(json.loads(request)["args"]["type"], json.loads(request)["args"]["id"])
            elif service == "/roboy/cognition/vision/DescribeScene":
                DescribeScene(json.loads(request)["args"]["id"])
            elif service == "/roboy/cognition/vision/LookAtSpeaker":
                LookAtSpeaker(json.loads(request)["args"]["id"])
    except Exception as e:
        logging.exception("Something went wrong in ReceiveServiceRequests in RosMsgUtil.py")            
