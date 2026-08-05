import cv2
import os
import sys

# Add the parent directory to the system path so we can import from 'utils'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.detection import VehicleDetector
from backend.tracking import VehicleTracker
from backend.direction import DirectionAnalyzer
from utils.visualizer import VideoVisualizer, VehicleHistory
from utils.logger import ViolationLogger

def run_dashboard_pipeline(video_source):
    """
    A generator that processes video frames and yields them for a frontend dashboard,
    along with any real-time violation data.
    """
    # Initialize all backend processing modules
    detector = VehicleDetector()
    tracker = VehicleTracker()
    direction_analyzer = DirectionAnalyzer(allowed_direction_vector=(0, 1))
    visualizer = VideoVisualizer()
    history = VehicleHistory()
    logger = ViolationLogger()
    
    cap = cv2.VideoCapture(video_source)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Detect and Track
        detections = detector.detect_vehicles(frame)
        tracked_detections = tracker.update_tracks(detections)
        
        # Update centroid history
        current_centroids = history.update_history(tracked_detections)
        
        # Wrong Direction Logic
        wrong_way_ids = []
        for tracker_id, current_centroid in current_centroids.items():
            trajectory = history.history[tracker_id]
            
            if len(trajectory) > 5: 
                previous_centroid = trajectory[0]
                is_wrong_way = direction_analyzer.check_wrong_direction(previous_centroid, current_centroid)
                
                if is_wrong_way:
                    wrong_way_ids.append(tracker_id)
                    logger.log_violation(tracker_id)
        
        # Draw bounding boxes, labels, and trails
        annotated_frame = visualizer.annotate_frame(frame, tracked_detections, history.history)
        
        # Add visual alert directly to the video if a wrong-way driver is found
        if wrong_way_ids:
            cv2.putText(
                annotated_frame, 
                f"WRONG WAY DETECTED: ID {wrong_way_ids}", 
                (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 
                1.5, 
                (0, 0, 255), 
                4
            )
            
        # Streamlit expects images in RGB format, but OpenCV uses BGR.
        # We must convert the color space before sending it to the frontend.
        frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        
        # Connect detection pipeline: Yield the frame and data instead of returning or saving
        yield frame_rgb, wrong_way_ids
        
    cap.release()