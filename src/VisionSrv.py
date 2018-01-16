from __future__ import print_function

import logging
import asyncio
import websockets
import json as json

from ForkedPdb import ForkedPdb
# # from config import params_setup
# from lib import data_utils

async def describescene_service_callback(ObjectsQueue):
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
                request = await websocket.recv()

                srv_response = {}
                answer = {}
                # retrieve the list of objects from the queue
                objects = ObjectsQueue.get()
                answer["objects_detected"] = objects
                print(answer["objects_detected"])

                srv_response["values"] = answer
                srv_response["op"] = "service_response"
                srv_response["id"] = "service_request:/roboy/cognition/vision/DescribeScene:" + str(i)
                srv_response["result"] = True
                srv_response["service"] = "/roboy/cognition/vision/DescribeScene"
                i += 1

                await websocket.send(json.dumps(srv_response))

            except Exception as e:
                logging.exception("Oopsie! Got an exception in DescribeSceneSrv")

async def findobject_service_callback(ObjectsQueue, RectQueue):
    async with websockets.connect('ws://localhost:9090') as websocket:

        # advertise the service
        await websocket.send("{ \"op\": \"advertise_service\",\
                      \"type\": \"roboy_communication_cognition/FindObject\",\
                      \"service\": \"/roboy/cognition/vision/FindObject\"\
                    }")

        i = 1  # counter for the service request IDs

        # wait for the service request, generate the answer, and send it back
        while True:
            try:

                request = await websocket.recv()
                type = json.loads(request)["args"]["type"]
                srv_response = {}
                answer = {}
                # find object function must be implemented here
                objects = ObjectsQueue.get()
                rects = RectQueue.get()
                print(rects)
                print('Somehow got here')

                if type in objects:
                    answer["found"] = True
                    answer["x"] = 1000
                    answer["y"] = 1000
                    answer["z"] = 1000
                else:
                    answer["found"] = False
                    answer["x"] = 0
                    answer["y"] = 0
                    answer["z"] = 0

                srv_response["values"] = answer
                srv_response["op"] = "service_response"
                srv_response["id"] = "service_request:/roboy/cognition/vision/FindObject:" + str(i)
                srv_response["result"] = True
                srv_response["service"] = "/roboy/cognition/vision/FindObject"
                i += 1

                await websocket.send(json.dumps(srv_response))

                # print ("Got here somehow" + str(srv_response))

            except Exception as e:
                logging.exception("Oopsie! Got an exception in FindObjectSrv")

# async def getobject_service_callback(ObjectsQueue):
#     async with websockets.connect('ws://localhost:9090') as websocket:
#
#         # advertise the service
#         await websocket.send("{ \"op\": \"advertise_service\",\
#                       \"type\": \"roboy_communication_cognition/GetObject\",\
#                       \"service\": \"/roboy/cognition/vision/GetObject\"\
#                     }")
#
#         i = 1  # counter for the service request IDs
#
#         # wait for the service request, generate the answer, and send it back
#         while True:
#             try:
#                 # pdb.set_trace()
#                 request = await websocket.recv()
#                 properties = json.loads(request)["args"]["properties"]
#                 values = json.loads(request)["args"]["values"]
#
#                 srv_response = {}
#                 answer = {}
#                 # get object function must be added here
#
#                 objects = ObjectsQueue.get()
#                 # answer["objects_detected"] = objects
#
#                 if str(objects) == (properties):
#                     answer["result"] = True
#                     answer["instance"] = str(objects)
#                 else:
#                     answer["result"] = False
#                     answer["instance"] = 'Object not in frame'
#                 # answer["result"] = True
#                 # answer["instance"] = 'lol'
#
#                 srv_response["values"] = answer
#                 srv_response["op"] = "service_response"
#                 srv_response["id"] = "service_request:/roboy/cognition/vision/GetObject:" + str(i)
#                 srv_response["result"] = True
#                 srv_response["service"] = "/roboy/cognition/vision/GetObject"
#                 i += 1
#
#                 await websocket.send(json.dumps(srv_response))
#
#                 # print ("Got here somehow" + str(srv_response))
#
#             except Exception as e:
#                 logging.exception("Oopsie! Got an exception in GetObjectSrv")

async def lookatspeaker_service_callback(ObjectsQueue):
    async with websockets.connect('ws://localhost:9090') as websocket:

        # advertise the service
        await websocket.send("{ \"op\": \"advertise_service\",\
                      \"type\": \"roboy_communication_cognition/LookAtSpeaker\",\
                      \"service\": \"/roboy/cognition/vision/LookAtSpeaker\"\
                    }")

        i = 1  # counter for the service request IDs

        # wait for the service request, generate the answer, and send it back
        while True:
            try:
                # pdb.set_trace()
                request = await websocket.recv()

                srv_response = {}
                answer = {}
                # Look at speaker function must be called here
                answer["turned"] = False

                srv_response["values"] = answer
                srv_response["op"] = "service_response"
                srv_response["id"] = "service_request:/roboy/cognition/vision/LookAtSpeaker:" + str(i)
                srv_response["result"] = True
                srv_response["service"] = "/roboy/cognition/vision/Loo  kAtSpeaker"
                i += 1

                await websocket.send(json.dumps(srv_response))


            except Exception as e:
                logging.exception("Oopsie! Got an exception in LookAtSpeakerSrv")

async def detectface_service_callback(ObjectsQueue):
    async with websockets.connect('ws://localhost:9090') as websocket:

        # advertise the service
        await websocket.send("{ \"op\": \"advertise_service\",\
                      \"type\": \"roboy_communication_cognition/DetectFace\",\
                      \"service\": \"/roboy/cognition/vision/DetectFace\"\
                    }")

        i = 1  # counter for the service request IDs

        # wait for the service request, generate the answer, and send it back
        while True:
            try:
                # pdb.set_trace()
                request = await websocket.recv()

                srv_response = {}
                answer = {}
                # detectface function must be called here
                answer["face_detected"] = True

                srv_response["values"] = answer
                srv_response["op"] = "service_response"
                srv_response["id"] = "service_request:/roboy/cognition/vision/DetectFace:" + str(i)
                srv_response["result"] = True
                srv_response["service"] = "/roboy/cognition/vision/DetectFace"
                i += 1

                await websocket.send(json.dumps(srv_response))

            except Exception as e:
                logging.exception("Oopsie! Got an exception in DetectFaceSrv")


def startDescribeSceneSrv(ObjectsQueue):
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(describescene_service_callback(ObjectsQueue))

def startFindObjectsSrv(ObjectsQueue, RectQueue):
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(findobject_service_callback(ObjectsQueue, RectQueue))

# def startGetObjectSrv(ObjectsQueue):
#     logging.basicConfig(level=logging.INFO)
#     asyncio.get_event_loop().run_until_complete(getobject_service_callback(ObjectsQueue))

def startLookAtSpeakerSrv(ObjectsQueue):
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(lookatspeaker_service_callback(ObjectsQueue))

def startDetectFace(ObjectsQueue):
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(detectface_service_callback(ObjectsQueue))

