import cv2
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    frame = frame[0:376, 0:500]
    cv2.imshow("Video",frame)
#
