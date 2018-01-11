from __future__ import print_function

import logging
import asyncio
import websockets
import json as json

# # from config import params_setup
# from lib import data_utils

async def getobject_service_callback():
    async with websockets.connect('ws://localhost:9090') as websocket:

        # advertise the service
        await websocket.send("{ \"op\": \"advertise_service\",\
                      \"type\": \"roboy_communication_cognition/GetObject\",\
                      \"service\": \"/roboy/cognition/vision/GetObject\"\
                    }")

        i = 1  # counter for the service request IDs

        # wait for the service request, generate the answer, and send it back
        while True:
            try:
                # pdb.set_trace()
                request = await websocket.recv()
                properties = json.loads(request)["args"]["properties"]
                values = json.loads(request)["args"]["values"]

                srv_response = {}
                answer = {}
                # get object function must be added here
                answer["result"] = True
                answer["instance"] = 'lol'

                srv_response["values"] = answer
                srv_response["op"] = "service_response"
                srv_response["id"] = "service_request:/roboy/cognition/vision/GetObject:" + str(i)
                srv_response["result"] = True
                srv_response["service"] = "/roboy/cognition/vision/GetObject"
                i += 1

                await websocket.send(json.dumps(srv_response))

                # print ("Got here somehow" + str(srv_response))

            except Exception as e:
                logging.exception("Oopsie! Got an exception in GetObjectSrv")

logging.basicConfig(level=logging.INFO)
asyncio.get_event_loop().run_until_complete(getobject_service_callback())