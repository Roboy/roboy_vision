import dlib
import cv2
import RosMsgUtil


def DetectSpeaker(FacepointQueue,SpeakerQueue):

    #dictionary to keep history of distances of each face
    distances = dict.fromkeys('0', list())

    #dictionary of facial landmarks of each face
    Facepoints = FacepointQueue.get()

    face_ids = Facepoints.keys()
    speakers = dict.fromkeys(face_ids)
    for id in face_ids:
        shape = Facepoints.get(id)

        # calculate mouth width and lip distances

        width = (shape[54][0] - shape[48][0])  # width outer
        inner = shape[66][1] - shape[62][1]

        mouth = []
        mouth.append(width)
        mouth.append(inner)

        distances_list = dict.get(id)
        distances_list.insert(0, mouth)
        if(len(distances_list) > 5):
            distances_list.pop(5)


        speaking = False
        if (inner >= (width / 9.5)):
            speaking = True
        else:
            for i in (1, len(distances_list)):
                distances_width = distances_list[i][0]
                distances_inner = distances_list[i][1]
                if (distances_inner >= (distances_width / 9)):
                    speaking = True
                    break

        speakers.setdefault(id, speaking)

    SpeakerQueue.put(speakers)