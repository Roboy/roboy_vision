import dlib
import cv2
#import RosMsgUtil
import sys
import pickle
import asyncio
import websockets
import json as json

def DetectSpeaker(FacepointQueue,SpeakerQueue,FrameQueue,VisualQueue):
    distances = {1:list()}
    async with websockets.connect('ws://localhost:9090') as websocket:
    # advertise the message/topic
    await websocket.send("{ \"op\": \"advertise\",\
                      \"type\": \"vision_service/msg/FaceCoordinates\",\
                      \"topic\": \"/roboy/cognition/vision/FaceCoordinates\"\
                    }")

    while True:
        #dictionary of facial landmarks of each face
        Facepoints = pickle.loads(FacepointQueue.get())
        face_ids = Facepoints.keys()
        speakers = dict.fromkeys(face_ids)
        for id in face_ids:
            shape = Facepoints.get(id)
            # calculate mouth width and lip distances
            width = shape[54][0] - shape[48][0]  # width outer
            inner = shape[66][1] - shape[62][1]
            mouth = []
            mouth.append(width)
            mouth.append(inner)

            if  distances.get(id):
                distances_list = distances.get(id)
                distances_list.append(mouth)
                if(len(distances_list) > 5):
                    distances_list.pop(0)
                    
            else:
                distances[id] = [mouth]
                distances_list = distances.get(id)

            distances[id] = distances_list

            speaking = False
            if (inner >= (width / 9.5)):
                speaking = True
            elif len(distances_list) > 1:
                for i in (0, len(distances_list)-1):
                    distances_width = distances_list[i][0]
                    distances_inner = distances_list[i][1]
                    if (distances_inner >= (distances_width / 9)):
                        speaking = True
                        break
            speakers[id] = speaking

            coordinates = {shape[33][0], shape[33][1], 0}

            face = {'id': id,
                    'speaking': speaking,
                    'coordinates': coordinates}

            message["values"] = face
            message["op"] = "service_response"
            message["id"] = "message:/roboy/cognition/vision/FaceCoordinates:" + str(i)
            message["topic"] = "/roboy/cognition/vision/FaceCoordinates"
            i += 1

            await websocket.send(json.dumps(message))

            except Exception as e:
            logging.exception("Oopsie! Got an exception in vision/FaceCoordinates")

        SpeakerQueue.put(speakers)
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(service_callback())
