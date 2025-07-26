import cv2
from .utils import draw_triangle, get_center_of_bbox

class BallAquisitionDrawer:
    def __init__(self):
        """
        Initialize the BallAquisitionDrawer.
        
        This drawer visualizes ball possession and acquisition.
        """
        pass
    
    def draw_ball_acquisition(self, frame, ball_acquisition, player_detections, team_assignments):
        """
        Draw ball acquisition visualization on the frame.
        
        Args:
            frame (numpy.ndarray): Input video frame.
            ball_acquisition (dict): Ball acquisition data for the frame.
            player_detections (dict): Dictionary of player detections.
            team_assignments (dict): Dictionary of team assignments.
        
        Returns:
            numpy.ndarray: Frame with ball acquisition visualization.
        """
        for player_id, ball_bbox in ball_acquisition.items():
            if player_id == 'team' or player_id == 'team_ball_control':
                continue
                
            if player_id in player_detections:
                player_bbox = player_detections[player_id]
                
                # Get team color
                team_id = team_assignments.get(player_id, 1)
                color = (0, 255, 0) if team_id == 1 else (0, 0, 255)
                
                # Draw triangle above player with ball
                frame = draw_triangle(frame, player_bbox, color)
                
                # Draw ball
                if isinstance(ball_bbox, list) and len(ball_bbox) >= 4:
                    ball_center = get_center_of_bbox(ball_bbox)
                    cv2.circle(frame, ball_center, 10, (0, 255, 255), -1)
                    cv2.circle(frame, ball_center, 12, (0, 0, 0), 2)
        
        return frame