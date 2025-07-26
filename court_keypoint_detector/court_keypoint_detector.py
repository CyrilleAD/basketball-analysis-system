from ultralytics import YOLO
import supervision as sv
import pickle
import os
import sys
sys.path.append('../')

class CourtKeypointDetector:
    def __init__(self, model_path):
        """
        Initialize the CourtKeypointDetector with a YOLO model.
        
        Args:
            model_path (str): Path to the YOLO model file.
        """
        self.model = YOLO(model_path)

    def predict(self, frame, read_from_stub=False, stub_path=None):
        """
        Detect court keypoints in a frame.
        
        Args:
            frame (numpy.ndarray): Input video frame.
            read_from_stub (bool): Whether to read from cached results.
            stub_path (str): Path to cached detection results.
        
        Returns:
            list: List of detected keypoint coordinates.
        """
        if read_from_stub and stub_path is not None and os.path.exists(stub_path):
            with open(stub_path, 'rb') as f:
                keypoints = pickle.load(f)
            return keypoints

        results = self.model(frame, imgsz=640)
        
        keypoints = []
        for result in results:
            if result.keypoints is not None:
                keypoints = result.keypoints.xy.cpu().numpy()[0]
                break
        
        if stub_path is not None:
            with open(stub_path, 'wb') as f:
                pickle.dump(keypoints, f)
                
        return keypoints