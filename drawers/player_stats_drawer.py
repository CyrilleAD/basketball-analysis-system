import cv2
from .utils import draw_ellipse

class PlayerStatsDrawer:
    def __init__(self):
        """
        Initialize the PlayerStatsDrawer.
        
        This drawer visualizes player statistics including speed and distance.
        """
        pass
    
    def draw_player_stats(self, frame, player_detections, team_assignments):
        """
        Draw player statistics on the frame.
        
        Args:
            frame (numpy.ndarray): Input video frame.
            player_detections (dict): Dictionary of player detections.
            team_assignments (dict): Dictionary of team assignments.
        
        Returns:
            numpy.ndarray: Frame with drawn player statistics.
        """
        for track_id, bbox in player_detections.items():
            if isinstance(bbox, dict):
                # Extract bbox if it's in dictionary format
                actual_bbox = [bbox.get('x1', 0), bbox.get('y1', 0), 
                              bbox.get('x2', 0), bbox.get('y2', 0)]
                speed = bbox.get('speed', 0)
                distance = bbox.get('total_distance', 0)
            else:
                actual_bbox = bbox
                speed = 0
                distance = 0
            
            # Get team color
            team_id = team_assignments.get(track_id, 1)
            color = (0, 255, 0) if team_id == 1 else (0, 0, 255)
            
            # Draw player ellipse
            frame = draw_ellipse(frame, actual_bbox, color, track_id)
            
            # Draw speed and distance info
            if speed > 0 or distance > 0:
                x_center = int((actual_bbox[0] + actual_bbox[2]) / 2)
                y_bottom = int(actual_bbox[3])
                
                # Draw speed
                speed_text = f"Speed: {speed:.1f} km/h"
                cv2.putText(frame, speed_text, 
                           (x_center - 50, y_bottom + 40),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                
                # Draw distance
                distance_text = f"Dist: {distance:.1f}m"
                cv2.putText(frame, distance_text, 
                           (x_center - 50, y_bottom + 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        return frame