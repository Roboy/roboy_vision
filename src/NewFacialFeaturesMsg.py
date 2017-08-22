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

        # advertise the message/topic
        await websocket.send("{ \"op\": \"advertise\",\
                          \"type\": \"vision_service/msg/NewFacialFeatures\",\
                          \"topic\": \"/roboy/cognition/vision/NewFacialFeatures\"\
                        }")

        i = 1  # counter for the service request IDs

        while True:

                    float64[128] ff = 0

                    message["values"] = ff
                    message["op"] = "service_response"
                    message["id"] = "message:/roboy/cognition/vision/coordinates:" + str(i)
                    message["service"] = "/roboy/cognition/vision/coordinates"
                    i += 1

                    await websocket.send(json.dumps(message))

                except Exception as e:
                    logging.exception("Oopsie! Got an exception in vision/NewFacialFeatures")

        logging.basicConfig(level=logging.INFO)
        asyncio.get_event_loop().run_until_complete(service_callback())


