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
        #await websocket.send("{ \"op\": \"advertise_service\",\
        #                  \"type\": \"roboy_communication_cognition/vision_coordinates\",\
        #                  \"service\": \"/roboy/cognition/vision/coordinates\"\
        #                }")

        # advertise the message/topic
        await websocket.send("{ \"op\": \"advertise\",\
                          \"type\": \"roboy_communication_cognition/vision_coordinates\",\
                          \"topic\": \"/roboy/cognition/vision/coordinates\"\
                        }")

        i = 1  # counter for the service request IDs

        while True:
            try:
                message = {}
                answer = {1:list()}

                Rects = RectQueue.get())
                Facepoints = FacepointQueue.get()
                Speaker = SpeakerQueue.get()
                face_ids = Facepoints.keys()


                for id in face_ids:

                    speaking = Speaker[id]
                    x_camera = Rects[id][0] ##TBD - where is x, calculate middlepoint
                    y_camera = Rects[id][0] ##TBD - where is y, calculate middlepoint

                    #transformation

                    #placeholder for input from headposition via ROS - 0 is neutral starting position for every axis
                    #convert angles from quaternion/radians if necesaary
                    pitch = 0.0 #nodding head
                    roll = 0.0 #tilting head
                    yaw = 0.0 #rotation around spine

                    x_resolution = 1280
                    y_resolution = 720

                    max_pitch = 30 #degrees
                    max_roll = 10 #degrees
                    max_yaw = 30 #degrees


                    width = 110 #degrees, given by ZED camera
                    height = 62 #degrees, calculated from ZED camera

                    x_step = x_resolution/width
                    y_step = y_resolution/height

                    x_start = x_camera + (max_yaw - width) * x_step #pixels to the left/right of the neutral position frame
                    y_start = y_camera + (max_pitch - height) * y_step #pixels to the top/bottom of the neutral position frame

                    x = x_start + (yaw * x_step)
                    y = y_start + (pitch * y_step)
                    z = 0.0 #input from ZED camera, based on middle point of rect

                    #rotation
                    #x += cosine(roll) * x_camera - sin(roll) * y_camera
                    #y += sine(roll) * x_camera + cosine(roll)* y_camera

                    coordinates = {x, y, z}


                    face = {'id': id,
                            'speaking': speaking,
                            'coordinates': coordinates}


                #what format should the output be? list of dictionairies?


                	answer["text_output"] = ''.join([i if ord(i) < 128 else '' for i in text])  # strip down unicode

                message["values"] = face
                message["op"] = "service_response"
                message["id"] = "message:/roboy/cognition/vision/coordinates:" + str(i)
                message["service"] = "/roboy/cognition/vision/coordinates"
                i += 1

                await websocket.send(json.dumps(message))

            except Exception as e:
                logging.exception("Oopsie! Got an exception in vision/coordinates")

        logging.basicConfig(level=logging.INFO)
        asyncio.get_event_loop().run_until_complete(service_callback())


