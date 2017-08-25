import websocket 
import json as json
import numpy as np
ws = websocket.WebSocket();
#ws.connect("ws://bot.roboy.org:9090")
ws.connect('ws://localhost:9090')	
def SendRosMsg():
	message = {}
	message["speaking"] = True
	message["ff"] = 0
    # ws.send("""data:'{"receiver":"/roboy/cognition/vision/faces","msg":"{data:''}","type":"package/Type"}'""")
	ws.send(json.dumps(message))
	print("Sent")
	print("Receiving...")
	ws.close()
	print("ads")

#Package the msg in JSON
def PackageMsg():
    print("BS")

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

def SendNewFacialFeatures(i):
    ff = 0
    msg = {}
    msg["speaking"] = False
    msg["ff"] = 0
    message = {}

    message["msg"] = msg
    message["op"] = "publish"
    message["id"] = "message:/roboy/cognition/vision/coordinates:" + str(i)
    message["topic"] = "/roboy/cognition/vision/NewFacialFeatures"
  

    ws.send(json.dumps(message))



