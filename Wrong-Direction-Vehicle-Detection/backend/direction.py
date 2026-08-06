import numpy as np

class DirectionAnalyzer:
    def __init__(self):
        # We track each vehicle ID so a single slow car doesn't add 100 tallies to the count
        self.vehicle_directions = {} 
        
        # Tallies to learn the "normal" flow of the road
        self.left_up = 0
        self.left_down = 0
        self.right_up = 0
        self.right_down = 0
        
        # Minimum number of cars needed to establish what is "normal"
        self.min_samples = 3 

    def check_wrong_direction(self, tracker_id, trajectory, frame_width):
        # We need a decent path history to judge direction
        if len(trajectory) < 5:
            return False

        # Check total Y-axis travel from where the car started to where it is now
        start_centroid = trajectory[0]
        current_centroid = trajectory[-1]
        
        dy = current_centroid[1] - start_centroid[1]
        
        # Ignore horizontal movements or parked cars
        if abs(dy) < 5.0:
            return False

        is_left_half = current_centroid[0] < (frame_width / 2)
        is_moving_down = dy > 0  # In OpenCV, Y increases as you go down the screen

        # 1. TALLY THE FLOW (Watch and Learn)
        # Only register a car's direction once so the tallies are accurate
        if tracker_id not in self.vehicle_directions:
            self.vehicle_directions[tracker_id] = is_moving_down
            
            if is_left_half:
                if is_moving_down: self.left_down += 1
                else: self.left_up += 1
            else:
                if is_moving_down: self.right_down += 1
                else: self.right_up += 1

        # 2. CATCH THE OUTLIERS (Flag the Violators)
        if is_left_half:
            if (self.left_up + self.left_down) >= self.min_samples:
                if self.left_up > self.left_down: # Normal flow is UP
                    return is_moving_down         # Violation if moving DOWN
                elif self.left_down > self.left_up: # Normal flow is DOWN
                    return not is_moving_down     # Violation if moving UP
        else:
            if (self.right_up + self.right_down) >= self.min_samples:
                if self.right_up > self.right_down: # Normal flow is UP
                    return is_moving_down
                elif self.right_down > self.right_up: # Normal flow is DOWN
                    return not is_moving_down

        return False