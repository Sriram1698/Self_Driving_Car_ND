import argparse
import glob
import shutil
import os
import random

import numpy as np

from utils import get_module_logger


def split(source, destination):
    """
    Create three splits from the processed records. The files should be moved to new folders in the
    same directory. This folder should be named train, val and test.

    args:
        - source [str]: source data directory, contains the processed tf records
        - destination [str]: destination data directory, contains 3 sub folders: train / val / test
    """
    # TODO: Implement function
    train_path = destination + 'train/'
    val_path = destination + 'val/'
    test_path = destination + 'test/'

    # Create these directories if they don't exist before
    os.makedirs(train_path, exist_ok=True)
    os.makedirs(val_path, exist_ok=True)
    os.makedirs(test_path, exist_ok=True)

    tf_records = [f for f in os.listdir(source) if f.endswith('.tfrecord')]
    np.random.shuffle(tf_records)
    n_files = len(tf_records)
    train_split = 0.7
    val_split   = 0.15
    test_split  = 1.0 - train_split - val_split

    n_train_samples = int(n_files * train_split)
    n_val_samples   = int(n_files * val_split)
    n_test_samples  = int(n_files * test_split)
    train_data  = tf_records[:n_train_samples]
    val_data    = tf_records[n_train_samples : n_train_samples + n_val_samples]
    test_data   = tf_records[n_train_samples + n_val_samples : ]

    train_tuple = (train_path, train_data)
    val_tuple   = (val_path, val_data)
    test_tuple  = (test_path, test_data)

    data_tuple = [train_tuple, val_tuple, test_tuple]

    for _, (path, files) in enumerate(data_tuple):
        for file in files:
            src = os.path.join(source, file)
            dst = os.path.join(path, file)
            shutil.move(src, dst)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split data into training / validation / testing')
    parser.add_argument('--source', required=True,
                        help='source data directory')
    parser.add_argument('--destination', required=True,
                        help='destination data directory')
    args = parser.parse_args()

    logger = get_module_logger(__name__)
    logger.info('Creating splits...')
    split(args.source, args.destination)