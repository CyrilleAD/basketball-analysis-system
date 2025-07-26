from ultralytics import YOLO
import supervision as sv
import pickle
import os
import sys
sys.path.append('../')
from utils import get_center_of_bbox

class BallTracker:
    def __init__(self, model_path):
        """
        Initialize the BallTracker with a YOLO model.
        
        Args:
            model_path (str): Path to the YOLO model file.
        """
        self.model = YOLO(model_path)

    def interpolate_ball_positions(self, ball_positions):
        """
        Interpolate missing ball positions between detected frames.
        
        Args:
            ball_positions (list): List of ball positions, with None for missing detections.
        
        Returns:
            list: List of ball positions with interpolated values.
        """
        ball_positions = [x.get(1, []) for x in ball_positions]
        # Convert to list of bbox coordinates
        df_ball_positions = pd.DataFrame(ball_positions, columns=['x1', 'y1', 'x2', 'y2'])
        
        # Interpolate missing values
        df_ball_positions = df_ball_positions.interpolate()
        df_ball_positions = df_ball_positions.bfill()
        
        ball_positions = [{1: x} for x in df_ball_positions.to_numpy().tolist()]
        
        return ball_positions

    def detect_frames(self, frames, read_from_stub=False, stub_path=None):
        """
        Detect ball across multiple video frames.
        
        Args:
            frames (list): List of video frames.
            read_from_stub (bool): Whether to read from cached results.
            stub_path (str): Path to cached detection results.
        
        Returns:
            list: List of ball detections for each frame.
        """
        ball_detections = []
        
        if read_from_stub and stub_path is not None and os.path.exists(stub_path):
            with open(stub_path, 'rb') as f:
                ball_detections = pickle.load(f)
            return ball_detections

        for frame in frames:
            player_dict = self.detect_frame(frame)
            ball_detections.append(player_dict)
        
        if stub_path is not None:
            with open(stub_path, 'wb') as f:
                pickle.dump(ball_detections, f)
                
        return ball_detections

    def detect_frame(self, frame):
        """
        Detect ball in a single frame.
        
        Args:
            frame (numpy.ndarray): Input video frame.
        
        Returns:
            dict: Dictionary containing ball detection information.
        """
        results = self.model(frame, imgsz=640)
        detections = sv.Detections.from_ultralytics(results[0])
        
        ball_dict = {}
        if len(detections) > 0:
            # Get the detection with highest confidence
            best_detection_idx = detections.confidence.argmax()
            bbox = detections.xyxy[best_detection_idx].tolist()
            ball_dict[1] = bbox
            
        return ball_dict