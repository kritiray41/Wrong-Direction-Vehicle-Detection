import cv2
from ultralytics import YOLO

print("OpenCV Version:", cv2.__version__)

# download the smallest YOLO model 
model = YOLO('yolov8n.pt') 
print("YOLOv8 loaded successfully!")