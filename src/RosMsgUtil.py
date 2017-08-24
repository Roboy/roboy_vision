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


def Advertise():
    ws.send("{ \"op\": \"advertise\",\
                          \"type\": \"roboy_communication_cognition/NewFacialFeatures\",\
                          \"topic\": \"/roboy/cognition/vision/NewFacialFeatures\"\
                        }")    

def SendFaceMsg():
    ff = 0
    msg = {}
    msg["speaking"] = False
    msg["ff"] = 0
    message = {}

    message["msg"] = msg
    message["op"] = "publish"
    # message["id"] = "message:/roboy/cognition/vision/coordinates:" + str(msg["id"])
    message["topic"] = "/roboy/cognition/vision/NewFacialFeatures"
  

    ws.send(json.dumps(message))



Advertise()
while True:
	SendFaceMsg()