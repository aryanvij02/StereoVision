#Used to tune the depth map. Takes real time video from the cameras and let's you tune

import cv2
import os
import threading
import numpy as np
import time
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button
import json
from stereovision.calibration import StereoCalibrator
from stereovision.calibration import StereoCalibration
from start_cameras import Start_Cameras

# Depth map function
SWS = 215
PFS = 115
PFC = 43
MDS = -25
NOD = 112
TTH = 100
UR = 10
SR = 15
SPWS = 100

loading = False


def stereo_depth_map(rectified_pair, variable_mapping):
    '''print ('SWS='+str(SWS)+' PFS='+str(PFS)+' PFC='+str(PFC)+' MDS='+\
           str(MDS)+' NOD='+str(NOD)+' TTH='+str(TTH))
    print (' UR='+str(UR)+' SR='+str(SR)+' SPWS='+str(SPWS))'''

    #blockSize is the SAD Window Size
    sbm = cv2.StereoBM_create(numDisparities=16, blockSize=variable_mapping["SWS"]) 
    # sbm.state SADWindowSize = SWS
    sbm.setPreFilterType(1)    
    sbm.setPreFilterSize(variable_mapping['PreFiltSize'])
    sbm.setPreFilterCap(variable_mapping['PreFiltCap'])
    sbm.setSpeckleRange(variable_mapping['SpeckleRange'])
    sbm.setSpeckleWindowSize(variable_mapping['SpeckleSize'])
    sbm.setMinDisparity(variable_mapping['MinDisp'])
    sbm.setNumDisparities(variable_mapping['NumofDisp'])
    sbm.setTextureThreshold(variable_mapping['TxtrThrshld'])
    sbm.setUniquenessRatio(variable_mapping['UniqRatio'])
    

    c, r = rectified_pair[0].shape
    #disparity = np.zeros((c, r), np.uint8)
    dmLeft = rectified_pair[0]
    dmRight = rectified_pair[1]
    #cv2.FindStereoCorrespondenceBM(dmLeft, dmRight, disparity, sbm)
    disparity = sbm.compute(dmLeft, dmRight)

    #disparity_visual = cv.CreateMat(c, r, cv.CV_8U)
    local_max = disparity.max()
    local_min = disparity.min()
    '''print ("MAX " + str(local_max))
    print ("MIN " + str(local_min))'''
    disparity_visual = (disparity-local_min)*(1.0/(local_max-local_min))
    
    local_max = disparity_visual.max()
    local_min = disparity_visual.min()
    '''print ("MAX " + str(local_max))
    print ("MIN " + str(local_min))'''
    cv2.normalize(disparity, disparity_visual, 0, 255, cv2.NORM_MINMAX)
    #disparity_visual = np.array(disparity_visual)
    return disparity_visual

def save_load_map_settings(current_save, current_load, variable_mapping):
    global loading
    if current_save != 0:
        print('Saving to file...')
        print(variable_mapping['MinDisp'])
        # result = json.dumps({'SADWindowSize':cv2.getTrackbarPos("SWS", "Stereo"), 'preFilterSize':cv2.getTrackbarPos("PreFiltSize", "Stereo"), 'preFilterCap':cv2.getTrackbarPos("PreFiltCap", "Stereo"), 
        #         'minDisparity':cv2.getTrackbarPos("MinDisp", "Stereo"), 'numberOfDisparities': cv2.getTrackbarPos("NumofDisp", "Stereo"), 'textureThreshold':cv2.getTrackbarPos("TxtrThrshld", "Stereo"), 
        #         'uniquenessRatio':cv2.getTrackbarPos("UniqRatio", "Stereo"), 'speckleRange':cv2.getTrackbarPos("SpeckleRange", "Stereo"), 'speckleWindowSize':cv2.getTrackbarPos("SpeckleSize", "Stereo")},
        #         sort_keys=True, indent=4, separators=(',',':'))
        result = json.dumps({'SADWindowSize':variable_mapping["SWS"], 'preFilterSize':variable_mapping['PreFiltSize'], 'preFilterCap':variable_mapping['PreFiltCap'], 
                'minDisparity':variable_mapping['MinDisp'], 'numberOfDisparities': variable_mapping['NumofDisp'], 'textureThreshold':variable_mapping['TxtrThrshld'], 
                'uniquenessRatio':variable_mapping['UniqRatio'], 'speckleRange':variable_mapping['SpeckleRange'], 'speckleWindowSize':variable_mapping['SpeckleSize']},
                sort_keys=True, indent=4, separators=(',',':'))
        fName = '3dmap_set.txt'
        f = open (str(fName), 'w')
        f.write(result)
        f.close()
        print ('Settings saved to file '+fName)


    if current_load != 0:
        loading = True
        fName = '3dmap_set.txt'
        print('Loading parameters from file...')
        f=open(fName, 'r')
        data = json.load(f)

        cv2.setTrackbarPos("SWS", "Stereo", data['SADWindowSize'])
        cv2.setTrackbarPos("PreFiltSize", "Stereo", data['preFilterSize'])
        cv2.setTrackbarPos("PreFiltCap", "Stereo", data['preFilterCap'])
        cv2.setTrackbarPos("MinDisp", "Stereo", data['minDisparity']+100)
        cv2.setTrackbarPos("NumofDisp", "Stereo", int(data['numberOfDisparities']/16))
        cv2.setTrackbarPos("TxtrThrshld", "Stereo", data['textureThreshold'])
        cv2.setTrackbarPos("UniqRatio", "Stereo", data['uniquenessRatio'])
        cv2.setTrackbarPos("SpeckleRange", "Stereo", data['speckleRange'])
        cv2.setTrackbarPos("SpeckleSize", "Stereo", data['speckleWindowSize'])

        f.close()
        print ('Parameters loaded from file '+fName)
        print ('Redrawing depth map with loaded parameters...')
        print ('Done!') 

