from __future__ import print_function

import logging
import asyncio
import websockets
import json as json
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.2f')

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

import time

import numpy as np

class FrameStreamer():
    async def init(self):
        logging.info('Initializing the streamer')
        async with websockets.connect('ws://localhost:9999') as websocket:
            await websocket.send("{ \"op\": \"advertise\",\
                                    \"topic\": \"/roboy/cognition/vision/CameraStream\",\
                                      \"type\": \"roboy_communication_cognition/Floats\"\
                                    }")

    async def publish(self, frame):
        async with websockets.connect('ws://localhost:9999') as websocket:
            values = {}
            message = {}

            values["data"] = frame.tolist()
            # values["ff"] = [100] * 128
            # print(type(values["ff"]))
            # print(type(values["ff"]))
            # values["ff"] = coordinates

            # message["values"] = values
            message["op"] = "publish"
            message["topic"] = "/roboy/cognition/vision/CameraStream"
            message["msg"] = values

        await websocket.send(json.dumps(message))

    def run(self, frame):
        asyncio.get_event_loop().run_until_complete(self.publish(frame))

    def advertise(self):
        asyncio.get_event_loop().run_until_complete(self.init())

# async def NewFacialFeatures(speaker, coordinates):
#     async with websockets.connect('ws://localhost:9999') as websocket:
#         print('test')
#
#         await websocket.send("{ \"op\": \"advertise\",\
#                             \"topic\": \"/roboy/cognition/vision/NewFacialFeatures\",\
#                               \"type\": \"roboy_communication_cognition/NewFacialFeatures\"\
#                             }")
#         while True:
#             time.sleep(1)
#             try:
#
#                     values = {}
#                     message = {}
#
#                     values["speaking"] = speaker
#                     values["ff"] = [100] * 128
#                     # print(type(values["ff"]))
#                     print(type(values["ff"]))
#                     # values["ff"] = coordinates
#
#                     # message["values"] = values
#                     message["op"] = "publish"
#                     message["topic"] = "/roboy/cognition/vision/NewFacialFeatures"
#                     message["msg"] = values
#
#                     await websocket.send(json.dumps(message))
#
#             except Exception as e:
#                 logging.exception("Oopsie! Got an exception in vision/NewFacialFeatures")
#
# async def FaceCoordinates_callback(id, speaker, coordinates):
#     async with websockets.connect('ws://localhost:9999') as websocket:
#             try:
#
#                     values = {}
#                     message = {}
#
#                     values["id"] = id
#                     values["speaking"] = speaker
#                     values["x"] = coordinates[0]
#                     values["y"] = coordinates[1]
#                     values["z"] = 100.00
#
#                     # message["values"] = values
#                     message["op"] = "publish"
#                     message["topic"] = "/roboy/cognition/vision/FaceCoordinates"
#                     # message["id"] = "message:/roboy/cognition/vision/FaceCoordinates:" + str(i)
#                     message["msg"] = values
#                     # message["msg"] = "Bool [data=true]"
#
#                     await websocket.send(json.dumps(message))
#                     # print('running')
#
#             except Exception as e:
#                 logging.exception("Oopsie! Got an exception in vision/FaceCoordinates")
#
# def publishFaceCoordinates(id, speaker, coordinates):
#     logging.basicConfig(level=logging.INFO)
#     asyncio.get_event_loop().run_until_complete(FaceCoordinates_callback(id, speaker, coordinates))
#
# def publishNewFacialFeatures(speaker, coordinates):
#     logging.basicConfig(level=logging.INFO)
#     asyncio.get_event_loop().run_until_complete(NewFacialFeatures(speaker, coordinates))
#
# # if __name__ == '__main__':
#     # logging.basicConfig(level=logging.INFO)
#     # test = Process(target=asyncio.get_event_loop().run_until_complete(FaceCoordinates_callback()))
#     # Process(target=asyncio.get_event_loop().run_until_complete(FaceCoordinates_callback()))
#     # logging.basicConfig(level=logging.INFO)
#     # asyncio.get_event_loop().run_until_complete(FaceCoordinates_callback())
#     logging.basicConfig(level=logging.INFO)
#     asyncio.get_event_loop().run_until_complete(NewFacialFeatures())
