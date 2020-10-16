import numpy as np
import cv2
import grid
import game

# define output video width and hight
video_width = 640
video_hight = 480

videoCapture = cv2.VideoCapture(0)
videoCapture.set(3,video_width)
videoCapture.set(4,video_hight)

gridpoints = grid.gridpoint(video_width,video_hight,130,3)

current_state = "Not Done"
winner = None
current_player_idx = 1

while True:
    ret,image = videoCapture.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #gray = cv2.blur(gray,(5,5))
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.4, 30)

    if current_player_idx == 0:
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                cv2.circle(image, (x, y), r, (0, 255, 0), 4)
                index = grid.check_position(x,y,r,gridpoints)

                #if the position available print position
                if(index != -1):
                    block_choice = index
                    success = game.play_move(game.game_state ,game.players[current_player_idx], block_choice)
                    if success:
                        current_player_idx = (current_player_idx + 1)%2
                    print(index)
    elif current_player_idx == 1:
        block_choice = game.getBestMove(game.game_state, game.players[current_player_idx])
        game.play_move(game.game_state ,game.players[current_player_idx], block_choice)
        current_player_idx = (current_player_idx + 1)%2
    i=0
    for point in gridpoints:
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image,str(game.game_state[i/3][i%3]),(point[0][0]+75,point[0][1]+75), font, 2,(0,255,0),2)
        cv2.rectangle(image,(point[0][0],point[0][1]),(point[1][0],point[1][1]),(0,0,255),2)
        i=i+1

    winner, current_state = game.check_current_state(game.game_state)
    if winner is not None:
        print(str(winner) + " won!")
        break
        
    if current_state is "Draw":
        print("Draw!")
        break


    cv2.imshow('Video',image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

videoCapture.release()
cv2.destroyWindow("Video") 