def activateTrackbars(x):
    global loading
    loading = False
    

def create_trackbars() :
    global loading
    # variables = ["SWS", "SpeckleSize", "SpeckleRange", "UniqRatio", "TxtrThrshld", "NumofDisp",
    # "MinDisp", "PreFiltCap", "PreFiltSize"]
    # for v in variables:

    #SWS cannot be larger than the image width and image heights.
    #In this case, width = 320 and height = 240

    #https://stackoverflow.com/questions/46951610/opencv-python-trackbar-callback
    cv2.createTrackbar("SWS", "Stereo", 115, 230, activateTrackbars)
    cv2.createTrackbar("SpeckleSize", "Stereo", 0, 300, activateTrackbars)
    cv2.createTrackbar("SpeckleRange", "Stereo", 0, 40, activateTrackbars)
    cv2.createTrackbar("UniqRatio", "Stereo", 1, 20, activateTrackbars)
    cv2.createTrackbar("TxtrThrshld", "Stereo", 0, 1000, activateTrackbars)
    cv2.createTrackbar("NumofDisp", "Stereo", 1, 16, activateTrackbars)
    cv2.createTrackbar("MinDisp", "Stereo", -100, 200, activateTrackbars)
    cv2.createTrackbar("PreFiltCap", "Stereo", 1, 63, activateTrackbars)
    cv2.createTrackbar("PreFiltSize", "Stereo", 5, 255, activateTrackbars)
    cv2.createTrackbar("Save Settings", "Stereo", 0, 1, activateTrackbars)
    cv2.createTrackbar("Load Settings","Stereo", 0, 1, activateTrackbars)




#################################################################################################
if __name__ == '__main__':
    left_camera = Start_Cameras(0).start()
    right_camera = Start_Cameras(1).start()

    # Initialise trackbars and windows
    cv2.namedWindow("Stereo")
    create_trackbars()

    print ("Cameras Started")

    variables = ["SWS", "SpeckleSize", "SpeckleRange", "UniqRatio", "TxtrThrshld", "NumofDisp",
    "MinDisp", "PreFiltCap", "PreFiltSize"]

    variable_mapping = {"SWS" : 15, "SpeckleSize" : 100, "SpeckleRange" : 15, "UniqRatio" : 10, "TxtrThrshld" : 100, "NumofDisp" : 1,
    "MinDisp": -25, "PreFiltCap" : 30, "PreFiltSize" : 105}
    # dict.fromkeys(variables)

    while True:
        left_grabbed, left_frame = left_camera.read()
        right_grabbed, right_frame = right_camera.read()

        if left_grabbed and right_grabbed:
            left_gray_frame = cv2.cvtColor(left_frame, cv2.COLOR_BGR2GRAY)
            right_gray_frame = cv2.cvtColor(right_frame, cv2.COLOR_BGR2GRAY)

            calibration = StereoCalibration(input_folder='calib_result')
            rectified_pair = calibration.rectify((left_gray_frame, right_gray_frame))

            #getting trackbar position and assigning to the variables
            if loading == False:
                for v in variables:
                    current_value = cv2.getTrackbarPos(v, "Stereo")
                    if v == "SWS" or v == "PreFiltSize":
                        if current_value < 5:
                            current_value = 5
                        if current_value % 2 == 0:
                            current_value += 1
                    
                    if v == "NumofDisp":
                        if current_value == 0:
                            current_value = 1
                        current_value = current_value * 16
                    if v == "MinDisp":
                        current_value = current_value - 100
                    if v == "UniqRatio" or v == "PreFiltCap":
                        if current_value == 0:
                            current_value = 1
                    
                    variable_mapping[v] = current_value


            
           #getting save and load trackbar positions

            current_save = cv2.getTrackbarPos("Save Settings", "Stereo")
            current_load = cv2.getTrackbarPos("Load Settings", "Stereo")
 
            save_load_map_settings(current_save, current_load, variable_mapping)
            cv2.setTrackbarPos("Save Settings", "Stereo", 0)
            cv2.setTrackbarPos("Load Settings", "Stereo", 0)
            disparity = stereo_depth_map(rectified_pair, variable_mapping)
            #Convering Numpy Array to CV_8UC1
            image = np.array(disparity * 255, dtype = np.uint8)
            disparity_color = cv2.applyColorMap(image, cv2.COLORMAP_JET)
            # print("disparity {}".format(disparity.shape))
            # print("rect pair {}".format(rectified_pair[1].shape))
            # print("Rect values {}".format(rectified_pair[1]))
            # display_image = np.concatenate((disparity, rectified_pair[1]), 1)
            
            # print(type(disparity))
            cv2.imshow("Stereo", disparity_color)
            cv2.imshow("Left", rectified_pair[0])
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
                

