import numpy as np
import cv2
import sys
sys.path.append('../')
from utils import get_foot_position
from .homography import Homography

class TacticalViewConverter:
    def __init__(self, court_image_path='court.png'):
        """
        Initialize the TacticalViewConverter.
        
        Args:
            court_image_path (str): Path to the tactical court image.
        """
        self.court_image_path = court_image_path
        self.court_width = 94  # feet
        self.court_height = 50  # feet
        
        # Define the key points on the tactical court view
        self.tactical_court_keypoints = np.array([
            [0, 0],
            [self.court_width, 0],
            [0, self.court_height],
            [self.court_width, self.court_height]
        ], dtype=np.float32)
        
    def validate_keypoints(self, detected_keypoints):
        """
        Validate detected keypoints by checking proportional distances.
        
        Args:
            detected_keypoints (numpy.ndarray): Array of detected court keypoints.
        
        Returns:
            bool: True if keypoints are valid, False otherwise.
        """
        if len(detected_keypoints) < 4:
            return False
            
        # Check if keypoints form a reasonable rectangle
        # Calculate distances between consecutive points
        distances = []
        for i in range(4):
            p1 = detected_keypoints[i]
            p2 = detected_keypoints[(i + 1) % 4]
            distance = np.linalg.norm(p1 - p2)
            distances.append(distance)
        
        # Check if opposite sides are approximately equal
        ratio1 = distances[0] / distances[2] if distances[2] > 0 else 0
        ratio2 = distances[1] / distances[3] if distances[3] > 0 else 0
        
        # Allow 20% tolerance
        if 0.8 <= ratio1 <= 1.2 and 0.8 <= ratio2 <= 1.2:
            return True
        
        return False
    
    def convert_position_to_tactical_view(self, position, detected_keypoints):
        """
        Convert a position from video frame to tactical court view.
        
        Args:
            position (tuple): Position coordinates (x, y) in the video frame.
            detected_keypoints (numpy.ndarray): Array of detected court keypoints.
        
        Returns:
            tuple or None: Converted position in tactical view, or None if conversion fails.
        """
        if not self.validate_keypoints(detected_keypoints):
            return None
            
        try:
            # Create homography object
            homography = Homography()
            
            # Calculate homography matrix
            homography_matrix = homography.calculate_homography(
                detected_keypoints[:4], 
                self.tactical_court_keypoints
            )
            
            if homography_matrix is None:
                return None
            
            # Transform the position
            transformed_position = homography.apply_homography(
                np.array([position], dtype=np.float32).reshape(-1, 1, 2),
                homography_matrix
            )
            
            if transformed_position is not None and len(transformed_position) > 0:
                return tuple(transformed_position[0][0])
            
        except Exception as e:
            print(f"Error in position conversion: {e}")
            
        return None
    
    def convert_bbox_to_tactical_view(self, bbox, detected_keypoints):
        """
        Convert a bounding box from video frame to tactical court view.
        
        Args:
            bbox (list): Bounding box coordinates [x1, y1, x2, y2].
            detected_keypoints (numpy.ndarray): Array of detected court keypoints.
        
        Returns:
            tuple or None: Converted foot position in tactical view, or None if conversion fails.
        """
        foot_position = get_foot_position(bbox)
        return self.convert_position_to_tactical_view(foot_position, detected_keypoints)
    
    def convert_detections_to_tactical_view(self, detections, detected_keypoints):
        """
        Convert all detections from video frame to tactical court view.
        
        Args:
            detections (dict): Dictionary of detections with player IDs as keys.
            detected_keypoints (numpy.ndarray): Array of detected court keypoints.
        
        Returns:
            dict: Dictionary of converted positions in tactical view.
        """
        tactical_detections = {}
        
        for player_id, bbox in detections.items():
            tactical_position = self.convert_bbox_to_tactical_view(bbox, detected_keypoints)
            if tactical_position is not None:
                tactical_detections[player_id] = tactical_position
                
        return tactical_detections