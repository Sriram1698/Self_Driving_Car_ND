import io
import os
import sys
import cv2
import zlib
import math
import numpy as np
import open3d as o3d
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.waymo_reader.simple_waymo_open_dataset_reader import dataset_pb2, label_pb2
from bev_object_detection import obj_det_tools as tools

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

def print_lidar_max_min_range(frame, lidar_name):
    """
    Get the max and min range for the given lidar frame
    """
    # Load the range image
    range_image = load_range_image(frame, lidar_name)
    # Replace all the distance value less than 0 to 0, because the distance
    # can not be negative
    range_image[range_image < 0] = 0.0
    print("Max range: {}m, Min range: {}m".format(round(np.amax(range_image[:, :, 0]), 2), round(np.amin(range_image[:, :, 0]), 2)))

################################################################

def visualize_range_channel(frame, lidar_name):
    """
    Visualize the range channel for the given lidar frame
    """
    # Load the range image 
    range_image = load_range_image(frame, lidar_name)
    # Replace all the distance value less than 0 to 0, because the distance
    # can not be negative
    range_image[range_image < 0] = 0.0
    # Extract the range values from the range image data
    ri_range = range_image[:, :, 0]
    # Scale the range values between 0 and 255 which represents the pixel values
    ri_range = (ri_range / (np.amax(ri_range) - np.amin(ri_range))) * 255
    img_range = ri_range.astype(np.uint8)

    # Focus on +/- deg around image center
    deg = 45
    n_cols = int(img_range.shape[1] / (360 // deg))
    range_image_center = int(img_range.shape[1] / 2)

    img_range = img_range[:, range_image_center - n_cols : range_image_center + n_cols]
    cv2.imshow('Range channel image', img_range)
    cv2.waitKey(0)

################################################################

def visualize_intensity_channel(frame, lidar_name):
    """
    Visualize the intensity channel for the given lidar frame
    """
    # Load the range image 
    range_image = load_range_image(frame, lidar_name)
    # Replace all the distance value less than 0 to 0, because the distance
    # can not be negative
    range_image[range_image < 0] = 0.0
    # Extract the intensity values from the range image data
    ri_intensity = range_image[:, :, 1]
    # Scale the intensity values between 0 and 255 which represents the pixel values
    ri_intensity =(np.amax(ri_intensity)/2) * (ri_intensity / (np.amax(ri_intensity) - np.amin(ri_intensity))) * 255
    img_intensity = ri_intensity.astype(np.uint8)

    # Focus on +/- deg around image center
    deg = 45
    n_cols = int(img_intensity.shape[1] / (360 // deg))
    intensity_image_center = int(img_intensity.shape[1] / 2)

    img_intensity = img_intensity[:, intensity_image_center - n_cols : intensity_image_center + n_cols]
    cv2.imshow('Intensity channel image', img_intensity)
    cv2.waitKey(0)

################################################################

def range_image_to_point_cloud(frame, lidar_name, visualization=True):
    """
    Convert the range image to 3d point cloud
    """
    # Load the range image 
    range_image = load_range_image(frame, lidar_name)
    # Replace all the distance value less than 0 to 0, because the distance
    # can not be negative
    range_image[range_image < 0] = 0.0
    # Extract the range values from the range image data
    ri_range = range_image[:, :, 0]

    # Load the calibration data
    calib_lidar = [obj for obj in frame.context.laser_calibrations if obj.name == lidar_name][0]
    
    # Compute vertical beam inclinations
    height = ri_range.shape[0]
    inclination_min = calib_lidar.beam_inclination_min
    inclination_max = calib_lidar.beam_inclination_max
    inclinations = np.linspace(inclination_min, inclination_max, height)
    # Flip the inclinations so that the first angle comes to the top
    inclinations = np.flip(inclinations)

    # Compute azimuth angle and correct it so that the range image center is aligned to the x-axis
    width = ri_range.shape[1]
    extrinsic = np.array(calib_lidar.extrinsic.transform).reshape(4, 4)
    # atan(y/x)
    azimuth_correction = math.atan2(extrinsic[1, 0], extrinsic[0, 0])
    azimuth = np.linspace(np.pi, -np.pi, width) - azimuth_correction
    
    # Expand inclination and azimuth such that every range image cell has its own appropriate value pair
    inclination_tiled = np.broadcast_to(inclinations[:, np.newaxis], (height, width))
    azimuth_tiled = np.broadcast_to(azimuth[np.newaxis, :], (height, width))

    # Get the 3d coordinates in wrt to lidar frame coordinate
    x = np.cos(azimuth_tiled) * np.cos(inclination_tiled) * ri_range
    y = np.sin(azimuth_tiled) * np.cos(inclination_tiled) * ri_range
    z = np.sin(inclination_tiled) * ri_range

    # Transform the 3D coordinates from lidar coordinate to vehicle coordinate
    xyz_sensor = np.stack([x, y, z, np.ones_like(z)])
    # (4, 4) x (4, 64, 2650) -> (4, 64, 2650)
    xyz_vehicle_coord = np.einsum('ij,jkl->ikl', extrinsic, xyz_sensor)
    # (4, 64, 2650) -> (64, 2650, 4)
    xyz_vehicle_coord = xyz_vehicle_coord.transpose(1, 2, 0)

    # Extract points with range > 0
    idx_range = ri_range > 0
    pcl = xyz_vehicle_coord[idx_range, : 3]

    # Visualize point-cloud
    if visualization:
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(pcl)
        o3d.visualization.draw_geometries([pcd])
    
    # Stack lidar point intensity as last column
    pcl_full = np.column_stack((pcl, range_image[idx_range, 1]))
    return pcl_full

################################################################

def crop_pcl(lidar_pcl, configs, visualization = True):
    """
    Crop the lidar point cloud with the given config
    """
    # Remove points outside of detection cube defined in 'configs.lim_*'
    mask = np.where((lidar_pcl[:, 0] >= configs.lim_x[0]) & (lidar_pcl[:, 0] <= configs.lim_x[1]) &
                    (lidar_pcl[:, 1] >= configs.lim_y[0]) & (lidar_pcl[:, 1] <= configs.lim_y[1]) &
                    (lidar_pcl[:, 2] >= configs.lim_z[0]) & (lidar_pcl[:, 2] <= configs.lim_z[1]))
    lidar_pcl = lidar_pcl[mask]

    # Visualize cropped point cloud # visualize point-cloud
    if visualization:
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(lidar_pcl[:, :3])
        o3d.visualization.draw_geometries([pcd])

    return lidar_pcl

################################################################

def get_min_max_intensity(lidar_pcl):
    """
    Get the minimum and maximum intensity for the given point cloud object
    """
    min_intensity = np.amin(lidar_pcl[:, 3])
    max_intensity = np.amax(lidar_pcl[:, 3])
    return (min_intensity, max_intensity)

################################################################

def render_bb_over_bev(bev_map, labels, configs, vis=False):

    # convert BEV map from tensor to numpy array
    bev_map_cpy = (bev_map.squeeze().permute(1, 2, 0).numpy() * 255).astype(np.uint8)
    bev_map_cpy = cv2.resize(bev_map_cpy, (configs.bev_width, configs.bev_height))

    # convert bounding box format format and project into bev
    label_objects = tools.convert_labels_into_objects(labels, configs)
    tools.project_detections_into_bev(bev_map_cpy, label_objects, configs, [0,255,0])
    
    # display bev map
    if vis==True:
        bev_map_cpy = cv2.rotate(bev_map_cpy, cv2.ROTATE_180)   
        cv2.imshow("BEV map", bev_map_cpy)
        cv2.waitKey(0)          

    return bev_map_cpy 

################################################################

def render_obj_over_bev(detections, lidar_bev_labels, configs, vis=False):
    """
    Render the object over BEV image
    """
    # project detected objects into bird's eye view
    tools.project_detections_into_bev(lidar_bev_labels, detections, configs, [0,0,255])

    # display bev map
    if vis==True:
        lidar_bev_labels = cv2.rotate(lidar_bev_labels, cv2.ROTATE_180)   
        cv2.imshow("BEV map", lidar_bev_labels)
        cv2.waitKey(0)

################################################################