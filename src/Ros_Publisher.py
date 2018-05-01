from __future__ import print_function

import logging
import asyncio
import websockets
import json as json
# from json_tricks import dump, dumps, load, loads, strip_comments
import pandas as pd
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

# import numpy as np



async def NewFacialFeatures(speaker, coordinates):
    async with websockets.connect('ws://localhost:9090') as websocket:
        print('test')

        await websocket.send("{ \"op\": \"advertise\",\
                            \"topic\": \"/roboy/cognition/vision/NewFacialFeatures\",\
                              \"type\": \"roboy_communication_cognition/NewFacialFeatures\"\
                            }")
        while True:
            time.sleep(1)
            try:

                    values = {}
                    message = {}

                    values["speaking"] = speaker
                    values["ff"] = [100] * 128
                    # print(type(values["ff"]))
                    print(type(values["ff"]))
                    # values["ff"] = coordinates

                    # message["values"] = values
                    message["op"] = "publish"
                    message["topic"] = "/roboy/cognition/vision/NewFacialFeatures"
                    message["msg"] = values

                    await websocket.send(json.dumps(message))

            except Exception as e:
                logging.exception("Oopsie! Got an exception in vision/NewFacialFeatures")

async def CameraFrame(frame):
    #     async with websockets.connect('ws://localhost:9090') as websocket:
    #
    #     # # # await websocket.send("{ \"op\": \"advertise\",\
    #     # #                                     \"topic\": \"/roboy/cognition/vision/CameraStream\",\
    #     #                                       \"type\": \"roboy_communication_cognition/Floats\"\
    #     #                                     }")
    #     #
    #     # while True:
    #     #     time.sleep(1)
    #         try:
    #             values = {}
    #             message = {}
    #
    #             # print(frame)
    #             values["data"] = frame.flatten().tolist()
    #             type(values["data"])
    #
    #             # message["values"] = values
    #     message["msg"] = valulues"] = valueses
    #
    #     await websocket.send(json.dumps(message))
    #
    # except Exception as e:
    #     logging.exception("Oopsie! Got an exception in vision/CameraStream")
        async with websockets.connect('ws://localhost:9090') as websocket:
            try:

                values = {}
                message = {}

                values["data"] = frame.flatten().tolist()
                values["z"] = 100.00

                # message["values"] = values
                message["op"] = "publish"
                message["topic"] = "/roboy/cognition/vision/FaceCoordinates"
                # message["id"] = "message:/roboy/cognition/vision/FaceCoordinates:" + str(i)
                message["msg"] = values
                # message["msg"] = "Bool [data=true]"

                await websocket.send(json.dumps(message))
                 # print('running')

            except Exception as e:
                logging.exception("Oopsie! Got an exception in vision/FaceCoordinates")

async def FaceCoordinates_callback(id, speaker, coordinates):
    async with websockets.connect('ws://localhost:9090') as websocket:
            try:

                    values = {}
                    message = {}

                    values["id"] = id
                    values["speaking"] = speaker
                    values["x"] = coordinates[0]
                    values["y"] = coordinates[1]
                    values["z"] = 100.00

                    # message["values"] = values
                    message["op"] = "publish"
                    message["topic"] = "/roboy/cognition/vision/FaceCoordinates"
                    # message["id"] = "message:/roboy/cognition/vision/FaceCoordinates:" + str(i)
                    message["msg"] = values
                    # message["msg"] = "Bool [data=true]"

                    await websocket.send(json.dumps(message))
                    # print('running')

            except Exception as e:
                logging.exception("Oopsie! Got an exception in vision/FaceCoordinates")

def publishFaceCoordinates(id, speaker, coordinates):
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(FaceCoordinates_callback(id, speaker, coordinates))

def publishNewFacialFeatures(speaker, coordinates):
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(NewFacialFeatures(speaker, coordinates))

def publishCameraFrame(frame):
    global websocket
    websocket = websockets.connect('ws://localhost:9090')
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(CameraFrame(frame))

# if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    # test = Process(target=asyncio.get_event_loop().run_until_complete(FaceCoordinates_callback()))
    # Process(target=asyncio.get_event_loop().run_until_complete(FaceCoordinates_callback()))
    # logging.basicConfig(level=logging.INFO)
    # asyncio.get_event_loop().run_until_complete(FaceCoordinates_callback())
    # logging.basicConfig(level=logging.INFO)
    # asyncio.get_event_loop().run_until_complete(NewFacialFeatures())
