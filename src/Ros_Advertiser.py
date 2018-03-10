from __future__ import print_function

import websockets
import time
import logging
import asyncio
import websockets


async def advertise_topics():
    async with websockets.connect('ws://localhost:9090') as websocket:

        await websocket.send("{ \"op\": \"advertise\",\
                            \"topic\": \"/roboy/cognition/vision/NewFacialFeatures\",\
                              \"type\": \"roboy_communication_cognition/NewFacialFeatures\"\
                            }")

        await websocket.send("{ \"op\": \"advertise\",\
                            \"topic\": \"/roboy/cognition/vision/FaceCoordinates\",\
                              \"type\": \"roboy_communication_cognition/FaceCoordinates\"\
                            }")
        while True:
            time.sleep(1)

def startAdvertising():
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(advertise_topics())
