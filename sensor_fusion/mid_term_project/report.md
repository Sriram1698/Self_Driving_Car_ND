# Sensor Fusion
## Object Detection in BEV image
![Range Image](imgs/range_image.gif)
<p align="left">Range image sequence. Range channel (top), Intensity channel (bottom)

<br>
<br>

![Detections](imgs/detections.gif)
<p align="left"> Object detection on BEV image (bottom)
<br>

-------------------------------------------------------------------------------------

## Visualizing the **`pcd`** (point-cloud)
After visualizing the point-cloud on open3d module, following are the few findings.

### Visibility:

* #### Front-View
    <em><b>Fig.1</b></em> illustrates that the vehicles ahead of the ego vehicle are clearly discernible."
<p align="left" style="margin-top: 0px; margin-bottom: 0px;">
  <img src="imgs/pcl_2.png" alt="Image 1" width="600" height="300"/>
  <br>
  <em><b>Fig.1:</b> Front-view of ego vehicle</em>
</p>

* #### Rear-View
<em><b>Fig.2</b></em> reveals that the vehicles trailing the ego vehicle are distinctly visible.
<p align="left" style="margin-top: 0px; margin-bottom: 0px;">
  <img src="imgs/pcl_11.png" alt="Image 2" width="900" height="300"/>
  <br>
  <em><b>Fig.2:</b> Rear-view of ego vehicle</em>
</p>

* #### Corner cases
    - #### Blind spots
    <em><b>Fig.3</b></em> illustrates that certain areas in close proximity to the ego vehicle are not detected by the LiDAR. This occurs because parts of the ego vehicle, such as the body or roof, obstruct the LiDAR beams, creating shadowed regions where detection is impaired. These blind spots are particularly concerning as they increase the risk of potential collisions.
    <p align="left" style="margin-top: 0px; margin-bottom: 0px; margin-right: 10px;">
     <img src="imgs/pcl_1.png" alt="Image 3" width="500" height="300"/>
     <img src="imgs/pcl_5.png" alt="Image 4" width="500" height="300"/>
     <br>
     <img src="imgs/pcl_9.png" alt="Image 5" width="500" height="300"/>
     <img src="imgs/pcl_8.png" alt="Image 6" width="500" height="300"/>
     <br>
     <em><b>Fig.3:</b> Blind spots</em>
    </p>    

    - #### Omission of Attached Trailer
    <em><b>Fig.4</b></em> shows us that the detection module failed to detect the car trailer
    <p align="left" style="margin-top: 0px; margin-bottom: 0px; margin-right: 10px;">
     <img src="imgs/pcl_6.png" alt="Image 7" width="1200" height="500"/>
     <br>
     <em><b>Fig.4:</b> LiDAR misses car trailer detection</em>
    </p>

<br>

### Stable Features of vehicle:
From <em><b>Fig.5</b></em> Here are some of the stable features observable in the vehicle's point cloud
* Side mirrors
* Front and Rear Bumper
* Wheels
* Head lights and Tail-lights
* Roofline/Roof Ridges
    <p align="left" style="margin-top: 0px; margin-bottom: 0px; margin-right: 10px;">
     <br>
     <img src="imgs/pcl_3.png" alt="Image 8" width="500" height="300"/>
     <img src="imgs/pcl_10.png" alt="Image 9" width="700" height="300"/>
     <br>
     <em><b>Fig.5:</b> Stable features of vehicle </em>
    </p>

<br>

# Precision Recall Plot
![Alt text](imgs/plot.png)