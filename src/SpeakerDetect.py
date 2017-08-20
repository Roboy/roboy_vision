import dlib
import cv2
#import RosMsgUtil
import sys
import pickle

def DetectSpeaker(FacepointQueue,SpeakerQueue,FrameQueue,VisualQueue):
    distances = {1:list()}
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
        SpeakerQueue.put(speakers)
