Public Interfaces
=================

Interfaces to other modules will be realized using ROS Communication. Currently 3 interfaces have been designed for communication with NLP:

- **wakeup service**: Service to be called to test whether a face is recognized within certain distance. Used by NLP for wakeup::

    argument: (none)
    returns: Bool face_nearby

- **recognition service**: Service called to recognize a face. Given a object ID the name of the detected person is returned::

    argument: int object_id
    returns: String name

- **vision_object message**: This message is published for every camera frame an object was detected. The message includes ID type and position of the object.

Currently these interfaces are not implemented because of the constraint that ROS could not run using python 3. Because of this a workaround was implemented in **dirty_final_hack** branch. This will allow running ROS nodes using Python 2.7 and running the Vision module using python 3.6. The two modules then communicate using File I/O. For further details refer to github: https://github.com/Roboy/Vision/tree/dirty_final_hack