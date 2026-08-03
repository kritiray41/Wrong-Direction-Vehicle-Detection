# Quick standalone test to ensure it works with the detector
if __name__ == "__main__":
    import cv2
    import os
    from detection import VehicleDetector
    
    test_video_path = os.path.join("videos", "traffic_both.mp4")
    
    if os.path.exists(test_video_path):
        detector = VehicleDetector()
        # Initialize tracker
        tracker = VehicleTracker() 
        
        cap = cv2.VideoCapture(test_video_path)
        
        # INCREASED TO 10 FRAMES
        for i in range(10): 
            ret, frame = cap.read()
            if ret:
                # Phase 1: Get raw detections
                detections = detector.detect_vehicles(frame)
                
                # Phase 2: Get tracked detections
                tracked_detections = tracker.update_tracks(detections)
                
                print(f"--- Frame {i} ---")
                print(f"Detected {len(detections)} raw vehicles.")
                print(f"Tracking IDs assigned: {tracked_detections.tracker_id}")
                
        cap.release()
