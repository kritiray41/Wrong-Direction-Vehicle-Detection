import cv2
from ultralytics import YOLO
import supervision as sv

class VehicleDetector:
    def __init__(self, model_path: str = "yolov8n.pt", conf_threshold: float = 0.4):
        """
        Initializes the YOLO model and sets vehicle filtering rules.
        """
        # Load the pre-trained YOLO model
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        
        # COCO Dataset IDs for vehicles: car (2), motorcycle (3), bus (5), truck (7)
        self.vehicle_classes = [2, 3, 5, 7]

    def detect_vehicles(self, frame):
        """
        Performs inference on a single frame and returns tracked vehicle detections.
        
        Parameters:
            frame (np.ndarray): The input video frame (OpenCV BGR image).
            
        Returns:
            sv.Detections: Supervision Detections object containing bounding boxes,
                           confidences, and class IDs.
        """
        # Perform YOLO inference filtered by vehicle classes and confidence threshold
        results = self.model(
            frame,
            conf=self.conf_threshold,
            classes=self.vehicle_classes,
            verbose=False
        )[0]
        
        # Convert Ultralytics YOLO results to a Supervision Detections object
        detections = sv.Detections.from_ultralytics(results)
        
        return detections

# Quick standalone test for Dev1
if __name__ == "__main__":
    import os
    
    # Path to one of the sample videos downloaded in Phase 0
    test_video_path = os.path.join("videos", "traffic_both.mp4")
    
    if not os.path.exists(test_video_path):
        print(f"Test video not found at '{test_video_path}'. Make sure video files exist in videos/ directory.")
    else:
        detector = VehicleDetector(conf_threshold=0.4)
        cap = cv2.VideoCapture(test_video_path)
        
        ret, frame = cap.read()
        if ret:
            detections = detector.detect_vehicles(frame)
            print(f"Successfully processed frame!")
            print(f"Detected {len(detections)} vehicles.")
            print(f"Bounding boxes array shape: {detections.xyxy.shape}")
        cap.release()
