import supervision as sv

class VehicleTracker:
    def __init__(self, track_thresh=0.25, track_buffer=30):
        """
        Initializes the ByteTrack object.
        
        Parameters:
            track_thresh (float): Detection confidence threshold for track activation.
            track_buffer (int): Number of frames to buffer when a track is lost.
        """
        # Initialize the supervision ByteTrack tracker
        self.tracker = sv.ByteTrack(
            track_thresh=track_thresh,
            track_buffer=track_buffer
        )

    def update_tracks(self, detections):
        """
        Updates the tracker with new detections and assigns tracking IDs.
        
        Parameters:
            detections (sv.Detections): The detections from the YOLO model.
            
        Returns:
            sv.Detections: The updated detections object, now containing a 'tracker_id' field.
        """
        # Pass the YOLO detections into ByteTrack
        tracked_detections = self.tracker.update_with_detections(detections)
        
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
        
        # Read two consecutive frames to test tracking
        for i in range(2):
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
