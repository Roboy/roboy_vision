import websocket 

def SendRosMsg(Msg):
	ws = websocket.WebSocket();
	ws.connect("ws://bot.roboy.org:9090")
	ws.send("""data:'{"receiver":"/roboy/cognition/vision/faces","msg":"{data:''}","type":"package/Type"}'""")
	print ("Sent")
	print ("Reeiving...")
	ws.close()	