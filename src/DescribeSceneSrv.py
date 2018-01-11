from __future__ import print_function

import logging
import asyncio
import websockets
import json as json

# # from config import params_setup
# from lib import data_utils

async def describescene_service_callback():
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
                request = await websocket   .recv()

                srv_response = {}
                answer = {}
                # describe scene function must be called here
                answer["objects_detected"] = ["Look","yourself! Moron"]

                srv_response["values"] = answer
                srv_response["op"] = "service_response"
                srv_response["id"] = "service_request:/roboy/cognition/vision/DescribeScene:" + str(i)
                srv_response["result"] = True
                srv_response["service"] = "/roboy/cognition/vision/DescribeScene"
                i += 1

                await websocket.send(json.dumps(srv_response))

            except Exception as e:
                logging.exception("Oopsie! Got an exception in DescribeSceneSrv")

def startDescribeSceneSrv():
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(describescene_service_callback())