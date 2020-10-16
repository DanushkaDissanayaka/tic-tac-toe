import cv2
import numpy as np
import copy

class Node():
    index = 0 
    score = 0

# define output video width and hight
video_width = 640
video_hight = 480
#defiene size of a squre and number of sqres per row and column shuld be 3 for our game

videoCapture = cv2.VideoCapture(0)
videoCapture.set(3,video_width)
videoCapture.set(4,video_hight)

#define symboles for players
human_symbol = 'O'
ai_symbol = 'X'
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

gridpoints = gridpoint(video_width,video_hight,150,3)


# check the circle in one of squre position
def check_position(x,y,r,gridpoints,marklist):
    # i = 0
    max_point_x = x+r
    min_point_x = x-r
    max_point_y = y+r
    min_point_y = y-r
    for i in range (len(gridpoints)):
        #we dont need to check if the position is alredy fill
        if ((marklist[i] == human_symbol) or (marklist[i] == ai_symbol)):
            continue
        #check if the position is not fill
        point = gridpoints[i]
        if((point[0][0] < min_point_x) and (point[1][0] > max_point_x) and (point[0][1] < min_point_y ) and (point[1][1] > max_point_y)):
            # print(i+1)
            return i
        # i += 1
        # else:
            # print ('not found')
    return -1

def check_wining(board):
     #wining possibilities
    winCombos = [[0, 1, 2],[3, 4, 5],[6, 7, 8],[0, 4, 8],[2, 4, 6],[0, 3, 6],[1, 4, 7],[2, 5, 8]]
    for i in range(len(winCombos)):
      H_win = 0
      AI_win = 0
      for j in range (len(winCombos[i])):
            if(board[winCombos[i][j]] == human_symbol):
                H_win += 1
            if(board[winCombos[i][j]] == ai_symbol):
                AI_win += 1
            if(H_win == 3):
                print("Human won the game")
                return human_symbol
            if(AI_win == 3):
                print("AI won the game")
                return ai_symbol
    return 'N'

def showresult(result,marklist):
    while True:
        ret, image = videoCapture.read()
        i=0
        for point in gridpoints:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image,str(marklist[i]),(point[0][0]+75,point[0][1]+75), font, 2,(0,255,0),2)
            cv2.rectangle(image,(point[0][0],point[0][1]),(point[1][0],point[1][1]),(0,0,255),2)
            i += 1
        cv2.putText(image,result,(10,(video_hight/2)), font, 1.5,(255,0,0),2)
        cv2.imshow('Video',image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def emptySqure(board):
    emptyList = []
    for i in range (len(board)):
        if (board[i]!=''):
            continue
        emptyList.append(i)
    return emptyList
    
def minMax(newBoard,player):
    availableSpots = emptySqure(newBoard)

    if (check_wining(newBoard) == ai_symbol):
        return -10
    elif (check_wining(newBoard) == human_symbol):
        return 10
    elif (len(availableSpots)==0):
        return 0
    moves = []
    for i in range (len(availableSpots)):
        node = Node()
        node.index = availableSpots[i]
        newBoard[availableSpots[i]] = player

        if (player == ai_symbol):
            node.score = minMax(newBoard[:],human_symbol)
        else:
            node.score = minMax(newBoard[:],ai_symbol)
        # newBoard[availableSpots[i]] = ''
        moves.append(node)
    
    bestMove = 0
    if (player == ai_symbol):
        best_score = -10000
        for node in moves:
             if (node.score > best_score):
                 best_score = node.score
                 bestMove = node.index
        else:
            best_score = 10000
            for node in moves:
             if (node.score < best_score):
                 best_score = node.score
                 bestMove = node.index
    return bestMove

def start():
    #list for mark the filled positions
    marklist = ['' for i in xrange(len(gridpoints))]
    change = False
    while True:
        ret, image = videoCapture.read()
        # image=cv2.flip(image, +1)
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
                #if the position available then mark it as filled with user symbole
                if(index != -1):
                    marklist[index] = human_symbol
                    change = True
        i=0
        # Add grid to image
        for point in gridpoints:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image,str(marklist[i]),(point[0][0]+75,point[0][1]+75), font, 2,(0,255,0),2)
            cv2.rectangle(image,(point[0][0],point[0][1]),(point[1][0],point[1][1]),(0,0,255),2)
            i += 1
        win = check_wining(marklist)
        if(win !='N'):
            showresult(win,marklist)
            break
        # Its AI turn now
        if (change):
            move = minMax(marklist[:],ai_symbol)
            marklist[move] = ai_symbol
            print(move)
            change = False
            
        cv2.imshow('Video',image)
        win = check_wining(marklist)
        if(win !='N'):
            showresult(win,marklist)
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
start()
videoCapture.release()
cv2.destroyAllWindows()