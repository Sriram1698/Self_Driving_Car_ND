import io
import cv2
import numpy as np
from PIL import Image
from tools.waymo_reader.simple_waymo_open_dataset_reader import dataset_pb2, label_pb2

def get_lidar_transformation_matrix(frame, lidar_name):
    """
    Get the transformation matrix for the given lidar with respect to the
    ego vehicle origin
    """
    calib_lidar = [obj for obj in frame.context.laser_calibrations if obj.name == lidar_name][0]
    return np.array(calib_lidar.extrinsic.transform)

def get_camera_transformation_matrix(frame, camera_name):
    """
    Get the transformation matrix for the given camera with respect to the
    ego vehicle origin
    """
    calib_camera = [obj for obj in frame.context.camera_calibrations if obj.name == camera_name][0]
    return np.array(calib_camera.extrinsic.transform)

def print_no_of_vehicles(frame):
    num_vehicles = 0
    for label in frame.laser_labels:
        if label.type == label.TYPE_VEHICLE:
            num_vehicles = num_vehicles + 1
    print("Number of labeled vehicles in current frame: {}".format(num_vehicles))


def display_image(frame, camera_name):

    # Load the camera
    image = [obj for obj in frame.images if obj.name == camera_name][0]

    # Convert the actual image into rgb format
    img = np.array(Image.open(io.BytesIO(image.image)))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Resize the image to better fit the screen
    dim = (int(img.shape[1] * 0.5), int(img.shape[0] * 0.5))
    resized = cv2.resize(img, dim)

    # Display the image
    cv2.imshow("Camer_image", resized)
    cv2.waitKey(0)