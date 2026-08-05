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

def run_pipeline(video_path, output_path):
    print(f"Starting pipeline on: {video_path}")
    print(f"Output will be saved to: {output_path}")
    
    # Initialize all modules
    detector = VehicleDetector()
    tracker = VehicleTracker()
    direction_analyzer = DirectionAnalyzer(allowed_direction_vector=(0, 1))
    visualizer = VideoVisualizer()
    history = VehicleHistory()
    logger = ViolationLogger()
    
    cap = cv2.VideoCapture(video_path)
    
    # Get video properties to configure the VideoWriter
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # Initialize the video writer
    writer = visualizer.setup_video_writer(output_path, width, height, fps)
    
    frame_count = 0
    
    # Process the entire video until it ends
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        # Print progress every 30 frames to terminal so you know it hasn't frozen
        if frame_count % 30 == 0:
            print(f"Processing frame {frame_count}...")
            
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
                    # THIS IS THE NEW LINE: Log the violation!
                    logger.log_violation(tracker_id)
        
        # Draw bounding boxes, labels, and trails
        annotated_frame = visualizer.annotate_frame(frame, tracked_detections, history.history)
        
        # Add visual alert directly to the video if a wrong-way driver is found
        if wrong_way_ids:
            cv2.putText(
                annotated_frame, 
                f"WRONG WAY DETECTED: ID {wrong_way_ids}", 
                (20, 100), # Positioned right below the FPS counter
                cv2.FONT_HERSHEY_SIMPLEX, 
                1.5, 
                (0, 0, 255), # Red text (BGR format)
                4
            )
            
        # Save the fully annotated frame into our output video file
        writer.write(annotated_frame)
        
    print("Video processing complete! Releasing resources...")
    cap.release()
    writer.release()

if __name__ == "__main__":
    test_video = os.path.join("videos", "traffic_both.mp4")
    output_video = "final_output.mp4" # The exported video file
    
    if os.path.exists(test_video):
        run_pipeline(test_video, output_video)
    else:
        print("Error: Test video not found.")