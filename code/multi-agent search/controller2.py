##Takes the input currentBoardState and
##return a list of two objects initial position and Final Position
##Board is in form of 2-D list where left top is [0,0] and right Bottom is [4,4]

##In Board
##0 -> Empty Location
##1 -> Musketeer
##2 -> soldier


def musketeerMove(board):

# Sample Code
    for i in range(5):
        for j in range(5):
            if board[i][j]==1:
                if i-1>=0 and board[i-1][j]==2:
                    return [[i,j],[i-1,j]]

                if i+1<5 and board[i+1][j]==2:
                    return [[i,j],[i+1,j]]
                if j-1>=0 and board[i][j-1]==2:
                    return [[i,j],[i,j-1]]

                if j+1<5 and board[i][j+1]==2:
                    return [[i,j],[i,j+1]]
                






##
## Write your code here
##  



##    return [ [initial Position Row, initial Position Column], [Final Position Row, Final Position Column]] 
    return [[0,0],[1,0]]
