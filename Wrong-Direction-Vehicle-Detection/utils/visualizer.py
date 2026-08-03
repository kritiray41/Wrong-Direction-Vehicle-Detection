import cv2
import supervision as sv
import time
from collections import deque

class VehicleHistory:
    def __init__(self, max_history=30):
        """
        Initializes the dictionary to store vehicle trajectories.
        """
        # Maintain vehicle history dictionary
        self.history = {}
        self.max_history = max_history

    def update_history(self, detections):
        """
        Calculates centroids and updates the history dictionary for tracked vehicles.
        
        Returns:
            dict: The current frame's centroids mapped by tracker_id.
        """
        current_centroids = {}
        
        # Ensure we have tracking IDs before proceeding
        if detections.tracker_id is None:
            return current_centroids
            
        for xyxy, tracker_id in zip(detections.xyxy, detections.tracker_id):
            # Calculate the centroid (center x, center y) of the bounding box
            cx = int((xyxy[0] + xyxy[2]) / 2)
            cy = int((xyxy[1] + xyxy[3]) / 2)
            centroid = (cx, cy)
            
            # Initialize history for new vehicles
            if tracker_id not in self.history:
                self.history[tracker_id] = deque(maxlen=self.max_history)
                
            # Store the trajectory
            self.history[tracker_id].append(centroid)
            current_centroids[tracker_id] = centroid
            
        return current_centroids


class VideoVisualizer:
    def __init__(self):
        self.box_annotator = sv.BoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()
        self.prev_frame_time = 0

    def draw_trails(self, frame, history_dict):
        """
        Draws movement trails on the video frame using the stored trajectories.
        """
        for tracker_id, points in history_dict.items():
            # Draw lines connecting the historical points
            for i in range(1, len(points)):
                if points[i - 1] is None or points[i] is None:
                    continue
                # Draw a yellow trail
                cv2.line(frame, points[i - 1], points[i], (0, 255, 255), 2)
        return frame

    def annotate_frame(self, frame, detections, history_dict=None):
        """
        Draws bounding boxes, labels, FPS, and optional movement trails.
        """
        # Draw movement trails if history is provided
        if history_dict:
            frame = self.draw_trails(frame, history_dict)

        # Draw bounding boxes
        annotated_frame = self.box_annotator.annotate(
            scene=frame.copy(), 
            detections=detections
        )
        
        # Display labels (Tracking ID + Confidence)
        if detections.tracker_id is not None:
            labels = [
                f"ID: {tracker_id} Conf: {confidence:.2f}"
                for tracker_id, confidence in zip(detections.tracker_id, detections.confidence)
            ]
            annotated_frame = self.label_annotator.annotate(
                scene=annotated_frame, 
                detections=detections, 
                labels=labels
            )

        # Display FPS
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - self.prev_frame_time) if self.prev_frame_time > 0 else 0
        self.prev_frame_time = new_frame_time
        
        cv2.putText(annotated_frame, f"FPS: {int(fps)}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return annotated_frame


# Updated Test Block
if __name__ == "__main__":
    import sys
    import os
    
    # Import Dev 1's backend logic
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from backend.detection import VehicleDetector
    from backend.tracking import VehicleTracker
    
    test_video_path = os.path.join("videos", "traffic_both.mp4")
    
    if os.path.exists(test_video_path):
        detector = VehicleDetector(conf_threshold=0.4)
        tracker = VehicleTracker()
        
        # Initialize Developer 2's new classes
        visualizer = VideoVisualizer()
        history = VehicleHistory()
        
        cap = cv2.VideoCapture(test_video_path)
        
        # Read 15 frames to build up a small trajectory trail
        for i in range(15):
            ret, frame = cap.read()
            if not ret:
                break
                
            detections = detector.detect_vehicles(frame)
            tracked_detections = tracker.update_tracks(detections)
            
            # Update history with the tracked detections
            history.update_history(tracked_detections)
            
            # Annotate frame with boxes, labels, and trails
            annotated_frame = visualizer.annotate_frame(frame, tracked_detections, history.history)
            
        # Save the 15th frame to visually check the trails
        output_image = "test_trails.jpg"
        cv2.imwrite(output_image, annotated_frame)
        print(f"Success! Check '{output_image}' to see the vehicle trails.")
        
        cap.release()