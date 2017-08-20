import websocket 
ws = websocket.WebSocket();
ws.connect("ws://bot.roboy.org:9090")
	
def SendRosMsg(Msg):
    ws.send("""data:'{"receiver":"/roboy/cognition/vision/faces","msg":"{data:''}","type":"package/Type"}'""")
    print("Sent")
	print("Reeiving...")
    ws.close()
    print("ads")

#Package the msg in JSON
def PackageMsg():
    print("BS")