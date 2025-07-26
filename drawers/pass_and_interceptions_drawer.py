import cv2
from .utils import draw_text_with_background

class PassInterceptionDrawer:
    def __init__(self):
        """
        Initialize the PassInterceptionDrawer.
        
        This drawer visualizes pass and interception statistics.
        """
        self.pass_count = {1: 0, 2: 0}
        self.interception_count = {1: 0, 2: 0}
    
    def update_pass_count(self, passes):
        """
        Update pass count based on detected passes.
        
        Args:
            passes (list): List of detected passes.
        """
        for pass_info in passes:
            team = pass_info.get('team', 1)
            if team in self.pass_count:
                self.pass_count[team] += 1
    
    def update_interception_count(self, interceptions):
        """
        Update interception count based on detected interceptions.
        
        Args:
            interceptions (list): List of detected interceptions.
        """
        for interception_info in interceptions:
            team = interception_info.get('intercepting_team', 1)
            if team in self.interception_count:
                self.interception_count[team] += 1
    
    def draw_pass_and_interception_stats(self, frame):
        """
        Draw pass and interception statistics on the frame.
        
        Args:
            frame (numpy.ndarray): Input video frame.
        
        Returns:
            numpy.ndarray: Frame with pass and interception statistics.
        """
        # Draw team 1 stats
        team1_text = f"Team 1 - Passes: {self.pass_count[1]}, Interceptions: {self.interception_count[1]}"
        frame = draw_text_with_background(frame, team1_text, (50, 50), 
                                        text_color=(255, 255, 255), bg_color=(0, 128, 0))
        
        # Draw team 2 stats
        team2_text = f"Team 2 - Passes: {self.pass_count[2]}, Interceptions: {self.interception_count[2]}"
        frame = draw_text_with_background(frame, team2_text, (50, 90), 
                                        text_color=(255, 255, 255), bg_color=(0, 0, 128))
        
        return frame