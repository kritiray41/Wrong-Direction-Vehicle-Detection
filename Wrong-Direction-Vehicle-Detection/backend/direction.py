import numpy as np

class DirectionAnalyzer:
    def __init__(self, allowed_direction_vector=(0, 1)):
        """
        Initializes the direction analyzer.
        
        Parameters:
            allowed_direction_vector (tuple): A vector (x, y) representing the legal 
                                              traffic flow direction. 
                                              Default (0, 1) means moving DOWN the screen.
                                              (0, -1) would mean moving UP the screen.
        """
        self.allowed_vector = np.array(allowed_direction_vector)

    def compute_movement_vector(self, previous_centroid, current_centroid):
        """
        Computes the movement vector between two centroid points.
        """
        return np.array(current_centroid) - np.array(previous_centroid)

    def check_wrong_direction(self, previous_centroid, current_centroid):
        """
        Uses dot product to make a wrong direction decision.
        
        Returns:
            bool: True if moving in the wrong direction, False otherwise.
        """
        # 1. Compute movement vector
        movement_vector = self.compute_movement_vector(previous_centroid, current_centroid)
        
        # If the vehicle hasn't moved (vector length is 0), it's not going the wrong way
        if np.linalg.norm(movement_vector) == 0:
            return False
            
        # 2. Dot-product implementation
        dot_product = np.dot(movement_vector, self.allowed_vector)
        
        # 3. Wrong direction decision
        # A negative dot product means the angle between vectors is > 90 degrees
        if dot_product < 0:
            return True
            
        return False