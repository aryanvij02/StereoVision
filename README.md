# Stereo Vision Camera: Depth Map and Distance measurement with Jetson Nano

Welcome to the tutorial on how to create a Depth Map, do Object Detection, and determine the distance to objects using a Stereo Vision camera!

--Pictures etc

Check out the step-by-step tutorial here:

## File Structure

All the scipts that we will run are in the **main_scripts** directory

In **main_scripts**:

### start_cameras.py
Starts the Raspberry Pi cameras on the Jetson Nano using a Gstreamer pipeline. <br /> To change camera capture or display resolution, use this script. 

### 1_taking_pictures.py
A continuous program to take 30 pictures at 5 second intervals for calibration. This is where pictures of the Chessboard will be taken.<br /> You can change the interval between pictures and also the total number of pictures you want to take. 

### 2_image_selection.py
Used to filter between good and poor quality images. Reject those with poor quality (blurry, chessboard cut out, etc.) to avoid having poor calibration results.  <br />
Press Y to accept and N to reject <br />
Accepted images will be split into left and right pairs and be saved into the 'pairs' folder.

### 3_calibration
This is where the magic happens. <br />
You will go through the point-matching process and see such images for each pair: <br />
PICTURE <br />
Ensure that the quality of the corner detection is good. If not, retake your pictures.

### 4_tuning_depthmap
Tuning the depth map. Descriptions for all the variables are here:

| Variables  | Description | Range |
| ------------- |:-------------:| ------------- |
| SAD Windows Size (SWS) | --- | 5 - 255 & Odd |
| Speckle Size      | Number of pixels below which a disparity blob is dismissed as "speckle."  | 0 - 300 |
| Speckle Range  | Controls how close in value disparities must be to be considered part of the same blob.    | 0 - 40 |
|   Uniqueness Ratio   |   Another post-filtering step. If the best matching disparity is not sufficiently better than every other<br /> disparity in the search range, the pixel is filtered out.  You can try tweaking this<br /> if texture_threshold and the speckle filtering are still letting through spurious matches.  | 1 - 20 |
|   Texture Threshold   |   filters out areas that don't have enough texture for reliable matching   | >0 (Positive) |
|   Number of disparities   |   How many pixels to slide the window over. The larger it is, the larger the range <br /> of visible depths, but more computation is required.   | 0-256 & Divisible by 16 |
|   Min Disparity   |   the offset from the x-position of the left pixel at which to begin searching.   | -100 - 100 | 
|  Pre Filter Cap  | The pre-filtering phase, which normalizes image brightness and enhances texture <br /> in preparation for block matching.<br /> Normally you should not need to adjust these.    | 1 - 63 |
| Pre Filter Size | ---- | 5 - 255 & Odd |

### 5_depthmap.py
After Calibration and Tuning, we finally have our depth map! 

### 6_depthwdistance
Like to take things to the next level? That is what this is. Combining Computer Vision with Machine Learning, this enables us to detect eople in the frame and tell their distance away from the camera. <br />
The range of the camera is limited depending on the seperation between the lenses, but your results should be relatively accurate between 20cm - 150cm!

## Sources
**Raspberry Pi**

Tutorial: https://stereopi.com/blog/opencv-and-depth-map-stereopi-tutorial

GitHub: https://github.com/realizator/stereopi-tutorial

**Jetson Hacks** - Used to start cameras

Tutorial Video: https://www.youtube.com/watch?v=GQ3drRllX3I

GitHub: https://github.com/JetsonHacksNano/CSI-Camera


## StereoVision Library
GitHub: https://github.com/erget/StereoVision

PyPi: https://pypi.org/project/StereoVision/




Sources: 
* https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html#stereosgbm-stereosgbm
* https://docs.opencv.org/master/dd/d53/tutorial_py_depthmap.html

### 5_depthmap

This is the final script to run! Now we have our depth map!
