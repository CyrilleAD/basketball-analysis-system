import cv2
import numpy as np
import sys
sys.path.append('../')

def draw_ellipse(frame, bbox, color, track_id=None):
    """
    Draw an ellipse around a bounding box.
    
    Args:
        frame (numpy.ndarray): Input video frame.
        bbox (list): Bounding box coordinates [x1, y1, x2, y2].
        color (tuple): RGB color for the ellipse.
        track_id (int, optional): Track ID to display.
    
    Returns:
        numpy.ndarray: Frame with drawn ellipse.
    """
    y2 = int(bbox[3])
    x_center, _ = get_center_of_bbox(bbox)
    width = get_bbox_width(bbox)
    
    cv2.ellipse(
        frame,
        center=(x_center, y2),
        axes=(int(width), int(0.35 * width)),
        angle=0.0,
        startAngle=-45,
        endAngle=235,
        color=color,
        thickness=2,
        lineType=cv2.LINE_4
    )
    
    rectangle_width = 40
    rectangle_height = 20
    x1_rect = x_center - rectangle_width // 2
    x2_rect = x_center + rectangle_width // 2
    y1_rect = (y2 - rectangle_height // 2) + 15
    y2_rect = (y2 + rectangle_height // 2) + 15
    
    if track_id is not None:
        cv2.rectangle(frame,
                      (int(x1_rect), int(y1_rect)),
                      (int(x2_rect), int(y2_rect)),
                      color,
                      cv2.FILLED)
        
        x1_text = x1_rect + 12
        if track_id > 99:
            x1_text -= 10
        
        cv2.putText(
            frame,
            f"{track_id}",
            (int(x1_text), int(y1_rect + 15)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 0),
            2
        )
    
    return frame

def draw_triangle(frame, bbox, color):
    """
    Draw a triangle above a bounding box.
    
    Args:
        frame (numpy.ndarray): Input video frame.
        bbox (list): Bounding box coordinates [x1, y1, x2, y2].
        color (tuple): RGB color for the triangle.
    
    Returns:
        numpy.ndarray: Frame with drawn triangle.
    """
    y = int(bbox[1])
    x, _ = get_center_of_bbox(bbox)
    
    triangle_points = np.array([
        [x, y],
        [x - 10, y - 20],
        [x + 10, y - 20],
    ])
    cv2.drawContours(frame, [triangle_points], 0, color, cv2.FILLED)
    cv2.drawContours(frame, [triangle_points], 0, (0, 0, 0), 2)
    
    return frame

def get_center_of_bbox(bbox):
    """
    Calculate the center point of a bounding box.
    
    Args:
        bbox (list): Bounding box coordinates [x1, y1, x2, y2].
    
    Returns:
        tuple: Center coordinates (x_center, y_center).
    """
    x1, y1, x2, y2 = bbox
    return int((x1 + x2) / 2), int((y1 + y2) / 2)

def get_bbox_width(bbox):
    """
    Calculate the width of a bounding box.
    
    Args:
        bbox (list): Bounding box coordinates [x1, y1, x2, y2].
    
    Returns:
        int: Width of the bounding box.
    """
    return bbox[2] - bbox[0]

def draw_text_with_background(frame, text, position, font_scale=0.7, thickness=2, 
                             text_color=(255, 255, 255), bg_color=(0, 0, 0), padding=5):
    """
    Draw text with a background rectangle.
    
    Args:
        frame (numpy.ndarray): Input video frame.
        text (str): Text to draw.
        position (tuple): Position (x, y) for the text.
        font_scale (float): Font scale factor.
        thickness (int): Text thickness.
        text_color (tuple): RGB color for the text.
        bg_color (tuple): RGB color for the background.
        padding (int): Padding around the text.
    
    Returns:
        numpy.ndarray: Frame with drawn text.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Get text size
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    
    # Calculate background rectangle coordinates
    x, y = position
    bg_x1 = x - padding
    bg_y1 = y - text_height - padding
    bg_x2 = x + text_width + padding
    bg_y2 = y + baseline + padding
    
    # Draw background rectangle
    cv2.rectangle(frame, (bg_x1, bg_y1), (bg_x2, bg_y2), bg_color, cv2.FILLED)
    
    # Draw text
    cv2.putText(frame, text, position, font, font_scale, text_color, thickness)
    
    return frame