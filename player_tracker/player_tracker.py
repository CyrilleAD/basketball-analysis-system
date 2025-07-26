from ultralytics import YOLO
import supervision as sv
import pickle
import os
import sys
sys.path.append('../')
from utils import get_center_of_bbox, get_bbox_width

class PlayerTracker:
    def __init__(self, model_path):
        """
        Initialize the PlayerTracker with a YOLO model.
        
        Args:
            model_path (str): Path to the YOLO model file.
        """
        self.model = YOLO(model_path)
        self.tracker = sv.ByteTracker()

    def choose_and_filter_players(self, court_keypoints, player_detections):
        """
        Filter player detections to only include those within the court boundaries.
        
        Args:
            court_keypoints (list): List of court keypoint coordinates.
            player_detections (sv.Detections): Player detection results.
        
        Returns:
            sv.Detections: Filtered player detections within court boundaries.
        """
        bbox_list = player_detections.xyxy.tolist()
        bbox_list = [get_center_of_bbox(bbox) for bbox in bbox_list]

        chosen_players = []
        for i, bbox in enumerate(bbox_list):
            if bbox[0] < court_keypoints[0][0] or bbox[0] > court_keypoints[1][0]:
                continue
            if bbox[1] < court_keypoints[0][1] or bbox[1] > court_keypoints[2][1]:
                continue
            chosen_players.append(i)
        
        player_detections_filtered = player_detections[chosen_players]
        return player_detections_filtered

    def detect_frames(self, frames, read_from_stub=False, stub_path=None):
        """
        Detect and track players across multiple video frames.
        
        Args:
            frames (list): List of video frames.
            read_from_stub (bool): Whether to read from cached results.
            stub_path (str): Path to cached detection results.
        
        Returns:
            list: List of player detections for each frame.
        """
        player_detections = []
        
        if read_from_stub and stub_path is not None and os.path.exists(stub_path):
            with open(stub_path, 'rb') as f:
                player_detections = pickle.load(f)
            return player_detections

        for frame in frames:
            player_dict = self.detect_frame(frame)
            player_detections.append(player_dict)
        
        if stub_path is not None:
            with open(stub_path, 'wb') as f:
                pickle.dump(player_detections, f)
                
        return player_detections

    def detect_frame(self, frame):
        """
        Detect and track players in a single frame.
        
        Args:
            frame (numpy.ndarray): Input video frame.
        
        Returns:
            dict: Dictionary containing player detections and tracking information.
        """
        results = self.model(frame, imgsz=1280)
        detections = sv.Detections.from_ultralytics(results[0])
        
        # Filter for person class (class_id = 0 in COCO dataset)
        detections = detections[detections.class_id == 0]
        
        # Update tracker
        detections = self.tracker.update_with_detections(detections)
        
        player_dict = {}
        for frame_detection, track_id in zip(detections.xyxy, detections.tracker_id):
            bbox = frame_detection.tolist()
            player_dict[track_id] = bbox
            
        return player_dict