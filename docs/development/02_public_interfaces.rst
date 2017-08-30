Public Interfaces
=================

Interfaces to other modules will be realized using ROS Communication. Currently 5 interfaces have been designed for communication, although not all have been fully implemented due to the not fully assembled Roboy to test it on.

- **FaceCoordinates message**: For each recognized face in the current frame, this message publishes the id, a boolean indicating whether the person is speaking and the 3D position (depth from ZED camera still to be implemented)::

    # returns: int32 id, bool speaking, float32 x, float32 y, float32 z
    
    rostopic echo /roboy/cognition/vision/FaceCoordinates

- **recognition service**: Service called to recognize a face. Given a object ID the name of the detected person is returned::

    # argument: int object_id
    # returns: String name

    rosservice call /recognize_face *object_id*

- **vision_object message**: This message is published for every camera frame an object was detected. The message includes ID type and position of the object.

Currently these interfaces are not implemented because of the constraint that ROS could not run using python 3. Because of this a workaround was implemented in **dirty_final_hack** branch. This will allow running ROS nodes using Python 2.7 and running the Vision module using python 3.6. The two modules then communicate using File I/O. For further details refer to github: https://github.com/Roboy/Vision/tree/dirty_final_hack
