#!/usr/bin/env python

import json
from uuid import uuid4
# Note that this needs:
# sudo pip install websocket-client
# not the library called 'websocket'
import websockets
import yaml
import json as json
import importlib.util
# from roboy_cognition.roboy_communication_cognition.msg import FaceCoordinates
import sys
# sys.path.insert(0, '/home/roboy/cognition_ws/src/roboy_cognition/roboy_communication/roboy_communication_cognition/msg')

"""
Class to send ROS messages to a ROS master that has a rosbridge.
Author: Sammy Pfeiffer 
found here
https://gist.github.com/awesomebytes/67ef305a2d9072ac64b786af292f5907
"""


class WebsocketROSPublisher(object):
    def __init__(self, websocket_ip, port=9090):
        """
        Class to manage publishing to ROS thru a rosbridge websocket.
        :param str websocket_ip: IP of the machine with the rosbridge server.
        :param int port: Port of the websocket server, defaults to 9090.
        """
        print("Connecting to websocket: {}:{}".format(websocket_ip, port))
        self.ws = websockets
        self.ws.connect('ws://' + websocket_ip + ':' + str(port))
        print('Connected')
        # self.ws = websocket.create_connection(
        #     'ws://' + websocket_ip + ':' + str(port))
        self._advertise_dict = {}

    def _advertise(self, topic_name, topic_type):
        """
        Advertise a topic with it's type in 'package/Message' format.
        :param str topic_name: ROS topic name.
        :param str topic_type: ROS topic type, e.g. std_msgs/String.
        :returns str: ID to de-advertise later on.
        """
        new_uuid = str(uuid4())
        self._advertise_dict[new_uuid] = {'topic_name': topic_name,
                                          'topic_type': topic_type}
        advertise_msg = {"op": "advertise",
                         "id": new_uuid,
                         "topic": topic_name,
                         "type": topic_type
                         }
        self.ws.send(json.dumps(advertise_msg))
        return new_uuid

    def _unadvertise(self, uuid):
        unad_msg = {"op": "unadvertise",
                    "id": uuid,
                    # "topic": topic_name
                    }
        self.ws.send(json.dumps(unad_msg))

    def __del__(self):
        """Cleanup all advertisings"""
        d = self._advertise_dict
        for k in d:
            self._unadvertise(k)

    def _publish(self, topic_name, message):
        """
        Publish onto the already advertised topic the msg in the shape of
        a Python dict.
        :param str topic_name: ROS topic name.
        :param dict msg: Dictionary containing the definition of the message.
        """
        msg = {
            'op': 'publish',
            'topic': topic_name,
            'msg': message
        }
        json_msg = json.dumps(msg)
        self.ws.send(json_msg)

    def publish(self, topic_name, ros_message):
        """
        Publish on a topic given ROS message thru rosbridge.
        :param str topic_name: ROS topic name.
        :param * ros_message: Any ROS message instance, e.g. LaserScan()
            from sensor_msgs/LaserScan.
        """
        # First check if we already advertised the topic
        d = self._advertise_dict
        for k in d:
            if d[k]['topic_name'] == topic_name:
                # Already advertised, do nothing
                break
        else:
            # Not advertised, so we advertise
            # topic_type = ros_message._type
            # print('test')
            # print(ros_message['op'])
            topic_type = ros_message['op']
            self._advertise(topic_name, topic_type)
        # Converting ROS message to a dictionary thru YAML
        # ros_message_as_dict = yaml.load(ros_message.__str__())
        # Publishing
        self._publish(topic_name, ros_message)


if __name__ == '__main__':
    # facialfeatures = WebsocketROSPublisher('129.187.142.21')
    pub = WebsocketROSPublisher('localhost')
    # FaceCoordinates = importlib.util.spec_from_file_location("FaceCoordinates.msg","/home/roboy/cognition_ws/src/roboy_cognition/roboy_communication/roboy_communication_cognition/msg")

    # define #stored id to facial features
    face_coordinates = "{ \"op\": \"advertise\",\
                      \"type\": \"roboy_communication_cognition/facecoordinates\",\
                      \"topic\": \"/roboy/cognition/vision/facecoordinates\"\
                    }"
    i = 1
    message = {}
    message["id"] = 123
    message["speaking"] = True
    message["x"] = 100.00
    message["y"] = 100.00
    message["z"] = 100.00

    face_coord_msg={}
    face_coord_msg["op"] = "advertise"
    face_coord_msg["id"] = "message:/roboy/cognition/vision/FaceCoordinates:"
    face_coord_msg["topic"] ="/roboy/cognition/vision/FaceCoordinates"
    face_coord_msg["msg"] = message

    try:
        while True:
            print("Publishing FaceCoordinatesMsg")
            print(face_coord_msg['topic'])
            pub.publish('/FaceCoordinates', face_coord_msg)
            print("Done")
    except KeyboardInterrupt:
        pass



# int32 id
# #is person speaking?
# bool speaking
# #3D position of person in transformed global coordinates
# float32 x
# float32 y
# float32 z


    # print('Hello')
    # # print(FaceCoordinates)
    # print('lol')
    # try:
    #     while True:
    #         print("Publishing NewFacialFeaturesMsg")
    #         facialfeatures.publish('/FaceCoordinates', fc)
    #         print("Done")
    # except KeyboardInterrupt:
    #     pass


#     from sensor_msgs.msg import LaserScan
#     pub = WebsocketROSPublisher('192.168.1.31')
#     ls = LaserScan()
#     try:
#         while True:
#             print("Publishing laser scan")
#             pub.publish('/laser_fake_topic', ls)
#             print("Done")
#     except KeyboardInterrupt:
# pass