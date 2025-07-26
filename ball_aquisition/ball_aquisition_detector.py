import sys
sys.path.append('../')
from utils import get_center_of_bbox, get_bbox_width

class BallAquisitionDetector():
    def __init__(self):
        """
        Initialize the BallAquisitionDetector.
        
        This detector identifies when players acquire possession of the basketball
        based on proximity between player and ball positions.
        """
        self.minimum_distance = 70

    def detect_frames(self, player_detections, ball_detections, assign_to_team=False, team_assignments=[]):
        """
        Detect ball acquisition across multiple frames.
        
        Args:
            player_detections (list): List of player detections for each frame.
            ball_detections (list): List of ball detections for each frame.
            assign_to_team (bool): Whether to assign ball possession to teams.
            team_assignments (list): List of team assignments for each frame.
        
        Returns:
            list: List of ball acquisition data for each frame.
        """
        ball_acquisition_frames = []
        for frame_num, player_detection in enumerate(player_detections):
            ball_acquisition = self.detect_frame(player_detection, ball_detections[frame_num], assign_to_team, team_assignments[frame_num] if assign_to_team else {})
            ball_acquisition_frames.append(ball_acquisition)
        return ball_acquisition_frames

    def detect_frame(self, player_detection, ball_detection, assign_to_team=False, team_assignment={}):
        """
        Detect ball acquisition in a single frame.
        
        Args:
            player_detection (dict): Player detections for the frame.
            ball_detection (dict): Ball detection for the frame.
            assign_to_team (bool): Whether to assign ball possession to teams.
            team_assignment (dict): Team assignments for the frame.
        
        Returns:
            dict: Ball acquisition information for the frame.
        """
        ball_acquisition = {}
        if 1 in ball_detection:
            ball_bbox = ball_detection[1]
            ball_position = get_center_of_bbox(ball_bbox)

            minimum_distance = 9999
            assigned_player = -1

            for player_id, player_bbox in player_detection.items():
                player_position = get_center_of_bbox(player_bbox)

                distance = abs(player_position[0] - ball_position[0]) + abs(player_position[1] - ball_position[1])
                if distance < self.minimum_distance:
                    if distance < minimum_distance:
                        minimum_distance = distance
                        assigned_player = player_id

            if assigned_player != -1:
                ball_acquisition[assigned_player] = ball_detection[1]

                if assign_to_team:
                    team_id = team_assignment.get(assigned_player, None)
                    if team_id is not None:
                        ball_acquisition['team'] = team_id
                        ball_acquisition['team_ball_control'] = team_id
        return ball_acquisition