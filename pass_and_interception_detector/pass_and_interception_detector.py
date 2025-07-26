class PassAndInterceptionDetector:
    def __init__(self):
        """
        Initialize the PassAndInterceptionDetector.
        
        This detector identifies successful passes between teammates
        and interceptions by opposing teams.
        """
        pass
    
    def detect_passes(self, ball_acquisition_frames, team_assignments):
        """
        Detect successful passes between teammates.
        
        Args:
            ball_acquisition_frames (list): List of ball acquisition data for each frame.
            team_assignments (list): List of team assignments for each frame.
        
        Returns:
            list: List of detected passes with frame numbers and player IDs.
        """
        passes = []
        previous_ball_owner = None
        previous_team = None
        
        for frame_num, ball_acquisition in enumerate(ball_acquisition_frames):
            current_ball_owner = None
            current_team = None
            
            # Find current ball owner
            for player_id, _ in ball_acquisition.items():
                if player_id != 'team' and player_id != 'team_ball_control':
                    current_ball_owner = player_id
                    if frame_num < len(team_assignments) and player_id in team_assignments[frame_num]:
                        current_team = team_assignments[frame_num][player_id]
                    break
            
            # Detect pass if ball ownership changed within the same team
            if (previous_ball_owner is not None and 
                current_ball_owner is not None and 
                previous_ball_owner != current_ball_owner and
                previous_team == current_team and
                previous_team is not None):
                
                pass_info = {
                    'frame': frame_num,
                    'from_player': previous_ball_owner,
                    'to_player': current_ball_owner,
                    'team': current_team
                }
                passes.append(pass_info)
            
            if current_ball_owner is not None:
                previous_ball_owner = current_ball_owner
                previous_team = current_team
        
        return passes
    
    def detect_interceptions(self, ball_acquisition_frames, team_assignments):
        """
        Detect interceptions where ball possession changes between opposing teams.
        
        Args:
            ball_acquisition_frames (list): List of ball acquisition data for each frame.
            team_assignments (list): List of team assignments for each frame.
        
        Returns:
            list: List of detected interceptions with frame numbers and team changes.
        """
        interceptions = []
        previous_team = None
        
        for frame_num, ball_acquisition in enumerate(ball_acquisition_frames):
            current_team = None
            current_ball_owner = None
            
            # Find current ball owner and team
            for player_id, _ in ball_acquisition.items():
                if player_id != 'team' and player_id != 'team_ball_control':
                    current_ball_owner = player_id
                    if frame_num < len(team_assignments) and player_id in team_assignments[frame_num]:
                        current_team = team_assignments[frame_num][player_id]
                    break
            
            # Detect interception if team possession changed
            if (previous_team is not None and 
                current_team is not None and 
                previous_team != current_team):
                
                interception_info = {
                    'frame': frame_num,
                    'intercepting_player': current_ball_owner,
                    'intercepting_team': current_team,
                    'previous_team': previous_team
                }
                interceptions.append(interception_info)
            
            if current_team is not None:
                previous_team = current_team
        
        return interceptions