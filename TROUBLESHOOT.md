# Solutions to possible errors.

## Issues with starting the Cameras
### Gstreamer error
![Gstreamer error](https://user-images.githubusercontent.com/75800604/112165043-599de580-8c29-11eb-9d85-e134ae8941d9.png)
**Error**: The Gstreamer pipeline will fail to open

**Solution**: `sudo service nvargus-daemon restart`

**Description**: This command helps to clean-up the Gstreamer pipeline. You may face this error if a program accidentally crashes or you closed it by pressing Ctrl^C in the Terminal.

### canberra-gtk-module error
**Error 2**: Failed to load module "canberra-gtk-module"…

**Solution 2**: `sudo apt-get install libcanberra-gtk-modulet`

### Unable to capture frames from camera
![cameraerror](https://user-images.githubusercontent.com/75800604/112163609-29097c00-8c28-11eb-8382-1ac6eaaff847.png)
**Error** The issue here may be with your OpenCV not being installed with GStreamer support. 

**Solution**: <br />
`python3` #This will open python <br />
`>>> import cv2` #This is to import OpenCV <br />
`>>> print (cv2.getBuildInformation())` #This will give us a bunch of details about the OpenCV build

Scroll through the terminal output and check under the Video I/O section.

![Buildinfo](https://user-images.githubusercontent.com/75800604/112164545-ebf1b980-8c28-11eb-83ca-af0b05de33e9.png)

If it shows something similar to the image above, with GStreamer: NO, then we know the problem is with the OpenCV installation. <br />
This issue occurs only if you have separately installed OpenCV on your Jetson using `pip3 install opencv-python` . To fix this, we must uninstall your separate OpenCV installation.

To uninstall current version: `sudo apt-get purge python3-opencv`

Then check again using the same methods above to get the Build Information.

Gstreamer should show YES now and the script should run and start your cameras!
