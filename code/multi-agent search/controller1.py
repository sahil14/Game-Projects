import random
# Heuristic Values
##class heuristicValues:
##    def __init__(self):
##        self.musketeerInRow = 10
##        self.closeSoldier = 15
##        self.closeSoldier1 = 10
##
###For Computing values for each Musketeer
##class valuesForMusketeers:
##    def __init__(self):
##        self.musketeerInRow = -1
##        self.closeSoldier = 1
##        self.closeSoldier1 = 1

# defining cut off depth for search algorithm
cutoffDepth = 0
# defining Constant Infinity
infinity = 99999999

##In Board Configuration
##1 -> Musketeer
##2 -> Soldier
##0 -> empty Location

factor = 1


##Implementin Search Algorithm Alpha Beta Pruning
##Input : Current Board configuration, Cut-off depth, -infinity, infinity, isSoldier Move (True)
##Output: A list of 4 elements. 1 ,2 tells intial position row and column and 3,4 tells final position row and column


def alphaBeta1(boardState,depth, alpha, beta, isSoldierMove):
    global cutoffDepth
    #checking state is winning or not
    winState = checkWin(boardState, isSoldierMove)
    # leaf node of Tree
    if depth == 0 or winState!= 0:
        #musketeer win
        if winState == 1:
            return -infinity
        #soldier Win        
        elif winState == 2:
            return infinity
        #No One Wins evaluate heuristics
        return evalHeuristic(boardState)
    # computing all possible moves from current State
    childNode = findPossibleMoves(boardState, isSoldierMove)
    #for Max Player 
    if isSoldierMove:
        # v is -infinity
        v = -infinity
        length = len(childNode)
        # child Move is returned for the root Node
        childMove = childNode[0]
        # for each possible Move    
        for i in range(length):
            boardState[childNode[i][0]][childNode[i][1]] = 0
            boardState[childNode[i][2]][childNode[i][3]] = 2
            alphaBetaValue = alphaBeta1(boardState,depth-1, alpha, beta, False)
            if depth == cutoffDepth:
                if v <= alphaBetaValue:
                    childMove = childNode[i]
                    v = alphaBetaValue
            else:
                v = max(v,alphaBetaValue)
            alpha = max(alpha, v)
            boardState[childNode[i][0]][childNode[i][1]] = 2
            boardState[childNode[i][2]][childNode[i][3]] = 0
            # Breaking Condition
            if beta <= alpha:
                break
        # Root Node
        if depth == cutoffDepth and (cutoffDepth == 1 or v != -infinity):
            return [[childMove[0],childMove[1]],[childMove[2],childMove[3]]]

        # Making it to choose defeat at greater depth 
        elif depth == cutoffDepth:
           cutoffDepth = 1
           return alphaBeta1(boardState,cutoffDepth, -infinity, infinity, True)

        # Not a root Node
        else:
            return v
    else:
        # for Min Player
        # v is set to infinity
        v = infinity
        length = len(childNode)
        for i in range(length):
            boardState[childNode[i][0]][childNode[i][1]] = 0
            boardState[childNode[i][2]][childNode[i][3]] = 1

            v = min(v, alphaBeta1(boardState,depth-1, alpha, beta, True))
            boardState[childNode[i][0]][childNode[i][1]] = 1
            boardState[childNode[i][2]][childNode[i][3]] = 2

            beta = min(beta, v)
            if beta <= alpha:
                break
        return v
        
        
    
#Evaluates the value of heuristic for the given Board State
def evalHeuristic(boardState):
    # Stores the location of musketeers.   
    musketeerLocation = []
    global factor
    
