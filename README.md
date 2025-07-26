# Basketball Video Analysis System

An advanced basketball video analysis system that uses computer vision and machine learning to analyze basketball games. The system provides comprehensive tracking, team assignment, tactical analysis, and performance metrics.

## Features

### Core Tracking
- **Player Detection & Tracking**: YOLO-based player detection with multi-object tracking
- **Ball Detection & Tracking**: Specialized ball tracking with trajectory analysis
- **Court Keypoint Detection**: Automatic detection of court boundaries and key areas

### Team Analysis
- **Automatic Team Assignment**: AI-powered team classification based on jersey colors
- **Ball Possession Tracking**: Real-time ball control analysis
- **Pass & Interception Detection**: Automatic detection of passes and interceptions

### Performance Metrics
- **Speed & Distance Calculation**: Player movement analysis with speed and distance metrics
- **Team Ball Control Statistics**: Possession percentage and control time analysis
- **Tactical View Conversion**: Transform player positions to tactical court view

### Visualization
- **Player Tracks**: Visual tracking of player movements with team colors
- **Ball Trajectory**: Ball movement visualization with possession indicators
- **Court Overlay**: Court keypoints and boundaries visualization
- **Statistics Display**: Real-time statistics overlay on video
- **Tactical View**: Bird's-eye tactical view of player positions

## Installation

### Prerequisites
- Python 3.8+
- OpenCV
- NumPy
- Ultralytics YOLO
- Supervision
- scikit-learn
- Pickle

### Setup
1. Clone the repository:
```bash
git clone https://github.com/CyrilleAD/basketball-analysis-system.git
cd basketball-analysis-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download YOLO models:
   - Place your trained models in the `models/` directory:
     - `player_detector.pt` - Player detection model
     - `ball_detector_model.pt` - Ball detection model
     - `court_keypoint_detector.pt` - Court keypoint detection model

4. Create necessary directories:
```bash
mkdir -p models stubs output_videos images
```

## Usage

### Basic Usage
```bash
python main.py path_to_input_video.mp4
```

### Advanced Usage
```bash
python main.py input_video.mp4 --output_video output_videos/analysis_result.avi --stub_path custom_stubs/
```

### Command Line Arguments
- `input_video`: Path to the input basketball video
- `--output_video`: Path for the output analyzed video (default: `output_videos/output_video.avi`)
- `--stub_path`: Directory for caching intermediate results (default: `stubs/`)

## Project Structure

```
basketball-analysis-system/
├── main.py                           # Main analysis script
├── configs/                          # Configuration files
│   ├── __init__.py
│   └── configs.py                    # Default paths and settings
├── trackers/                         # Object tracking modules
│   ├── __init__.py
│   ├── player_tracker.py             # Player detection and tracking
│   └── ball_tracker.py               # Ball detection and tracking
├── team_assigner/                    # Team assignment module
│   ├── __init__.py
│   └── team_assigner.py              # Automatic team classification
├── court_keypoint_detector/          # Court detection module
│   ├── __init__.py
│   └── court_keypoint_detector.py    # Court keypoint detection
├── ball_aquisition/                  # Ball possession module
│   ├── __init__.py
│   └── ball_aquisition_detector.py   # Ball possession tracking
├── pass_and_interception_detector/   # Pass analysis module
│   ├── __init__.py
│   └── pass_and_interception_detector.py # Pass and interception detection
├── speed_and_distance_calculator/    # Performance metrics module
│   ├── __init__.py
│   └── speed_and_distance_calculator.py # Speed and distance calculation
├── tactical_view_converter/          # Tactical analysis module
│   ├── __init__.py
│   ├── tactical_view_converter.py    # Tactical view transformation
│   └── homography.py                 # Homographic transformations
├── drawers/                          # Visualization modules
│   ├── __init__.py
│   ├── player_tracks_drawer.py       # Player visualization
│   ├── ball_tracks_drawer.py         # Ball visualization
│   ├── court_key_points_drawer.py    # Court visualization
│   ├── team_ball_control_drawer.py   # Team control visualization
│   ├── frame_number_drawer.py        # Frame numbering
│   ├── pass_and_interceptions_drawer.py # Pass/interception stats
│   ├── tactical_view_drawer.py       # Tactical view visualization
│   ├── speed_and_distance_drawer.py  # Performance metrics display
│   └── utils.py                      # Drawing utilities
├── utils/                            # Core utilities
│   ├── __init__.py
│   ├── bbox_utils.py                 # Bounding box operations
│   ├── video_utils.py                # Video I/O operations
│   └── stubs_utils.py                # Caching utilities
├── models/                           # YOLO model files (not included)
├── stubs/                            # Cached results directory
├── output_videos/                    # Output directory
├── images/                           # Court images and assets
└── training_notebooks/               # Jupyter notebooks for model training
```

## Key Components

### Tracking System
- **PlayerTracker**: Uses YOLO for player detection and tracking across frames
- **BallTracker**: Specialized tracking for basketball with trajectory analysis
- **CourtKeypointDetector**: Detects court boundaries and key areas

### Analysis Modules
- **TeamAssigner**: Automatically assigns players to teams based on jersey colors
- **BallAquisitionDetector**: Tracks ball possession and control
- **PassAndInterceptionDetector**: Identifies passes between teammates and interceptions
- **SpeedAndDistanceCalculator**: Calculates player movement metrics
- **TacticalViewConverter**: Transforms player positions to tactical court view

### Visualization System
- **Drawer Classes**: Modular visualization components for different aspects
- **Real-time Overlays**: Statistics and tracking information overlaid on video
- **Tactical View**: Bird's-eye view of player positions and movements

## Performance Features

- **Caching System**: Intermediate results are cached to avoid recomputation
- **Modular Design**: Each component can be used independently
- **Configurable Paths**: Easy configuration of model and output paths
- **Batch Processing**: Efficient processing of video frames

## Model Training

The system includes Jupyter notebooks for training custom YOLO models:
- `training_notebooks/basketball_player_detection_training.ipynb`
- `training_notebooks/basketball_ball_training.ipynb`

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available under the MIT License.

## Author

Dday Akrou Cyrille

## Acknowledgments

- YOLO (You Only Look Once) for object detection
- Ultralytics for the YOLO implementation
- OpenCV for computer vision operations
- Supervision for tracking utilities