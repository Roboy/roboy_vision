import dlib
import cv2
import RosMsgUtil
import sys
import pickle
from __future__ import print_function

import os
import sys
import logging

import asyncio
import websockets
import json as json
import RoboyVision

import pdb

async def service_callback():
    async with websockets.connect('ws://localhost:9090') as websocket:

        # advertise the service
        await websocket.send("{ \"op\": \"advertise_service\",\
                          \"type\": \"vision_service/srv/FindObject\",\
                          \"service\": \"/roboy/cognition/vision/FindObject\"\
                        }")

        i = 1  # counter for the service request IDs


        while True:
            try:
                request = await websocket.recv()

                type = json.loads(request)["type"] #not sure this works, need to retrieve type

                #placeholder for real objects queue
                FoundObjects= ObjectRects.getQueue();

                #structure of FoundObjects: type, x, y, z

                found = False
                coordinates = {}
                for obj in FoundObjects:
                    if(type = obj[0]):
                        found = True
                        coordinates = {obj[1], obj[2], 0}
                        break #does this do enough to break out of the for loop?

                answer = {'found': found,
                          'coordinates': coordinates}

                message["values"] = answer
                message["op"] = "service_response"
                message["id"] = "message:/roboy/cognition/vision/FindObject:" + str(i)
                message["service"] = "/roboy/cognition/vision/FindObject"
                i += 1

                await websocket.send(json.dumps(message))

            except Exception as e:
                logging.exception("Oopsie! Got an exception in vision/coordinates")

        logging.basicConfig(level=logging.INFO)
        asyncio.get_event_loop().run_until_complete(service_callback())


