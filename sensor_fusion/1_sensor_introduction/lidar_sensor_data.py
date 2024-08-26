import os
import sys
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.waymo_reader.simple_waymo_open_dataset_reader import WaymoDataFileReader, dataset_pb2, label_pb2
from tools.waymo_reader.simple_waymo_open_dataset_reader import utils as waymo_utils
import utils

def process_frames(data_file, start_frame, n_frames):
    datafile = WaymoDataFileReader(data_file)
    dataset_iter = iter(datafile)

    end_frame = start_frame + n_frames
    frame_counter = 0
    while True:
        try:
            # Get the next frame from the dataset
            frame = next(dataset_iter)

            if frame_counter < start_frame:
                frame_counter += 1
            elif frame_counter > end_frame:
                print("Reached end of selected frames")
                break
            print('------------------------------')
            print('Processing frame #{}'.format(frame_counter))
            frame_counter += 1
            
            lidar_name = dataset_pb2.LaserName.TOP
            camera_name = dataset_pb2.CameraName.FRONT

            # Uncomment to see the number of vehicles in the given frame
            # utils.print_no_of_vehicles(frame)

            # Uncomment to display the camera images associated with the given frame
            utils.display_image(frame, camera_name)

            
        except StopIteration:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Visualize the Lidar frames from .tfrecord data')
    parser.add_argument('--tfrecord_file', required=True, type=str, help='.tfrecord file path')
    parser.add_argument('--start_frame', required=False, default=0, type=int, help='Starting frame index')
    parser.add_argument('--frames', required=False, default=10, type=int, help='Number of frames to display')
    args = parser.parse_args()
    
    process_frames(args.tfrecord_file, args.start_frame, args.frames)
