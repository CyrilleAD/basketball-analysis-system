import cv2
import numpy as np

class TacticalViewDrawer:
    def __init__(self, court_image_path='court.png'):
        """
        Initialize the TacticalViewDrawer.
        
        Args:
            court_image_path (str): Path to the tactical court image.
        """
        self.court_image_path = court_image_path
        self.court_width = 94  # feet
        self.court_height = 50  # feet
        
        # Create a simple court background if image not available
        self.court_image = self.create_court_background()
    
    def create_court_background(self, width=940, height=500):
        """
        Create a simple basketball court background.
        
        Args:
            width (int): Court image width in pixels.
            height (int): Court image height in pixels.
        
        Returns:
            numpy.ndarray: Court background image.
        """
        court = np.ones((height, width, 3), dtype=np.uint8) * 139  # Brown court color
        
        # Draw court boundaries
        cv2.rectangle(court, (50, 50), (width-50, height-50), (255, 255, 255), 3)
        
        # Draw center circle
        center_x, center_y = width // 2, height // 2
        cv2.circle(court, (center_x, center_y), 60, (255, 255, 255), 2)
        
        # Draw center line
        cv2.line(court, (center_x, 50), (center_x, height-50), (255, 255, 255), 2)
        
        # Draw three-point lines (simplified)
        cv2.ellipse(court, (100, center_y), (120, 140), 0, -90, 90, (255, 255, 255), 2)
        cv2.ellipse(court, (width-100, center_y), (120, 140), 0, 90, 270, (255, 255, 255), 2)
        
        # Draw free throw circles
        cv2.circle(court, (150, center_y), 60, (255, 255, 255), 2)
        cv2.circle(court, (width-150, center_y), 60, (255, 255, 255), 2)
        
        return court
    
    def draw_tactical_view(self, frame, tactical_detections, team_assignments, ball_acquisition):
        """
        Draw the tactical view with player positions.
        
        Args:
            frame (numpy.ndarray): Input video frame.
            tactical_detections (dict): Dictionary of tactical positions.
            team_assignments (dict): Dictionary of team assignments.
            ball_acquisition (dict): Ball acquisition data.
        
        Returns:
            numpy.ndarray: Frame with tactical view overlay.
        """
        # Create a copy of the court image
        tactical_frame = self.court_image.copy()
        
        # Scale factor to convert from feet to pixels
        scale_x = tactical_frame.shape[1] / self.court_width
        scale_y = tactical_frame.shape[0] / self.court_height
        
        # Draw players
        for player_id, position in tactical_detections.items():
            if isinstance(position, (list, tuple)) and len(position) >= 2:
                # Convert position to pixel coordinates
                x = int(position[0] * scale_x)
                y = int(position[1] * scale_y)
                
                # Ensure coordinates are within bounds
                x = max(0, min(x, tactical_frame.shape[1] - 1))
                y = max(0, min(y, tactical_frame.shape[0] - 1))
                
                # Get team color
                team_id = team_assignments.get(player_id, 1)
                color = (0, 255, 0) if team_id == 1 else (0, 0, 255)
                
                # Draw player circle
                cv2.circle(tactical_frame, (x, y), 8, color, -1)
                cv2.circle(tactical_frame, (x, y), 10, (255, 255, 255), 2)
                
                # Draw player ID
                cv2.putText(tactical_frame, str(player_id), (x-5, y+5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                
                # Highlight ball possession
                if player_id in ball_acquisition:
                    cv2.circle(tactical_frame, (x, y), 15, (0, 255, 255), 3)
        
        # Resize tactical view to fit in corner of main frame
        tactical_height = frame.shape[0] // 3
        tactical_width = int(tactical_height * (tactical_frame.shape[1] / tactical_frame.shape[0]))
        tactical_resized = cv2.resize(tactical_frame, (tactical_width, tactical_height))
        
        # Overlay on main frame
        y_offset = frame.shape[0] - tactical_height - 20
        x_offset = frame.shape[1] - tactical_width - 20
        
        frame[y_offset:y_offset+tactical_height, x_offset:x_offset+tactical_width] = tactical_resized
        
        # Draw border around tactical view
        cv2.rectangle(frame, (x_offset-2, y_offset-2), 
                     (x_offset+tactical_width+2, y_offset+tactical_height+2), 
                     (255, 255, 255), 2)
        
        return frame