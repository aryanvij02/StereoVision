#This script is to go through all the images taken for rectification and select which are good
#The images will then be split into left and right images respectively 

import cv2 
import os

# Global variables preset
total_photos = 30
photo_height = 360
photo_width = 1280
img_height = 360
img_width = 640


def SeperateImages():
    photo_counter = 1
    
    if (os.path.isdir("../pairs") == False):
        os.makedirs("../pairs")
        
    while photo_counter != total_photos:
        k = None
        filename = '../images/image_'+ str(photo_counter).zfill(2) + '.png'
        if os.path.isfile(filename) == False:
            print("No file named " + filename)
            photo_counter += 1
            
            continue
        pair_img = cv2.imread(filename, -1)
        
        print ("Image Pair: " + str(photo_counter))
        cv2.imshow("ImagePair", pair_img)
        
        #waits for any key to be pressed
        k = cv2.waitKey(0) & 0xFF
 
        if k == ord('y'):
            # save the photo
            imgLeft = pair_img[0:img_height, 0:img_width]  # Y+H and X+W
            imgRight = pair_img[0:img_height, img_width:photo_width]
            leftName = '../pairs/left_' + str(photo_counter).zfill(2) + '.png'
            rightName = '../pairs/right_' + str(photo_counter).zfill(2) + '.png'
            cv2.imwrite(leftName, imgLeft)
            cv2.imwrite(rightName, imgRight)
            print('Pair No ' + str(photo_counter) + ' saved.')
            photo_counter += 1
     
        elif k == ord('n'):
            # skip the photo
            photo_counter += 1
            print ("Skipped")
            
        elif k == ord('q'):
            break  
  

            
    
    print('End cycle')
    
if __name__ == '__main__':

    print ("The paired images will be shown")
    print ("Press Y to accept & save the image")
    print ("Press N to skip the image if it is blurry/unclear/cut-off") 
    SeperateImages()



