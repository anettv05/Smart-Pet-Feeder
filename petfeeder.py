
#cat_cascade = cv2.CascadeClassifier("/home/pi/Downloads/haarcascade_frontalcatface.xml")
import sys
sys.path.append('/usr/lib/python3/dist-packages')

# /home/pi/object-detection/detect_pet.py


#cat_cascade = cv2.CascadeClassifier("/home/pi/Downloads/haarcascade_frontalcatface.xml")
import sys
sys.path.append('/usr/lib/python3/dist-packages')

# /home/pi/object-detection/detect_pet.py

import numpy as np
import cv2

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

net = cv2.dnn.readNetFromCaffe(
    "/home/pi/object-detection/MobileNetSSD_deploy.prototxt",
    "/home/pi/object-detection/MobileNetSSD_deploy.caffemodel"
)

width = 640
height = 480
frame_size = int(width * height * 1.5)

while True:
    raw_frame = sys.stdin.buffer.read(frame_size)
    if len(raw_frame) != frame_size:
        break

    yuv = np.frombuffer(raw_frame, dtype=np.uint8).reshape((int(height * 1.5), width))
    frame = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)

    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.7:
            idx = int(detections[0, 0, i, 1])
            label = CLASSES[idx]
            if label in ["cat", "dog"]:
                print("PET", flush=True)
                sys.exit(0)

print("NONE", flush=True)
