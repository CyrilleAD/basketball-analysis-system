import argparse
import cv2
import numpy as np
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all necessary modules
from trackers import PlayerTracker, BallTracker
from team_assigner import TeamAssigner
from court_keypoint_detector import CourtKeypointDetector
from ball_aquisition import BallAquisitionDetector
from pass_and_interception_detector import PassAndInterceptionDetector
from speed_and_distance_calculator import SpeedAndDistanceCalculator
from tactical_view_converter import TacticalViewConverter
from utils import read_video, save_video
from drawers import (
    PlayerTracksDrawer,
    BallTracksDrawer,
    CourtKeypointDrawer,
    TeamBallControlDrawer,
    FrameNumberDrawer,
    PassInterceptionDrawer,
    TacticalViewDrawer,
    SpeedAndDistanceDrawer
)

# Import configuration
from configs import(
    STUBS_DEFAULT_PATH,
    PLAYER_DETECTOR_PATH,
    BALL_DETECTOR_PATH,
    COURT_KEYPOINT_DETECTOR_PATH,
    OUTPUT_VIDEO_PATH
)

def main():
    parser = argparse.ArgumentParser(description='Basketball Video Analysis')
    parser.add_argument('input_video', type=str, help='Path to input video file')
    parser.add_argument('--output_video', type=str, default=OUTPUT_VIDEO_PATH,
                        help='Path to output video file')
    parser.add_argument('--stub_path', type=str, default=STUBS_DEFAULT_PATH,
                        help='Path to stub directory')
    
    args = parser.parse_args()
    
    # Read video
    video_frames = read_video(args.input_video)
    
    # Initialize trackers and detectors
    player_tracker = PlayerTracker(PLAYER_DETECTOR_PATH)
    ball_tracker = BallTracker(BALL_DETECTOR_PATH)
    
    # Initialize court keypoint detector
    court_keypoint_detector = CourtKeypointDetector(COURT_KEYPOINT_DETECTOR_PATH)
    
    # Get player tracks
    player_tracks = player_tracker.get_object_tracks(
        video_frames,
        read_from_stub=True,
        stub_path=os.path.join(args.stub_path, 'player_track_stubs.pkl')
    )
    
    # Get ball tracks
    ball_tracks = ball_tracker.get_object_tracks(
        video_frames,
        read_from_stub=True,
        stub_path=os.path.join(args.stub_path, 'ball_track_stubs.pkl')
    )
    
    # Get court keypoints
    court_keypoints = court_keypoint_detector.get_court_keypoints(
        video_frames,
        read_from_stub=True,
        stub_path=os.path.join(args.stub_path, 'court_key_points_stub.pkl')
    )
    
    # Initialize team assigner
    team_assigner = TeamAssigner()
    team_assigner.choose_and_filter_players(court_keypoints, player_tracks)
    
    # Get player team assignments
    player_assignment = team_assigner.get_player_teams_across_frames(
        video_frames,
        player_tracks,
        read_from_stub=True,
        stub_path=os.path.join(args.stub_path, 'player_assignment_stub.pkl')
    )
    
    # Initialize ball acquisition detector
    ball_acquisition_detector = BallAquisitionDetector()
    ball_acquisition = ball_acquisition_detector.get_ball_acquisition_across_frames(
        player_tracks,
        ball_tracks
    )
    
    # Initialize pass and interception detector
    pass_interception_detector = PassAndInterceptionDetector()
    passes = pass_interception_detector.detect_passes(ball_acquisition, player_assignment)
    interceptions = pass_interception_detector.detect_interceptions(ball_acquisition, player_assignment)
    
    # Initialize tactical view converter
    court_image_path="./images/basketball_court.png"
    tactical_view_converter = TacticalViewConverter(court_image_path)
    
    # Initialize speed and distance calculator
    speed_distance_calculator = SpeedAndDistanceCalculator()
    speed_distance_data = speed_distance_calculator.add_speed_and_distance_to_tracks(player_tracks)
    
    # Initialize all drawers
    player_tracks_drawer = PlayerTracksDrawer()
    ball_tracks_drawer = BallTracksDrawer()
    court_keypoint_drawer = CourtKeypointDrawer()
    team_ball_control_drawer = TeamBallControlDrawer()
    frame_number_drawer = FrameNumberDrawer()
    pass_interception_drawer = PassInterceptionDrawer()
    tactical_view_drawer = TacticalViewDrawer(court_image_path)
    speed_distance_drawer = SpeedAndDistanceDrawer()
    
    # Process each frame
    output_video_frames = []
    
    for frame_num, frame in enumerate(video_frames):
        frame = frame.copy()
        
        # Draw court keypoints
        if frame_num in court_keypoints:
            frame = court_keypoint_drawer.draw_keypoints(frame, court_keypoints[frame_num])
        
        # Draw player tracks
        if frame_num in player_tracks:
            frame = player_tracks_drawer.draw_tracks(
                frame,
                player_tracks[frame_num],
                player_assignment[frame_num] if frame_num in player_assignment else {},
                ball_acquisition[frame_num] if frame_num in ball_acquisition else None
            )
        
        # Draw ball tracks
        if frame_num in ball_tracks:
            frame = ball_tracks_drawer.draw_tracks(frame, ball_tracks[frame_num])
        
        # Draw team ball control
        frame = team_ball_control_drawer.draw_team_ball_control(
            frame,
            frame_num,
            ball_acquisition
        )
        
        # Draw pass and interception stats
        frame = pass_interception_drawer.draw_pass_interception_stats(
            frame,
            passes,
            interceptions,
            player_assignment
        )
        
        # Draw speed and distance
        if frame_num in speed_distance_data:
            frame = speed_distance_drawer.draw_speed_and_distance(
                frame,
                speed_distance_data[frame_num]
            )
        
        # Draw tactical view
        if frame_num in court_keypoints and frame_num in player_tracks:
            frame = tactical_view_drawer.draw_tactical_view(
                frame,
                tactical_view_converter.court_image_path,
                court_keypoints[frame_num],
                player_tracks[frame_num],
                player_assignment[frame_num] if frame_num in player_assignment else {},
                ball_acquisition[frame_num] if frame_num in ball_acquisition else None
            )
        
        # Draw frame number
        frame = frame_number_drawer.draw_frame_number(frame, frame_num)
        
        output_video_frames.append(frame)
    
    # Save output video
    save_video(output_video_frames, args.output_video)
    print(f"Analysis complete! Output saved to: {args.output_video}")

if __name__ == '__main__':
    main()