Context
--------

The Vision package receives realsense camera input which is then processed internally. Other than that it should also receive data from Roboy motor control about roboy's current position. This can be used to calculate the relative and absolute positions of detected objects.

The main output of the Vision Module will be detected objects and some object properties (e.g. detected face, name of person, mood, gender, ...). The receiver for this will be Natural language processing. This is illustrated in the following contect overview:

.. _context_within_environment:
.. figure:: images/Context.*
  :alt: Context Overview


  **Context diagram** - shows the birds eye view of the vision system (black box) described by this architecture within the ecosystem it is to be placed in. Shows orbit level interfaces on the user interaction and component scope.
