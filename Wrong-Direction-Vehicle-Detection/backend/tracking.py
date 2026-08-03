import supervision as sv

class VehicleTracker:
    def __init__(self, track_activation_threshold=0.25, lost_track_buffer=30):
        # Initialize the supervision ByteTrack tracker with the updated argument names
        self.tracker = sv.ByteTrack(
            track_activation_threshold=track_activation_threshold,
            lost_track_buffer=lost_track_buffer
        )

    def update_tracks(self, detections):
        # Add a small padding to bounding boxes to help tracker maintain ID
        # across fast-moving frames
        if not detections.is_empty():
            padded_xyxy = sv.pad_boxes(detections.xyxy, px=10, py=10)
            detections.xyxy = padded_xyxy
        
        # Safely handle the method name change in newer supervision versions
        if hasattr(self.tracker, 'update_with_detections'):
            tracked_detections = self.tracker.update_with_detections(detections)
        else:
            tracked_detections = self.tracker.update(detections)
        
        return tracked_detections

# Quick standalone test to ensure it works with the detector
if __name__ == "__main__":
    import cv2
    import os
    from detection import VehicleDetector
    
    test_video_path = os.path.join("videos", "traffic_both.mp4")
    
    if os.path.exists(test_video_path):
        detector = VehicleDetector()
        tracker = VehicleTracker()
        
        cap = cv2.VideoCapture(test_video_path)
        
        # INCREASED TO 15 FRAMES to allow the tracker time to initialize
        for i in range(15):
            ret, frame = cap.read()
            if ret:
                # Phase 1: Get raw detections
                detections = detector.detect_vehicles(frame)
                
                # Phase 2: Get tracked detections
                tracked_detections = tracker.update_tracks(detections)
                
                print(f"--- Frame {i} ---")
                print(f"Detected {len(detections)} raw vehicles.")
                
                # Check if tracker_id has been populated yet
                if tracked_detections.tracker_id is not None:
                    print(f"Tracking IDs assigned: {tracked_detections.tracker_id}")
                else:
                    print("Tracking IDs assigned: [] (Tracker initializing...)")
                
        cap.release()
    else:
        print("Test video not found!")