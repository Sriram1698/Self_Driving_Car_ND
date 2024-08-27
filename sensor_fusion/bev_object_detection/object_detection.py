import os
import sys
import yaml
from easydict import EasyDict as edict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sensor_utils import utils
from helper import load_object_from_file
from tools.waymo_reader.simple_waymo_open_dataset_reader import WaymoDataFileReader, dataset_pb2, label_pb2
from tools.waymo_reader.simple_waymo_open_dataset_reader import utils as waymo_utils

################################################################

def process_frames(dataset_config, bev_config, obj_det_config):
    datafile = WaymoDataFileReader(dataset_config.base_path + dataset_config.tffile_name)
    dataset_iter = iter(datafile)

    end_frame = dataset_config.start_frame + dataset_config.n_frames
    frame_counter = 0

    while True:
        try:
            # Get the next frame from the dataset
            frame = next(dataset_iter)

            if frame_counter < dataset_config.start_frame:
                frame_counter += 1
            elif frame_counter > end_frame:
                print("Reached end of selected frames")
                break
            print('------------------------------')
            print('Processing frame #{}'.format(frame_counter))
            
            lidar_name  = dataset_pb2.LaserName.TOP
            camera_name = dataset_pb2.CameraName.FRONT

            lidar_pcl   = utils.range_image_to_point_cloud(frame, lidar_name, False)
            cropped_pcl = utils.crop_pcl(lidar_pcl, bev_config, False)

            utils.pcl_to_bev(cropped_pcl, bev_config)
            # lidar_bev = load_object_from_file(obj_det_config.results_path, 
            #                                   dataset_config.tffile_name,
            #                                   bev_config.bev_obj_name,
            #                                   frame_counter)
            # lidar_bev_labels = utils.render_bb_over_bev(lidar_bev, frame.laser_labels, bev_config, True)
            # Increment the frame counter
            frame_counter += 1

        except StopIteration:
            break
        
################################################################

def process_data(config):
    """
    Read the config and process the data for Object detection
    """
    # Read dataset config
    dataset_config              = edict()
    dataset_config.base_path    = config['dataset']['base_path']
    dataset_config.tffile_name  = config['dataset']['tfrecord_file']
    dataset_config.n_frames     = config['dataset']['num_frames']
    dataset_config.start_frame  = config['dataset']['start_frame']

    # Read BEV config
    bev_config                  = edict()
    bev_config.lim_x            = config['bev_config']['lim_x']
    bev_config.lim_y            = config['bev_config']['lim_y']
    bev_config.lim_z            = config['bev_config']['lim_z']
    bev_config.bev_width        = config['bev_config']['bev_width']
    bev_config.bev_height       = config['bev_config']['bev_height']
    bev_config.conf_thresh      = config['bev_config']['conf_thresh']
    bev_config.bev_obj_name     = config['bev_config']['bev_objname']


    # Object detection config
    obj_det_config              = edict()      
    obj_det_config.model        = config['object_detection']['model']
    obj_det_config.results_path = config['object_detection']['result_path']

    # Process all the frames within the given limit and 
    # Convert the 3d point cloud to BEV image
    process_frames(dataset_config, bev_config, obj_det_config)

################################################################

if __name__ == '__main__':
    # Read the config file
    with open('config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    process_data(config)

################################################################