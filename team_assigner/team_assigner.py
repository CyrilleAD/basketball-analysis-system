from sklearn.cluster import KMeans
import cv2
import pickle
import os

class TeamAssigner:
    def __init__(self):
        """
        Initialize the TeamAssigner.
        
        The team assignment is based on clustering player jersey colors
        using K-means clustering algorithm.
        """
        self.team_colors = {}
        self.player_team_dict = {}
        
    def get_clustering_model(self, image):
        """
        Create and fit a K-means clustering model on the image.
        
        Args:
            image (numpy.ndarray): Input image for color clustering.
        
        Returns:
            KMeans: Fitted K-means clustering model.
        """
        # Reshape the image to 2D array of pixels
        image_2d = image.reshape(-1, 3)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=2, init="k-means++", n_init=1)
        kmeans.fit(image_2d)
        
        return kmeans

    def get_player_color(self, frame, bbox):
        """
        Extract the dominant color from a player's bounding box.
        
        Args:
            frame (numpy.ndarray): Input video frame.
            bbox (list): Player bounding box coordinates [x1, y1, x2, y2].
        
        Returns:
            tuple: RGB color values of the dominant color.
        """
        image = frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]
        
        top_half_image = image[0:int(image.shape[0]/2), :]
        
        # Get clustering model
        kmeans = self.get_clustering_model(top_half_image)
        
        # Get the cluster labels for each pixel
        labels = kmeans.labels_
        
        # Reshape the labels to the image shape
        clustered_image = labels.reshape(top_half_image.shape[0], top_half_image.shape[1])
        
        # Get the player cluster
        corner_clusters = [clustered_image[0,0], clustered_image[0,-1], clustered_image[-1,0], clustered_image[-1,-1]]
        non_player_cluster = max(set(corner_clusters), key=corner_clusters.count)
        player_cluster = 1 - non_player_cluster
        
        player_color = kmeans.cluster_centers_[player_cluster]
        
        return player_color

    def assign_team_color(self, frame, player_detections):
        """
        Assign team colors based on player jersey colors.
        
        Args:
            frame (numpy.ndarray): Input video frame.
            player_detections (dict): Dictionary of player detections.
        """
        player_colors = []
        for track_id, bbox in player_detections.items():
            player_color = self.get_player_color(frame, bbox)
            player_colors.append(player_color)
        
        kmeans = KMeans(n_clusters=2, init="k-means++", n_init=10)
        kmeans.fit(player_colors)
        
        self.kmeans = kmeans
        
        self.team_colors[1] = kmeans.cluster_centers_[0]
        self.team_colors[2] = kmeans.cluster_centers_[1]

    def get_player_team(self, frame, player_bbox, player_id):
        """
        Determine which team a player belongs to.
        
        Args:
            frame (numpy.ndarray): Input video frame.
            player_bbox (list): Player bounding box coordinates.
            player_id (int): Player tracking ID.
        
        Returns:
            int: Team ID (1 or 2).
        """
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id]

        player_color = self.get_player_color(frame, player_bbox)
        
        team_id = self.kmeans.predict(player_color.reshape(1, -1))[0]
        team_id += 1
        
        if player_id is not None:
            self.player_team_dict[player_id] = team_id
        
        return team_id

    def assign_teams(self, frames, player_detections, read_from_stub=False, stub_path=None):
        """
        Assign teams to all players across all frames.
        
        Args:
            frames (list): List of video frames.
            player_detections (list): List of player detections for each frame.
            read_from_stub (bool): Whether to read from cached results.
            stub_path (str): Path to cached team assignments.
        
        Returns:
            list: List of team assignments for each frame.
        """
        if read_from_stub and stub_path is not None and os.path.exists(stub_path):
            with open(stub_path, 'rb') as f:
                team_assignments = pickle.load(f)
            return team_assignments

        team_assignments = []
        
        for frame_num, player_detection in enumerate(player_detections):
            if frame_num == 0:
                self.assign_team_color(frames[frame_num], player_detection)
            
            team_assignment = {}
            for player_id, bbox in player_detection.items():
                team = self.get_player_team(frames[frame_num], bbox, player_id)
                team_assignment[player_id] = team
            
            team_assignments.append(team_assignment)
        
        if stub_path is not None:
            with open(stub_path, 'wb') as f:
                pickle.dump(team_assignments, f)
        
        return team_assignments