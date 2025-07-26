import cv2
import numpy as np

class Homography:
    def __init__(self):
        """
        Initialize the Homography class for perspective transformation calculations.
        """
        pass
    
    def calculate_homography(self, source_points, target_points):
        """
        Calculate the homography matrix between source and target points.
        
        Args:
            source_points (numpy.ndarray): Source points in the original image.
            target_points (numpy.ndarray): Corresponding target points.
        
        Returns:
            numpy.ndarray or None: Homography matrix, or None if calculation fails.
        """
        if len(source_points) < 4 or len(target_points) < 4:
            return None
            
        try:
            # Ensure points are in the correct format
            source_points = np.array(source_points, dtype=np.float32)
            target_points = np.array(target_points, dtype=np.float32)
            
            # Calculate homography matrix
            homography_matrix, _ = cv2.findHomography(
                source_points, 
                target_points, 
                cv2.RANSAC
            )
            
            return homography_matrix
            
        except Exception as e:
            print(f"Error calculating homography: {e}")
            return None
    
    def apply_homography(self, points, homography_matrix):
        """
        Apply homography transformation to a set of points.
        
        Args:
            points (numpy.ndarray): Points to transform.
            homography_matrix (numpy.ndarray): Homography matrix.
        
        Returns:
            numpy.ndarray or None: Transformed points, or None if transformation fails.
        """
        if homography_matrix is None:
            return None
            
        try:
            # Ensure points are in the correct format
            if len(points.shape) == 2:
                points = points.reshape(-1, 1, 2)
            
            # Apply perspective transformation
            transformed_points = cv2.perspectiveTransform(
                points.astype(np.float32), 
                homography_matrix
            )
            
            return transformed_points
            
        except Exception as e:
            print(f"Error applying homography: {e}")
            return None