##    hValues = heuristicValues()
##    # Objects for computing Values for 3 musketeers
##    m1 = valuesForMusketeers()
##    m2 = valuesForMusketeers()
##    m3 = valuesForMusketeers()
    
    # Find Location of musketeers 
    for i in range(5):
        if len(musketeerLocation) == 3:
           break

        for j in range(5):
           if len(musketeerLocation) == 3:
                break
           if boardState[i][j] == 1:
                musketeerLocation.append([i,j])

    # Min row or Column distance between each pair of Musketeers
    

    
    musketeer12x=  abs(musketeerLocation[0][0] - musketeerLocation[1][0])
    musketeer12y = abs(musketeerLocation[0][1] - musketeerLocation[1][1])
    musketeer13x = abs(musketeerLocation[0][0]- musketeerLocation[2][0])
    musketeer13y = abs(musketeerLocation[0][1] - musketeerLocation[2][1])
    musketeer23x = abs(musketeerLocation[1][0]- musketeerLocation[2][0])
    musketeer23y = abs(musketeerLocation[1][1] - musketeerLocation[2][1])

    if musketeer12x == 0:
        musketeer12x = musketeer12x + 3
    
    if musketeer12y == 0:
        musketeer12y = musketeer12y + 3
    
    if musketeer13x == 0:
        musketeer13x = musketeer13x + 3
    
    if musketeer13y == 0:
        musketeer13y = musketeer13y + 3
    
    if musketeer23x:
        musketeer23x = musketeer23x + 3

    if musketeer23y:
        musketeer23y = musketeer23y + 3

    # finding the distance between musketeer
    a = pow((pow(musketeer12x,2)+pow(musketeer12y,2)),0.5)
    b = pow((pow(musketeer23x,2)+pow(musketeer23y,2)),0.5)
    c = pow((pow(musketeer13x,2)+pow(musketeer13y,2)),0.5)
    countMusk = []
    countSoldier = []
    value = 0
    for i in range(5):
        countMusk.append(boardState[i].count(1))
        countSoldier.append(boardState[i].count(2))
    for i in range(5):
        
        if countMusk[i] == 2:
             value = value - countSoldier[i]
             if i<4:
                 value - countSoldier[i+1]
             if i>0:
                 value - countSoldier[i-1]
            
        elif i<4 and countMusk[i]==1 and countMusk[i+1]==1:
             value = value - countSoldier[i] - countSoldier[i+1]
             if i+1<4:
                 value - countSoldier[i+2]
             if i>0:
                 value - countSoldier[i-1]
                 
             elif countMusk[i] == 1:
                 value = value + 2*countSoldier[i]
                 if i<4:
                     value + 2*countSoldier[i+1]
                 if i>0:
                     value + 2*countSoldier[i-1]
                 

    s = (a+b+c)/2.0
    
    value1 = abs(s*(s-a)*(s-b)*(s-c))
    return 25*value - factor*abs(value1)

#check winning the state of the game

def checkWin(boardState,isSoldierMove):
    isSoldierPresent = False
    # Checking All three Musketeers are in a row or Column or Not
    for i in range(5):
        countInColumn = 0
        countInRow = boardState[i].count(1)
        countSoldier = boardState[i].count(2)
        if countSoldier > 0:
            isSoldierPresent = True
        if countInRow == 3:
            return 2
        for j in range(5):
            if boardState[j][i]==1:
                countInColumn = countInColumn + 1
            
        if countInColumn == 3:
            return 2
    # Checking Winning State for Musketeers
    if not isSoldierMove:       
        for i in range(5):
            for j in range(5):
                if boardState[i][j] == 1:
                    if boardState[abs(i-1)][j] == 2:
                        return 0
                    elif i+1 < 5 and boardState[i+1][j] == 2:
                        return 0
                    elif boardState[i][abs(j-1)] == 2:
                        return 0
                    elif j+1 < 5 and boardState[i][j+1] == 2:
                        return 0
        return 1
    # Checking Atleast One Soldier should be present 
    if not isSoldierPresent:
        return 1
# No One Wins
    return 0

                

#Returns Possible moves from a given Board State
# Input : Board State , isSoldierTurn(Bool)
# Output: List of Lists. Where each sublist signifies a move. Sublist contains 4 elements, where 1,2 elements correponds to intial Position and last 2 for finsl Position

def findPossibleMoves(boardState,isSoldierTurn):

    possibleMoves = []
    # if its Soldier Turn    
    if isSoldierTurn:
        for i in range(5):
            for j in range(5):
                if  boardState[i][j] == 2:
                    if i-1 >= 0 and boardState[i-1][j] == 0:
                        possibleMoves.append([i,j,i-1,j])                        
                    if i+1 < 5 and boardState[i+1][j] == 0:
                        possibleMoves.append([i,j,i+1,j])

                    if j-1 >= 0 and boardState[i][j-1] == 0:
                        possibleMoves.append([i,j,i,j-1])
                    if j+1 < 5 and boardState[i][j+1] == 0:
                        possibleMoves.append([i,j,i,j+1])

    # if its Musketeers' Turn
    else:
        for i in range(5):
            for j in range(5):
                if  boardState[i][j] == 1:
                    if i-1 >= 0 and boardState[i-1][j] == 2:
                        possibleMoves.append([i,j,i-1,j])
                        
                    if i+1 < 5 and boardState[i+1][j] == 2:
                        possibleMoves.append([i,j,i+1,j])

                    if j-1 >= 0 and boardState[i][j-1] == 2:
                        possibleMoves.append([i,j,i,j-1])
                    if j+1 < 5 and boardState[i][j+1] == 2:                       
                        possibleMoves.append([i,j,i,j+1])
    return possibleMoves




                    
