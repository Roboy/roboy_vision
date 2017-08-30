import websocket 
import json as json
import numpy as np
ws = websocket.WebSocket();
ws.connect('ws://localhost:9090')	

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


def AdvertiseContinously()
while True:
	AdvertiseNewFacialFeatures()
	AdvertiseFaceCoordinates()
	AdvertiseFindObject()
	AdvertiseDescribeScene()
	AdvertiseLookAtSpeaker()
	#also put ReceiveServiceRequests here?

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

		await ws.send(json.dumps(message))
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
	  
	    await ws.send(json.dumps(message))
	except Exception as e:
			logging.exception("Something went wrong in SendFaceCoordinates in RosMsgUtil.py")

def FindObject(type):
	try:
		
	except Exception as e:
		logging.exception("Something went wrong in FindObject in RosMsgUtil.py")

def DescribeScene():
	try:

	except Exception as e:
		logging.exception("Something went wrong in DescribeScene in RosMsgUtil.py")

def LookAtSpeaker():
	try:
	except Exception as e:
		logging.exception("Something went wrong in LookAtSpeaker in RosMsgUtil.py")


def ReceiveServiceRequests():
	try:
		request = await ws.recv()
		request_type = json.loads(request)["op"]
		if request_type = "call_service":
			service = json.loads(request)["service"]
			if service = "/roboy/cognition/vision/FindObjects":
				FindObject(json.loads(request)["args"]["type"])
			elif service = "/roboy/cognition/vision/DescribeScene":
				DescribeScene()
			elif service = "/roboy/cognition/vision/LookAtSpeaker":
				LookAtSpeaker()
	except Exception as e:
		logging.exception("Something went wrong in ReceiveServiceRequests in RosMsgUtil.py")			