import cv2

vs = cv2.VideoCapture(0)

while True:
    """
    grab the frame from the threaded video stream, resize it to
    have a maximum width of 800 pixels, and convert it to
    grayscale"""

    # cam.retrieve_image(mat, sl.PyVIEW.PyVIEW_LEFT)
    # frame = mat.get_data()
    ok, frame = vs.read()
    if (ok):
        cv2.imshow("frame", frame)
    else:
        print("not ok")