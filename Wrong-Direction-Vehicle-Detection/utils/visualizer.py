import cv2
import supervision as sv
import time

class VideoVisualizer:
    def __init__(self):
        """
        Initializes the annotators for drawing on the video frames.
        """
        # Annotator for drawing the bounding boxes
        self.box_annotator = sv.BoxAnnotator()
        
        # Annotator for drawing the text labels (like confidence scores)
        self.label_annotator = sv.LabelAnnotator()
        
        # Variable to help calculate FPS
        self.prev_frame_time = 0

    def annotate_frame(self, frame, detections):
        """
        Draws bounding boxes, confidence scores, and FPS on the frame.
        """
        # 1. Draw bounding boxes
        annotated_frame = self.box_annotator.annotate(
            scene=frame.copy(), 
            detections=detections
        )
        
        # 2. Display confidence scores
        # Extract confidence scores from the detections and format them as text
        if detections.confidence is not None:
            labels = [
                f"Conf: {confidence:.2f}"
                for confidence in detections.confidence
            ]
            annotated_frame = self.label_annotator.annotate(
                scene=annotated_frame, 
                detections=detections, 
                labels=labels
            )

        # 3. Display FPS
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - self.prev_frame_time) if self.prev_frame_time > 0 else 0
        self.prev_frame_time = new_frame_time
        
        cv2.putText(
            annotated_frame, 
            f"FPS: {int(fps)}", 
            (20, 50), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            1, 
            (0, 255, 0), 
            2
        )
        
        return annotated_frame

    def setup_video_writer(self, output_path, width, height, fps=30):
        """
        4. Export annotated video
        Sets up the OpenCV VideoWriter to save the final output.
        """
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        return cv2.VideoWriter(output_path, fourcc, fps, (width, height))

if __name__ == "__main__":
    import sys
    import os
    
    # Add the root project directory to Python's path so we can import Developer 1's code
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from backend.detection import VehicleDetector
    
    print("Testing VideoVisualizer...")
    test_video_path = os.path.join("videos", "traffic_both.mp4")
    
    if not os.path.exists(test_video_path):
        print(f"Error: Could not find video at {test_video_path}")
    else:
        # Initialize Dev 1's Detector and your Visualizer
        detector = VehicleDetector(conf_threshold=0.4)
        visualizer = VideoVisualizer()
        
        cap = cv2.VideoCapture(test_video_path)
        ret, frame = cap.read() # Read just the first frame
        
        if ret:
            # 1. Detect vehicles (Dev 1 logic)
            detections = detector.detect_vehicles(frame)
            
            # 2. Draw boxes and labels (Your logic)
            annotated_frame = visualizer.annotate_frame(frame, detections)
            
            # 3. Save the result to check it
            output_image = "test_visualization.jpg"
            cv2.imwrite(output_image, annotated_frame)
            print(f"Success! Check your project folder for '{output_image}' to see the drawn bounding boxes.")
            
        cap.release()