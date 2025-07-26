def get_center_of_bbox(bbox):
    """
    Calculate the center point of a bounding box.
    
    Args:
        bbox (list): Bounding box coordinates [x1, y1, x2, y2].
    
    Returns:
        tuple: Center coordinates (x_center, y_center).
    """
    x1,y1,x2,y2 = bbox
    return int((x1+x2)/2),int((y1+y2)/2)

def get_bbox_width(bbox):
    """
    Calculate the width of a bounding box.
    
    Args:
        bbox (list): Bounding box coordinates [x1, y1, x2, y2].
    
    Returns:
        int: Width of the bounding box.
    """
    return bbox[2]-bbox[0]

def get_foot_position(bbox):
    """
    Calculate the foot position (bottom center) of a bounding box.
    
    This is typically used for player tracking where the foot position
    is more stable than the center of the bounding box.
    
    Args:
        bbox (list): Bounding box coordinates [x1, y1, x2, y2].
    
    Returns:
        tuple: Foot position coordinates (x_center, y2).
    """
    x1,y1,x2,y2 = bbox
    return int((x1+x2)/2),int(y2)