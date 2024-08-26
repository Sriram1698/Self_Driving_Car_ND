import os
import sys
import pickle

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

################################################################

def load_object_from_file(file_path, base_file_name, object_name, frame_id=1):
    """
    Loads an object from a binary pickle file
    """
    obj_file = os.path.join(file_path, "training_" + os.path.splitext(base_file_name)[0] + "__frame-" + str(frame_id) + "__" + object_name + ".pkl")
    with open(obj_file, 'rb') as f:
        object = pickle.load(f)
        return object

################################################################