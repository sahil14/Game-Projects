import model
import controller1
import controller2
import time
import copy
class controller:
##  Creating Model Class Object
    modelObj = model.model()
    isSoldierMove = False
##    This function makes the move, update the model and return current board state.It is called by view.
##    Input : variable Aruguments
##            0 -> solodier's Move
##            2(intial Position, Final position) -> Musketeer's Move
##    Output : Current Board State
    
    def makeMove(self):
        # Soldiers' Move
        if self.isSoldierMove:
            self.isSoldierMove = False
            length = len(self.listOfMove())
            if length <  24:
                controller1.cutoffDepth = 5
            elif length <= 28:
                controller1.cutoffDepth = 7
            else:
                controller1.cutoffDepth = 8
            move =  controller1.alphaBeta1(self.modelObj.currentBoardState,controller1.cutoffDepth,-controller1.infinity,controller1.infinity,True)
            self.modelObj.makeMove(move[0],move[1])


        # Musketeers' Move
        else:
            self.isSoldierMove = True
            board = copy.deepcopy(self.modelObj.currentBoardState) 
            move = controller2.musketeerMove(board)

            ## Validating Move
            if move[0][0] > -1 and move[0][0] < 5 and move[0][1] > -1 and move[0][1] < 5 and move[1][0] > -1 and move[1][0] < 5 and move[1][1] > -1 and move[1][1] < 5:   
                if self.modelObj.currentBoardState[move[0][0]][move[0][1]] == 1 and self.modelObj.currentBoardState[move[1][0]][move[1][1]] == 2: 
                    self.modelObj.makeMove(move[0],move[1])

        return self.modelObj.currentBoardState
        
##    Return list of Moves made in form of Memento Objects  to the view which are present in the model
    
    def listOfMove(self):
        return self.modelObj.listMementoObj
