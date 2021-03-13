# Stereo Vision Camera - Depth Map with Jetson Nano

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

## Depth map Tuning Variables


| Variables  | Description |
| ------------- |:-------------:|
| SAD Windows Size (SWS) | ||
| Speckle Size      | number of pixels below which a disparity blob is dismissed as "speckle."      |
| Speckle Range  | right bar     |
|   Number of disparities   |   How many pixels to slide the window over. The larger it is, the larger the range <br /> of visible depths, but more computation is required.   |
|   Min Disparity   |   the offset from the x-position of the left pixel at which to begin searching.   |
|   Uniqueness Ratio   |   Another post-filtering step. If the best matching disparity is not sufficiently better than every other<br /> disparity in the search range, the pixel is filtered out.  You can try tweaking this<br /> if texture_threshold and the speckle filtering are still letting through spurious matches.   |
|  Pre Filter Cap <br /> Pre Filter Size    |  prefilter_size and prefilter_cap: The pre-filtering phase, which normalizes image<br /> brightness and enhances texture in preparation for block matching.<br /> Normally you should not need to adjust these.    |
|   Texture Threshold   |   filters out areas that don't have enough texture for reliable matching   |

Sources: 
* https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html#stereosgbm-stereosgbm
* https://docs.opencv.org/master/dd/d53/tutorial_py_depthmap.html

## File Structure
All the main scripts are in **main_scripts** directory