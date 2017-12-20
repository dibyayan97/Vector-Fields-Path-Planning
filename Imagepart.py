import cv2
import imutils
import numpy as np
import serial
import math

cap = cv2.VideoCapture(1)
cX_botf = 0
cY_botf = 0
cX_botb = 0
cY_botb = 0
cX_goal = 0
cY_goal = 0
cX_ball = 0
cY_ball = 0

angle = 0
orient=0


def image_processing():
    global orient, cX_botf, cY_botf, cX_botb, cY_botb, cX_goal, cY_goal, angle, cX_ball, cY_ball
    
    while(1):

        
        #taking each frame
        _, frame = cap.read()
        image = frame.copy()
        cv2.imshow("Image", image)

        #Convert BGR TO HSV
        blurred = cv2.GaussianBlur(image, (5,5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        #define range of blue color in HSV
        lower_red = np.array([150,100,100])
        upper_red = np.array([179,255,255])

        lower_green = np.array([45,100,50])
        upper_green = np.array([75, 255,255])

        lower_yellow = np.array([20,100,100])
        upper_yellow = np.array([30,255,255])

        lower_blue = np.array([110,50,50])
        upper_blue = np.array([130,255,255])

        #Threshold image to only blue color
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

        kernel = np.ones((5,5), np.uint8)

        if cX_botb & cX_botf & cX_goal:
            global angle
                    
            cv2.arrowedLine(image, (cX_botb, cY_botb,), (cX_botf, cY_botf), (0,255,0), 5)
            cv2.line(image, (cX_botb, cY_botb), (cX_goal, cY_goal), (0,255,0), 5)
            m1 = math.degrees(math.atan2((cY_botf - cY_botb),(cX_botf-cX_botb)))
            m2 = math.degrees(math.atan2((cY_goal - cY_botb),(cX_goal-cX_botb)))
            angle = abs(m2)-abs(m1)
##            print("m1 = "+str(m1)+"  m2 = "+str(m2)+"  angle = "+str(angle))
##            print(angle)
            cv2.putText(image, "Angle: "+str(angle), (10,10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0),2)
            cv2.imshow("Image", image)


    #---------------------------------------------------------------------------------------------#
        
        img_erosion = cv2.erode(mask_red, kernel, iterations=7)
        mask_red = cv2.dilate(img_erosion, kernel, iterations=50)

        # find contours in the thresholded image
        cnts = cv2.findContours(mask_red.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        ##if cnts != 0:
        ##    print (cnts);
        # loop over the contours
        for c in cnts:
                
                # compute the center of the contour
                M = cv2.moments(c)
                cX_botf = int(M["m10"] / M["m00"])
                cY_botf = int(M["m01"] / M["m00"])

                # draw the contour and center of the shape on the image
                cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                cv2.circle(image, (cX_botf, cY_botf), 7, (255, 255, 255), -1)
                cv2.putText(image, "center: "+str(cX_botf-20)+","+str(cY_botf-20), (cX_botf - 20, cY_botf - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                # show the image
                cv2.imshow("Image", image)

    ##            print("1")
    ##            ser = serial.Serial("COM15", 19200)
    ##            print(ser)
    ##            ser.write(cX)
    ##            print("2")

    #---------------------------------------------------------------------------------------#


        img_erosion = cv2.erode(mask_green, kernel, iterations=3)
        mask_green = cv2.dilate(img_erosion, kernel, iterations=10)

        cnts = cv2.findContours(mask_green.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        for c in cnts:
                
                # compute the center of the contour
                M = cv2.moments(c)
                cX_goal = int(M["m10"] / M["m00"])
                cY_goal = int(M["m01"] / M["m00"])

                # draw the contour and center of the shape on the image
                cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                cv2.circle(image, (cX_goal, cY_goal), 7, (255, 255, 255), -1)
                cv2.putText(image, "center: "+str(cX_goal-20)+","+str(cY_goal-20), (cX_goal - 20, cY_goal - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                # show the image
                cv2.imshow("Image", image)
        
    #---------------------------------------------------------------------------------------#


        
        img_erosion = cv2.erode(mask_yellow, kernel, iterations=5)
        mask_yellow = cv2.dilate(img_erosion, kernel, iterations=50)

        cnts = cv2.findContours(mask_yellow.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        for c in cnts:    
                # compute the center of the contour
                M = cv2.moments(c)
                cX_botb = int(M["m10"] / M["m00"])
                cY_botb = int(M["m01"] / M["m00"])

                # draw the contour and center of the shape on the image
                cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                cv2.circle(image, (cX_botb, cY_botb), 7, (255, 255, 255), -1)
                cv2.putText(image, "center: "+str(cX_botb-20)+","+str(cY_botb-20), (cX_botb - 20, cY_botb - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    
                

                # show the image
                cv2.imshow("Image", image)
        
    #---------------------------------------------------------------------------------------#    

        
        img_erosion = cv2.erode(mask_blue, kernel, iterations=5)
        mask_blue = cv2.dilate(img_erosion, kernel, iterations=50)

        cnts = cv2.findContours(mask_blue.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        for c in cnts:    
                # compute the center of the contour
                M = cv2.moments(c)
                cX_ball = int(M["m10"] / M["m00"])
                cY_ball = int(M["m01"] / M["m00"])

                # draw the contour and center of the shape on the image
                cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                cv2.circle(image, (cX_botb, cY_botb), 7, (255, 255, 255), -1)
                cv2.putText(image, "center: "+str(cX_ball-20)+","+str(cY_ball-20), (cX_ball - 20, cY_ball - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    
                

                # show the image
                cv2.imshow("Image", image)
        
    #---------------------------------------------------------------------------------------# 
        

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        ##if cnts == 0:
        ##    continue

    cv2.destroyAllWindows()
    print('Inital Details')
    print('Robot: ',cX_botf/100,' , ',cY_botf/100)
    
    if cX_botf != cX_botb:
        orient = math.atan2((cY_botf - cY_botb),(cX_botf - cX_botb))
        if orient < 0:
            orient = orient + 3.14
        
    print('Robot Orientation: ', orient)
    print('Ball: ', cX_ball/100,' , ',cY_ball/100)
    print('Goal: ', cX_goal/100,' , ',cY_goal/100)
    
    return (cX_botf/100, cY_botf/100, cX_ball/100, cY_ball/100, orient, cX_goal/100, cY_goal/100)



	
