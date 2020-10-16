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
def check_position(x,y,r,gridpoints):
    # i = 0
    max_point_x = x+r
    min_point_x = x-r
    max_point_y = y+r
    min_point_y = y-r
    for i in range (len(gridpoints)):
        point = gridpoints[i]
        if((point[0][0] < min_point_x) and (point[1][0] > max_point_x) and (point[0][1] < min_point_y ) and (point[1][1] > max_point_y)):
            return i+1
    #return not found as -1
    return -1