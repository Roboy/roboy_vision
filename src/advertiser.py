from __future__ import print_function

import logging
import asyncio
import websockets
import json as json
from multiprocessing import Process, Queue
from ForkedPdb import ForkedPdb
# # from config import params_setup
# from lib import data_utils

from imutils import face_utils
import imutils
import dlib
import cv2
#import RosMsgUtil
import pickle
import pdb

from ctypes import *
import math
import random
import sys

import numpy as np


async def FaceCoordinates_callback():
    async with websockets.connect('ws://localhost:9999') as websocket:

        # advertise the topic
        # await websocket.send("{ \"op\": \"advertise\",\
        #                      \"topic\": \"/roboy/cognition/vision/FaceCoordinates\",\
        #                     \"type\": \"vision_service/msg/FaceCoordinates\"\
        #                 }")

        # print('test')
        # while True:
            await websocket.send("{ \"op\": \"advertise\",\
                                \"topic\": \"/roboy/cognition/vision/FaceCoordinates\",\
                                  \"type\": \"roboy_communication_cognition/FaceCoordinates\"\
                                }")

            websocket.send("{ \"op\": \"advertise_service\",\
                          \"type\": \"roboy_communication_cognition/FindObject\",\
                          \"service\": \"/roboy/cognition/vision/FindObject\"\
                        }")

            await websocket.send("{ \"op\": \"advertise\",\
                                                    \"topic\": \"/roboy/cognition/vision/CameraStream\",\
                                                      \"type\": \"roboy_communication_cognition/Floats\"\
                                                    }")
            # websocket.send("{ \"op\": \"subscribe\",\
            #                     \"topic\": \"/roboy/cognition/vision/FaceCoordinates\",\
            #                       \"type\": \"roboy_communication_cognition/FaceCoordinates\"\
            #                     }")

        # i = 1  # counter for the service request IDs
        #
        # # wait for the service request, generate the answer, and send it back
        # while True:
        #     try:
        #         request = await websocket.recv()
        #
        #         srv_response = {}
        #         answer = {}
        #         # retrieve the list of objects from the queue
        #         objects = ObjectsQueue.get()
        #         answer["objects_detected"] = objects[0]
        #         # print(answer["objects_detected"])
        #
        #         srv_response["values"] = answer
        #         srv_response["op"] = "advertise"
        #         srv_response["id"] = "service_request:/roboy/cognition/vision/DescribeScene:" + str(i)
        #         srv_response["result"] = True
        #         srv_response["service"] = "/roboy/cognition/vision/DescribeScene"
        #         i += 1
        #
        #         await websocket.send(json.dumps(srv_response))
        #
        #     except Exception as e:
        #         logging.exception("Oopsie! Got an exception in DescribeSceneSrv")

        # i = 1
        # while True:
        #     try:
        #
        #             values = {}
        #             message = {}
        #
        #             values["id"] = 123
        #             values["speaking"] = True
        #             values["x"] = 100.00
        #             values["y"] = 100.00
        #             values["z"] = 100.00
        #
        #             # message["values"] = values
        #             message["op"] = "publish"
        #             message["topic"] = "/roboy/cognition/vision/FaceCoordinates"
        #             # message["id"] = "message:/roboy/cognition/vision/FaceCoordinates:" + str(i)
        #             # message["msg"] = "/roboy/cognition/vision/FaceCoordinates"
        #             message["msg"] = values
        #             i += 1
        #
        #             await websocket.send(json.dumps(message))
        #             print('running')
        #
        #     except Exception as e:
        #         logging.exception("Oopsie! Got an exception in vision/FaceCoordinates")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(FaceCoordinates_callback())