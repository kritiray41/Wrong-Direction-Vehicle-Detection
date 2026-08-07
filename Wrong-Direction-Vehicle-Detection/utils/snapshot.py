import cv2
import os
from datetime import datetime

class SnapshotManager:
    def __init__(self, output_dir="snapshots"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        self.saved_ids = set()

    def save_snapshot(self, frame, tracker_id, bbox):
        if tracker_id in self.saved_ids:
            return None 

        x1, y1, x2, y2 = map(int, bbox)
        
        h, w, _ = frame.shape
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        cropped_vehicle = frame[y1:y2, x1:x2]
        
        if cropped_vehicle.size == 0:
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"vehicle_{tracker_id}_{timestamp}.jpg"
        filepath = os.path.join(self.output_dir, filename)

        cv2.imwrite(filepath, cropped_vehicle)
        self.saved_ids.add(tracker_id)
        print(f"[SNAPSHOT SAVED] {filepath}")
        return filepath