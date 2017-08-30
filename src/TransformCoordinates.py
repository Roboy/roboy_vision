def coordinate_transform(x_camera, y_camera, z)

        while True:
            try:
	            x_camera = Rects[id][0] ##x coordinate of current frame
                y_camera = Rects[id][1] ##y coordinate of current frame

                #transformation

                #placeholder for input from headposition via ROS - setup routine needs to be done with head
                #convert angles from quaternion/radians if necesaary
                yaw = 0.0 #rotation around spine, 0 position all the way to the left
                pitch = 0.0 #nodding head, 0 position all the way to the top
                roll = 0.0 #tilting head

                x_resolution = 1280
                y_resolution = 720
                
                width = 110 #degrees, given by ZED camera
                height = 62 #degrees, calculated from ZED camera

                x_step = x_resolution/width #step width - pixel per degree
                y_step = y_resolution/height #step width - pixel per degree

                max_yaw = 60 #degrees (0 left, 60 right)
				max_pitch = 40 #degrees (0 top, 40 bottom)
                max_roll = 10 #degrees

                x = x_camera + (yaw * x_step)
                y = y_camera + (pitch * y_step)
                z = 0.0 #input from ZED camera

                #rotation - to be tested again
                #x += cosine(roll) * x_camera - sin(roll) * y_camera
                #y += sine(roll) * x_camera + cosine(roll)* y_camera

                coordinates = {x, y, z}