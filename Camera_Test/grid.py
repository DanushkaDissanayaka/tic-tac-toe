import cv2
import numpy as np

# define output video width and hight
video_width = 640
video_hight = 480
#defiene size of a squre and number of sqres per row and column shuld be 3 for our game


# calculate grid points
def gridpoint(video_w,video_h,size_of_squre,no_of_squre):
    gridpoint = [[] for i in xrange(no_of_squre*no_of_squre)]
    i = 0
    # calculate center position constant
    center_constant_x = (video_w - (size_of_squre*no_of_squre))/2
    center_constant_y = (video_h -(size_of_squre*no_of_squre))/2
    # calculate grid points
    for y in range (0,size_of_squre*no_of_squre,size_of_squre):
        # y += center_constant_y
        for x in range (0,size_of_squre*no_of_squre,size_of_squre):
            # x += center_constant_x
            # print ('begin',x,y)
            # print ('end',x+size_of_squre,y+size_of_squre)
            gridpoint[i]= [[x+center_constant_x,y+center_constant_y],[x+size_of_squre+center_constant_x,y+size_of_squre+center_constant_y]]
            i=i+1
    # print(gridpoint)
    return gridpoint

# check the circle in one of squre position
def check_position(x,y,r,gridpoints,marklist):
    # i = 0
    max_point_x = x+r
    min_point_x = x-r
    max_point_y = y+r
    min_point_y = y-r
    for i in range (len(gridpoints)):
        #we dont need to check if the position is alredy fill
        if ((marklist[i] == 'H') or (marklist[i] == 'A')):
            continue
        #check if the position is not fill
        point = gridpoints[i]
        if((point[0][0] < min_point_x) and (point[1][0] > max_point_x) and (point[0][1] < min_point_y ) and (point[1][1] > max_point_y)):
            print(i+1)
            return i
        # i += 1
        # else:
            # print ('not found')
    return -1


gridpoints = gridpoint(video_width,video_hight,150,3)

#list for mark the filled positions
marklist = ['' for i in xrange(len(gridpoints))]

videoCapture = cv2.VideoCapture(0)
videoCapture.set(3,video_width)
videoCapture.set(4,video_hight)

while True:
    ret, image = videoCapture.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray,(5,5))
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.4, 30)

    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

		# loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (0, 255, 0), 4)
            index = check_position(x,y,r,gridpoints,marklist)
            # print(x,y)
            #if the position available then mark it as filled
            if(index != -1):
                marklist[index] = 'H'
    i=0
    # Add grid to image
    for point in gridpoints:
        # print (point[0][0])
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image,str(marklist[i]),(point[0][0]+25,point[0][1]+25), font, 0.7,(255,255,255),2)
        cv2.rectangle(image,(point[0][0],point[0][1]),(point[1][0],point[1][1]),(0,0,255),2)
        i += 1

    cv2.imshow('Video',image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # print(marklist)

videoCapture.release()
cv2.destroyAllWindows()
