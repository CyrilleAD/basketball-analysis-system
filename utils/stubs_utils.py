import pickle
import os

def save_stub(stub_path,object):
    """
    Save a Python object to disk at the specified path.
    
    This function serializes a Python object using pickle and saves it to the
    specified file path. If the directory doesn't exist, it creates it.
    
    Args:
        stub_path (str): File path where the object should be saved.
        object: The Python object to be saved.
    """
    if not os.path.exists(os.path.dirname(stub_path)):
        os.makedirs(os.path.dirname(stub_path))
    
    if stub_path is not None:
        with open(stub_path,'wb') as f:
            pickle.dump(object,f)

def read_stub(read_from_stub,stub_path):
    """
    Read a Python object from disk if conditions are met.
    
    Args:
        read_from_stub (bool): Whether to attempt reading from stub.
        stub_path (str): File path where the object was saved.
    
    Returns:
        object or None: The deserialized object if successful, None otherwise.
    """
    object = None
    if read_from_stub and stub_path is not None and os.path.exists(stub_path):
        with open(stub_path,'rb') as f:
            object = pickle.load(f)
    return object