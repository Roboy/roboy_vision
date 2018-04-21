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
                          \"type\": \"vision_service/srv/DescribeScene\",\
                          \"service\": \"/roboy/cognition/vision/DescribeScene\"\
                        }")

        i = 1  # counter for the service request IDs

        while True:
            try:
                request = await websocket.recv()

                #placeholder for real objects queue
                FoundObjects= ObjectRects.getQueue();

                ObjectsList = {}

                #structure of FoundObjects: type, x, y, z

                for obj in FoundObjects:
                    ObjectsList.append((obj[0], obj[1]))

                sorted(ObjectsList, key=lambda x: x[1], reverse=False) #sort for second value (x coord)
                ObjectsString = [] #array of strings to send

                for i in ObjectsList:
                    ObjectsString.append(i[0])

                message["values"] = ObjectsString
                message["op"] = "service_response"
                message["id"] = "message:/roboy/cognition/vision/DescribeScene:" + str(i)
                message["service"] = "/roboy/cognition/vision/DescribeScene"
                i += 1

                await websocket.send(json.dumps(message))

            except Exception as e:
                logging.exception("Oopsie! Got an exception in vision/coordinates")

        logging.basicConfig(level=logging.INFO)
        asyncio.get_event_loop().run_until_complete(service_callback())


