import cv2
from .utils import draw_text_with_background

class SpeedAndDistanceDrawer:
    def __init__(self):
        """
        Initialize the SpeedAndDistanceDrawer.
        
        This drawer visualizes speed and distance statistics for teams.
        """
        pass
    
    def calculate_team_stats(self, player_detections, team_assignments):
        """
        Calculate team-level speed and distance statistics.
        
        Args:
            player_detections (dict): Dictionary of player detections with stats.
            team_assignments (dict): Dictionary of team assignments.
        
        Returns:
            dict: Team statistics including average speed and total distance.
        """
        team_stats = {1: {'speeds': [], 'distances': []}, 
                     2: {'speeds': [], 'distances': []}}
        
        for player_id, detection in player_detections.items():
            team_id = team_assignments.get(player_id, 1)
            
            if isinstance(detection, dict):
                speed = detection.get('speed', 0)
                distance = detection.get('total_distance', 0)
                
                if speed > 0:
                    team_stats[team_id]['speeds'].append(speed)
                if distance > 0:
                    team_stats[team_id]['distances'].append(distance)
        
        # Calculate averages and totals
        result = {}
        for team_id in [1, 2]:
            speeds = team_stats[team_id]['speeds']
            distances = team_stats[team_id]['distances']
            
            avg_speed = sum(speeds) / len(speeds) if speeds else 0
            total_distance = sum(distances) if distances else 0
            
            result[team_id] = {
                'avg_speed': avg_speed,
                'total_distance': total_distance
            }
        
        return result
    
    def draw_speed_and_distance_stats(self, frame, player_detections, team_assignments):
        """
        Draw speed and distance statistics on the frame.
        
        Args:
            frame (numpy.ndarray): Input video frame.
            player_detections (dict): Dictionary of player detections with stats.
            team_assignments (dict): Dictionary of team assignments.
        
        Returns:
            numpy.ndarray: Frame with speed and distance statistics.
        """
        team_stats = self.calculate_team_stats(player_detections, team_assignments)
        
        # Draw team 1 stats
        team1_stats = team_stats[1]
        team1_text = f"Team 1 - Avg Speed: {team1_stats['avg_speed']:.1f} km/h, Total Dist: {team1_stats['total_distance']:.1f}m"
        frame = draw_text_with_background(frame, team1_text, (50, 130), 
                                        text_color=(255, 255, 255), bg_color=(0, 128, 0))
        
        # Draw team 2 stats
        team2_stats = team_stats[2]
        team2_text = f"Team 2 - Avg Speed: {team2_stats['avg_speed']:.1f} km/h, Total Dist: {team2_stats['total_distance']:.1f}m"
        frame = draw_text_with_background(frame, team2_text, (50, 170), 
                                        text_color=(255, 255, 255), bg_color=(0, 0, 128))
        
        return frame