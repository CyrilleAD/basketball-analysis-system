import cv2
from .utils import draw_text_with_background

class TeamBallControlDrawer:
    def __init__(self):
        """
        Initialize the TeamBallControlDrawer.
        
        This drawer visualizes team ball control statistics.
        """
        self.team_ball_control_frames = {1: 0, 2: 0}
    
    def update_team_ball_control(self, ball_acquisition):
        """
        Update team ball control statistics.
        
        Args:
            ball_acquisition (dict): Ball acquisition data for the frame.
        """
        if 'team_ball_control' in ball_acquisition:
            team = ball_acquisition['team_ball_control']
            if team in self.team_ball_control_frames:
                self.team_ball_control_frames[team] += 1
    
    def calculate_ball_control_percentage(self):
        """
        Calculate ball control percentage for each team.
        
        Returns:
            dict: Ball control percentages for each team.
        """
        total_frames = sum(self.team_ball_control_frames.values())
        if total_frames == 0:
            return {1: 0, 2: 0}
        
        return {
            1: (self.team_ball_control_frames[1] / total_frames) * 100,
            2: (self.team_ball_control_frames[2] / total_frames) * 100
        }
    
    def draw_team_ball_control(self, frame):
        """
        Draw team ball control statistics on the frame.
        
        Args:
            frame (numpy.ndarray): Input video frame.
        
        Returns:
            numpy.ndarray: Frame with ball control statistics.
        """
        percentages = self.calculate_ball_control_percentage()
        
        # Draw team 1 ball control
        team1_text = f"Team 1 Ball Control: {percentages[1]:.1f}%"
        frame = draw_text_with_background(frame, team1_text, (50, 210), 
                                        text_color=(255, 255, 255), bg_color=(0, 128, 0))
        
        # Draw team 2 ball control
        team2_text = f"Team 2 Ball Control: {percentages[2]:.1f}%"
        frame = draw_text_with_background(frame, team2_text, (50, 250), 
                                        text_color=(255, 255, 255), bg_color=(0, 0, 128))
        
        return frame