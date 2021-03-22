import cv2
import numpy as np
from start_cameras import Start_Cameras
from datetime import datetime
import time
import os
from os import path

#Photo Taking presets
total_photos = 30  # Number of images to take
countdown = 5  # Interval for count-down timer, seconds
font = cv2.FONT_HERSHEY_SIMPLEX  # Cowntdown timer font


def TakePictures():
    val = input("Would you like to start the image capturing? (Y/N) ")

    if val.lower() == "y":
        left_camera = Start_Cameras(0).start()
        right_camera = Start_Cameras(1).start()
        cv2.namedWindow("Images", cv2.WINDOW_NORMAL)

        counter = 0
        t2 = datetime.now()
        while counter <= total_photos:
            #setting the countdown
            t1 = datetime.now()
            countdown_timer = countdown - int((t1 - t2).total_seconds())

            left_grabbed, left_frame = left_camera.read()
            right_grabbed, right_frame = right_camera.read()

            if left_grabbed and right_grabbed:
                #combine the two images together
                images = np.hstack((left_frame, right_frame))
                #save the images once the countdown runs out
                if countdown_timer == -1:
                    counter += 1
                    print(counter)

                 #Check if directory exists. Save image if it exists. Create folder and then save images if it doesn't
                    if path.isdir('../images') == True:
                        #zfill(2) is used to ensure there are always 2 digits, eg 01/02/11/12
                        filename = "../images/image_" + str(counter).zfill(2) + ".png"
                        cv2.imwrite(filename, images)
                        print("Image: " + filename + " is saved!")
                    else:
                        #Making directory
                        os.makedirs("../images")
                        filename = "../images/image_" + str(counter).zfill(2) + ".png"
                        cv2.imwrite(filename, images)
                        print("Image: " + filename + " is saved!")

                    t2 = datetime.now()
                    #suspends execution for a few seconds
                    time.sleep(1)
                    countdown_timer = 0
                    next
                    
                #Adding the countdown timer on the images and showing the images
                cv2.putText(images, str(countdown_timer), (50, 50), font, 2.0, (0, 0, 255), 4, cv2.LINE_AA)
                cv2.imshow("Images", images)

                k = cv2.waitKey(1) & 0xFF

                if k == ord('q'):
                    break
                    
            else:
                break

    elif val.lower() == "n":
        print("Quitting! ")
        exit()
    else:
        print ("Please try again! ")

    left_camera.stop()
    left_camera.release()
    right_camera.stop()
    right_camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    TakePictures()
                
                
                
