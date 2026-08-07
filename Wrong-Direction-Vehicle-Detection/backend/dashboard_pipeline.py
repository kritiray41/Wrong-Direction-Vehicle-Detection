import cv2
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.detection import VehicleDetector
from backend.tracking import VehicleTracker
from backend.direction import DirectionAnalyzer
from utils.visualizer import VideoVisualizer, VehicleHistory
from utils.logger import ViolationLogger
from utils.snapshot import SnapshotManager

def run_dashboard_pipeline(video_source):
    detector = VehicleDetector()
    tracker = VehicleTracker()
    direction_analyzer = DirectionAnalyzer()
    visualizer = VideoVisualizer()
    history = VehicleHistory()
    logger = ViolationLogger()
    snapshot_mgr = SnapshotManager()  
    
    cap = cv2.VideoCapture(video_source)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        detections = detector.detect_vehicles(frame)
        tracked_detections = tracker.update_tracks(detections)
        current_centroids = history.update_history(tracked_detections)
        
        wrong_way_ids = []
        for tracker_id, current_centroid in current_centroids.items():
            trajectory = history.history[tracker_id]
            
            # Pass the tracker ID, the full path trajectory, and the frame width
            is_wrong_way = direction_analyzer.check_wrong_direction(tracker_id, trajectory, frame.shape[1])
            
            if is_wrong_way:
                clean_id = int(tracker_id) 
                wrong_way_ids.append(clean_id)
                logger.log_violation(clean_id)
                
                if hasattr(tracked_detections, 'tracker_id') and tracked_detections.tracker_id is not None:
                    idx = np.where(tracked_detections.tracker_id == tracker_id)[0]
                    if len(idx) > 0:
                        bbox = tracked_detections.xyxy[idx[0]]
                        snapshot_mgr.save_snapshot(frame, clean_id, bbox)

        annotated_frame = visualizer.annotate_frame(frame, tracked_detections, history.history)
        
        if wrong_way_ids:
            # Limit to the 5 most recent IDs to prevent horizontal text overlapping/overflow
            display_ids = ", ".join([str(i) for i in wrong_way_ids[-5:]])
            alert_text = f"VIOLATION - IDs: {display_ids}"
            
            # OpenCV Text Setup
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1.0
            thickness = 3
            
            # Calculate text size to draw a perfect background box
            (text_width, text_height), baseline = cv2.getTextSize(alert_text, font, font_scale, thickness)
            x, y = 20, 60
            
            # Draw Solid Black Rectangle (Background)
            cv2.rectangle(annotated_frame, (x - 5, y - text_height - 5), (x + text_width + 5, y + baseline + 5), (0, 0, 0), cv2.FILLED)
            
            # Draw Neon Red Text (Foreground)
            cv2.putText(annotated_frame, alert_text, (x, y), font, font_scale, (0, 0, 255), thickness)
            
        frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        yield frame_rgb, wrong_way_ids
        
    cap.release()