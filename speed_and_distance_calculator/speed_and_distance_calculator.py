import sys
sys.path.append('../')
from utils import get_center_of_bbox, get_foot_position
import math

class SpeedAndDistanceCalculator:
    def __init__(self):
        """
        Initialize the SpeedAndDistanceCalculator.
        
        This calculator computes player speeds and distances covered
        based on their positions across video frames.
        """
        self.frame_window = 5
        self.frame_rate = 24
    
    def add_speed_and_distance_to_tracks(self, tracks):
        """
        Add speed and distance information to player tracks.
        
        Args:
            tracks (list): List of player tracking data for each frame.
        
        Returns:
            list: Updated tracks with speed and distance information.
        """
        total_distance = {}
        
        for object_id in tracks[0].keys():
            if object_id == "ball" or object_id == "referees":
                continue
            total_distance[object_id] = 0
        
        for frame_num in range(1, len(tracks)):
            for object_id in tracks[frame_num].keys():
                if object_id == "ball" or object_id == "referees":
                    continue
                
                if object_id in tracks[frame_num-1]:
                    prev_position = get_foot_position(tracks[frame_num-1][object_id])
                    curr_position = get_foot_position(tracks[frame_num][object_id])
                    
                    distance_covered = self.calculate_distance(prev_position, curr_position)
                    
                    if object_id not in total_distance:
                        total_distance[object_id] = 0
                    
                    total_distance[object_id] += distance_covered
                    
                    tracks[frame_num][object_id]['total_distance'] = total_distance[object_id]
        
        # Calculate speed
        for frame_num in range(len(tracks)):
            for object_id in tracks[frame_num].keys():
                if object_id == "ball" or object_id == "referees":
                    continue
                
                speed = self.calculate_speed(tracks, object_id, frame_num)
                tracks[frame_num][object_id]['speed'] = speed
        
        return tracks
    
    def calculate_distance(self, position1, position2):
        """
        Calculate the Euclidean distance between two positions.
        
        Args:
            position1 (tuple): First position (x, y).
            position2 (tuple): Second position (x, y).
        
        Returns:
            float: Distance in pixels (converted to meters).
        """
        pixel_distance = math.sqrt((position1[0] - position2[0])**2 + (position1[1] - position2[1])**2)
        # Convert pixels to meters (approximate conversion)
        meters = pixel_distance * 0.05  # Assuming 1 pixel = 0.05 meters
        return meters
    
    def calculate_speed(self, tracks, object_id, frame_num):
        """
        Calculate the speed of an object over a window of frames.
        
        Args:
            tracks (list): List of tracking data for each frame.
            object_id (int): ID of the object to calculate speed for.
            frame_num (int): Current frame number.
        
        Returns:
            float: Speed in km/h.
        """
        total_distance = 0
        frames_considered = 0
        
        for i in range(max(0, frame_num - self.frame_window + 1), frame_num + 1):
            if i > 0 and object_id in tracks[i] and object_id in tracks[i-1]:
                prev_position = get_foot_position(tracks[i-1][object_id])
                curr_position = get_foot_position(tracks[i][object_id])
                
                distance = self.calculate_distance(prev_position, curr_position)
                total_distance += distance
                frames_considered += 1
        
        if frames_considered == 0:
            return 0
        
        # Calculate speed in m/s
        time_elapsed = frames_considered / self.frame_rate
        speed_ms = total_distance / time_elapsed
        
        # Convert to km/h
        speed_kmh = speed_ms * 3.6
        
        return speed_kmh