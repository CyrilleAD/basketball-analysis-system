import cv2
import os

def read_video(video_path):
    """
    Read video frames from a video file.
    
    Args:
        video_path (str): Path to the input video file.
    
    Returns:
        list: List of video frames as numpy arrays.
    """
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

def save_video(ouput_video_frames,output_video_path):
    """
    Save video frames to a video file.
    
    This function takes a list of video frames and saves them as a video file
    using OpenCV's VideoWriter.
    
    Args:
        ouput_video_frames (list): List of video frames as numpy arrays.
        output_video_path (str): Path where the video should be saved.
    """
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    if not os.path.exists(os.path.dirname(output_video_path)):
        os.makedirs(os.path.dirname(output_video_path))
    
    out = cv2.VideoWriter(output_video_path, fourcc, 24, (ouput_video_frames[0].shape[1], ouput_video_frames[0].shape[0]))
    for frame in ouput_video_frames:
        out.write(frame)
    out.release()