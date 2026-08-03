import supervision as sv

class VehicleTracker:
    # 1. Lower the track_thresh to make activation easier
    def __init__(self, track_thresh=0.1, match_thresh=0.8, track_buffer=30):
        self.tracker = sv.ByteTrack(
            track_thresh=track_thresh,
            match_thresh=match_thresh,
            track_buffer=track_buffer
        )

    def update_tracks(self, detections):
        # 2. Add padding to the bounding boxes to force overlap
        padded_xyxy = sv.pad_boxes(detections.xyxy, px=10, py=10)
        detections.xyxy = padded_xyxy
        
        # Now update the tracker
        tracked_detections = self.tracker.update_with_detections(detections)
        
        return tracked_detections

# Test script
if __name__ == "__main__":
    import cv2
    import os
    from detection import VehicleDetector
    
    test_video_path = os.path.join("videos", "traffic_both.mp4")
    
    if os.path.exists(test_video_path):
        detector = VehicleDetector()
        tracker = VehicleTracker()
        
        cap = cv2.VideoCapture(test_video_path)
        
        # Read a few more frames to give ByteTrack time to initialize
        for i in range(5):
            ret, frame = cap.read()
            if ret:
                detections = detector.detect_vehicles(frame)
                tracked_detections = tracker.update_tracks(detections)
                
                print(f"--- Frame {i} ---")
                print(f"Tracking IDs assigned: {tracked_detections.tracker_id}")
                
        cap.release()
