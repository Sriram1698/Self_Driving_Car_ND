import io
import cv2
import zlib
import numpy as np
from PIL import Image

from tools.waymo_reader.simple_waymo_open_dataset_reader import dataset_pb2, label_pb2

################################################################

def get_lidar_transformation_matrix(frame, lidar_name):
    """
    Get the transformation matrix for the given lidar with respect to the
    ego vehicle's origin
    """
    calib_lidar = [obj for obj in frame.context.laser_calibrations if obj.name == lidar_name][0]
    return np.array(calib_lidar.extrinsic.transform)

################################################################

def get_camera_transformation_matrix(frame, camera_name):
    """
    Get the transformation matrix for the given camera with respect to the
    ego vehicle's origin
    """
    calib_camera = [obj for obj in frame.context.camera_calibrations if obj.name == camera_name][0]
    return np.array(calib_camera.extrinsic.transform)

################################################################

def print_no_of_vehicles(frame):
    """
    Print the number of vehicles labeled in the current frame
    """
    num_vehicles = 0
    for label in frame.laser_labels:
        if label.type == label.TYPE_VEHICLE:
            num_vehicles = num_vehicles + 1
    print("Number of labeled vehicles in current frame: {}".format(num_vehicles))

################################################################

def display_image(frame, camera_name):
    """
    Display the image in the given frame that corresponding to the given camera
    """
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

################################################################

def load_range_image(frame, lidar_name):
    lidar = [obj for obj in frame.lasers if obj.name == lidar_name][0]
    range_image = []
    # Use only the first return from objects
    if len(lidar.ri_return1.range_image_compressed) > 0:
        range_image = dataset_pb2.MatrixFloat()
        range_image.ParseFromString(zlib.decompress(lidar.ri_return1.range_image_compressed))
        range_image = np.array(range_image.data).reshape(range_image.shape.dims)
    return range_image

################################################################

def get_v_fov_for_lidar(frame, lidar_name):
    """
    Get the vertical FOV for the given lidar
    """
    calib_lidar = [obj for obj in frame.context.laser_calibrations if obj.name == lidar_name][0]
    return (calib_lidar.beam_inclination_max - calib_lidar.beam_inclination_min)

################################################################

def print_range_image_shape(frame, lidar_name):
    """
    Print the dimension of the range image
    """
    range_image = load_range_image(frame, lidar_name)
    print(range_image.shape)

################################################################

def visualize_range_image(frame, lidar_name):
    """
    Visualize the range image
    """
    # Obtain the range image from the frame object for the respective lidar
    range_image = load_range_image(frame, lidar_name)
    # Extract range data and convert to 8 bit
    ri_range = range_image[:, :, 0]
    ri_range = ri_range * 256 / (np.amax(ri_range))
    img_range = ri_range.astype(np.uint8)

    # Visualize the range image
    cv2.imshow('Range image', img_range)
    cv2.waitKey(0)

################################################################

def print_pitch_resolution(frame, lidar_name):
    """
    Print the pitch angle resolution in degrees
    """
    # Load the range image
    range_image = load_range_image(frame, lidar_name)
    # Compute the vertical FOV from lidar calibration
    v_fov = get_v_fov_for_lidar(frame, lidar_name)
    # Divide the vertical FOV with the number of rows in range_image data
    pitch_resolution = v_fov / range_image.shape[0]
    print("Pitch angle resolution: {0:.2f}°".format(pitch_resolution * 180 / np.pi))

################################################################ 