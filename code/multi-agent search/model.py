import copy

##This class contains two members initial position and final Position
##history is stored in form of list of object of this class
class memento:
    def __init__(self):
        self.initialPos = [-1,-1]
        self.finalPos = [-1,-1]
## Initial Board Configuration
defaultBoardState = [[1,2,2,2,2],
                     [2,2,2,2,2],
                     [2,2,1,2,2],
                     [2,2,2,2,2],
                     [2,2,2,2,1]]
class model:
    global defaultBoardState
    # Stores current board State
    currentBoardState = copy.deepcopy(defaultBoardState) 
    # stores list of memento objects of hsitory of moves 
    listMementoObj = []
##  Here move comes after validation
    def makeMove(self,initialPos,finalPos):
        self.currentBoardState[finalPos[0]][finalPos[1]] = self.currentBoardState[initialPos[0]][initialPos[1]]
        self.currentBoardState[initialPos[0]][initialPos[1]] = 0
        createObj = memento()
        createObj.initialPos = initialPos
        createObj.finalPos = finalPos
        self.listMementoObj.append(createObj)
        return 1

##  Change the current board state to previous state. It also appends the history
    
    def undoMove(self):
        initialPos = self.listMementoObj[-1].initialPos
        finalPos = self.listMementoObj[-1].finalPos
        self.currentBoardState[initialPos[0]][initialPos[1]] = self.currentBoardState[finalPos[0]][finalPos[1]]

        if self.currentBoardState[finalPos[0]][finalPos[1]] == 1:
            self.currentBoardState[finalPos[0]][finalPos[1]] = 2
        else:    
            self.currentBoardState[finalPos[0]][finalPos[1]] =  0

        del self.listMementoObj[-1]
        return 1

    
##  Reset the history and Change the current board state to default state
    
    def reset(self):
        global defaultBoardState
        del self.listMementoObj[:]
        self.currentBoardState = copy.deepcopy(defaultBoardState) 
        return 1    
        
        
            
