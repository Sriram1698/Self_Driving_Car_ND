# Object Detection in an Urban Environment

## Project Objective:
The objective of this project is to train a model to detect multiple objects in urban driving scenrio.


## Local setup

### Requirements
*   NVIDIA GPU with the latest driver installed
*   docker/ nvidia-docker

For local setup, we can follow the below steps
1.  **Build the docker container:**
    -   Build the image with:
        ```bash
        docker build -t project-dev -f Dockerfile .
        ```
    -   Create the container with:
        ```
        docker run --gpus all -v <PATH TO LOCAL PROJECT FOLDER>:/app/project/ --network=host -ti project-dev bash
        ```
2.  **Set up:**
    -   Once in container, we will need to auth using:
        ```bash
        gcloud auth login
        ```

## Download and process data

For this project, we will be using data from the [Waymo Open dataset](https://waymo.com/open/).

Download the data from the Waymo's Google cloud bucket to the local machine. For this project, we only need a subset of the data provided (for example, we do not need to use the Lidar data). Therefore, we are going to download and trim each file. In `download_process.py`, we can view the `create_tf_example` function, which will perform this processing. This function takes the components of a Waymo Tf record and saves them in the Tf Object Detection api format. 

Run the following script using the following command
```bash
python download_process.py --data_dir {processed_file_location} --size {number of files you want to download}
```

By default 100 files will be downloaded.

## Structure

### Data

The downloaded data will be used for training, validation and testing. So for that 3 folders will be created those are:
*   **train**: contain the train data
*   **val**: contain the validation data
*   **test**: contain the test data

We have to run `create_splits.py` script to the split we require. This can be achieved by running the following command
```bash
python create_splits.py --source {source directory which contains all the downloaded files} --destination {destination folder}
```

The split that we have used here is 70/15/15, where 70 for training, 15 for validation and 15 for testing.

## Instructions

### Exploratory Data Analysis
Use the data present in `data/processed` folder to explore the dataset. This task is most important task to get the sense of how the data distributed in multiple aspects. The detailed view of these aspects are discussed with the corresponding plots in `Exploratory Data Analysis.ipynb` file.

### Edit the config file

Now before the model training, one more file needs attention, the `pipeline.config`. The Tf Object Detection API relies on this config file. The config that we are using is for SSD Resnet 50 640x640 model.

First, we need to download the [pretrained model](http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_resnet50_v1_fpn_640x640_coco17_tpu-8.tar.gz) and move it to `experiments/pretrained_model/`.

We need to edit the config files to change the location of the training and validation files, as well as the location of the label_map file, pretrained weights. We also need to adjust the batch size. To do so, run the following:

```bash
python edit_config.py --train_dir data/train/ --eval_dir data/val/ --batch_size 2 --checkpoint experiments/pretrained_model/ssd_resnet50_v1_fpn_640x640_coco17_tpu-8/checkpoint/ckpt-0 --label_map experiments/label_map.pbtxt
```

A new config file has been created, `pipeline_new.config`. We then need to tweak certain parameters here to optimize the model performance.

### Training

Now launch the experiement with the Tensorflow object detection API. Move the `pipeline_new.config` to the `experiements/reference` folder. Now launch the training process:

*   training process:
    ```bash
    python experiments/model_main_tf2.py --model_dir=experiments/reference/ --pipeline_config_path=experiments/reference/pipeline_new.config
    ```

Once the training is finished, launch the evaluation process:

*   evaluation process:
    ```bash
    python experiments/model_main_tf2.py --model_dir=experiments/reference/ --pipeline_config_path=experiments/reference/pipeline_new.config --checkpoint_dir=experiments/reference/
    ```

To monitor the training, launch a tensorboard instance by running
```bash
python -m tensorboard.main --logdir experiments/reference/
```