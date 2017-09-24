Public Interfaces(ROS)
=================

Interfaces to other modules will be realized using ROS Communication. Currently 5 interfaces have been designed for communication, although not all have been fully implemented due to the not fully assembled Roboy to test it on.
Due to version clashes and Rospy not being available for Python 3, the ROS Communication is implemented using websocket.

- **FaceCoordinates message**: For each recognized face in the current frame, this message publishes the id, a boolean indicating whether the person is speaking and the 3D position (depth from ZED camera still to be implemented)::

    # returns: int32 id, bool speaking, float32 x, float32 y, float32 z
    
    rostopic echo /roboy/cognition/vision/FaceCoordinates

- **NewFacialFeatures message**: For each unrecognized face in the current frame, this message publishes the facial features as a 128-dimensional vector and a boolean indicating whether the person is speaking::

    # returns: bool speaking, float64[128] ff
    
    rostopic echo /roboy/cognition/vision/NewFacialFeatures


- **DescribeScene service**: Service called to list all objects detected in the current frame, ordered from left to right::

    # argument:
    # returns: String[] objects_detected

    rosservice call /roboy/cognition/vision/DescribeScnee


- **FindObject service**: Service called to find an object in the current frame. Given an object type, the position of the object is returned::

    # argument: String type
    # returns: bool found, float32 x, float32 y, float32 z

    rosservice call /roboy/cognition/vision/FindObject *type*

- **LookAtSpeaker service**: Service called to turn towards to closest speaking face. Due to Roboy not being assembled yet, this service hasn't been implemented yet::

    # argument: 
    # returns: bool turned

    rosservice call /roboy/cognition/vision/LookAtSpeaker


A more detailed documentation of the ROS Communication as well as future plans can be viewed here: https://devanthro.atlassian.net/wiki/spaces/HT/pages/76402960/ROS+services+messages+overview
