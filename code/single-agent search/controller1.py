##This function takes board as an input
##returns a list of sequence of steps followed by the musketeer to reach the soldier with diamond
##In Board 1 -> musketeer
##         2 -> soldier
##         0 -> empty location
##         3 -> Soldier With Diamond (Goal State)


def singleAgentSearch(board):

    listMove = [[2,6],[2,7],[2,8],[2,9],[3,9],[4,9],[5,9],[6,9]]

## Write your code here

    
    return listMove


## return [[0,0],[0,1],[1,1],[1,2],[1,3]]
## this means that musketeer is located at (0,0) and soldier with diamond at (1,3)
    
