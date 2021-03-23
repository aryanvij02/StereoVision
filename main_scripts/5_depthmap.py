import cv2
import numpy as np
import json
from stereovision.calibration import StereoCalibration
from start_cameras import Start_Cameras


# Depth map default preset
SWS = 5
PFS = 5
PFC = 29
MDS = -30
NOD = 160
TTH = 100
UR = 10
SR = 14
SPWS = 100


def load_map_settings(file):
    global SWS, PFS, PFC, MDS, NOD, TTH, UR, SR, SPWS, loading_settings, sbm
    print('Loading parameters from file...')
    f = open(file, 'r')
    data = json.load(f)
    #loading data from the json file and assigning it to the Variables
    SWS = data['SADWindowSize']
    PFS = data['preFilterSize']
    PFC = data['preFilterCap']
    MDS = data['minDisparity']
    NOD = data['numberOfDisparities']
    TTH = data['textureThreshold']
    UR = data['uniquenessRatio']
    SR = data['speckleRange']
    SPWS = data['speckleWindowSize']
    
    #changing the actual values of the variables
    sbm = cv2.StereoBM_create(numDisparities=16, blockSize=SWS) 
    sbm.setPreFilterType(1)
    sbm.setPreFilterSize(PFS)
    sbm.setPreFilterCap(PFC)
    sbm.setMinDisparity(MDS)
    sbm.setNumDisparities(NOD)
    sbm.setTextureThreshold(TTH)
    sbm.setUniquenessRatio(UR)
    sbm.setSpeckleRange(SR)
    sbm.setSpeckleWindowSize(SPWS)
    f.close()
    print('Parameters loaded from file ' + file)

def stereo_depth_map(rectified_pair):
    #blockSize is the SAD Window Size

    dmLeft = rectified_pair[0]
    dmRight = rectified_pair[1]
    disparity = sbm.compute(dmLeft, dmRight)
    disparity_normalized = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX)
    image = np.array(disparity_normalized, dtype = np.uint8)
    disparity_color = cv2.applyColorMap(image, cv2.COLORMAP_JET)
    return disparity_color, disparity_normalized

def onMouse(event, x, y, flag, disparity_normalized):
    if event == cv2.EVENT_LBUTTONDOWN:
        distance = disparity_normalized[y][x]
        print("Distance in centimeters {}".format(distance))
        return distance


if __name__ == "__main__":
    left_camera = Start_Cameras(0).start()
    right_camera = Start_Cameras(1).start()
    load_map_settings("../3dmap_set.txt")

    cv2.namedWindow("DepthMap")

    while True:
        left_grabbed, left_frame = left_camera.read()
        right_grabbed, right_frame = right_camera.read()

        if left_grabbed and right_grabbed:  
            #Convert BGR to Grayscale     
            left_gray_frame = cv2.cvtColor(left_frame, cv2.COLOR_BGR2GRAY)
            right_gray_frame = cv2.cvtColor(right_frame, cv2.COLOR_BGR2GRAY)

            #calling all calibration results
            calibration = StereoCalibration(input_folder='../calib_result')
            rectified_pair = calibration.rectify((left_gray_frame, right_gray_frame))
            disparity_color, disparity_normalized = stereo_depth_map(rectified_pair)

            #Mouse clicked function
            cv2.setMouseCallback("DepthMap", onMouse, disparity_normalized)

            #Show depth map and image frames
            output = cv2.addWeighted(left_frame, 0.5, disparity_color, 0.5, 0.0)
            cv2.imshow("DepthMap", np.hstack((disparity_color, output)))
            
            cv2.imshow("Frames", np.hstack((left_frame, right_frame)))

            k = cv2.waitKey(1) & 0xFF
            if k == ord('q'):
                break

            else:
                continue

    left_camera.stop()
    left_camera.release()
    right_camera.stop()
    right_camera.release()
    cv2.destroyAllWindows()
                


    


