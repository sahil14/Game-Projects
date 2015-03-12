import model
import controller1
import time
import random

class controller:
##  Creating Model Class Object
    modelObj = model.model()
## defines difficulty level of the game 1-> easy, 2 -> medium, 3 -> Hard     
    level = 2
    print(level)
    

##    This function makes the move, update the model and return current board state.It is called by view.
##    Input : variable Aruguments
##            0 -> soldier's Move
##            2(intial Position, Final position) -> Musketeer's Move
##    Output : Current Board State
    
    def makeMove(self,*arg):
        # Soldiers' Move
        if len(arg)== 0:
            i1 = time.clock()
            if self.level == 1:
                controller1.cutoffDepth = 5
                controller1.factor = random.randrange(1,12)
                
            elif self.level == 2:
                length = len(self.listOfMove())
                if length <  24:
                    controller1.cutoffDepth = 5
                    controller1.factor = random.randrange(1,12)
                elif length <= 28:
                    controller1.cutoffDepth = 7
                    controller1.factor = 1
                else:
                    controller1.cutoffDepth = 8
                    controller1.factor = 1
                
            else:              
                # length contains list of Moves and According to number of moves depth of minimax tree changes     
                length = len(self.listOfMove())
                if length <  24:
                    controller1.cutoffDepth = 5
                    controller1.factor = random.randrange(1,12)
                elif length <= 28:
                    controller1.cutoffDepth = 7
                    controller1.factor = 1
                else:
                    controller1.cutoffDepth = 10
                    controller1.factor = 1


            # calling alpha beta pruning tree.
            move =  controller1.alphaBeta(self.modelObj.currentBoardState,controller1.cutoffDepth,-controller1.infinity,controller1.infinity,True)

            print(time.clock()-i1)
            # updating the model and adding the move to list of moves
            self.modelObj.makeMove(move[0],move[1])
        # Musketeers' Move

        elif len(arg)==2:
            
            self.modelObj.makeMove(arg[0], arg[1])
        # invalid number of arguments
        else:
            print('Supply Correct Arguments')
        return self.modelObj.currentBoardState

##    Return list of Moves made in form of Memento Objects  to the view which are present in the model
    
    def listOfMove(self):
        return self.modelObj.listMementoObj

## Reset the current Board State to default
    def reset(self):
        self.modelObj.reset()
        return True
## Undo the current Board State to last Board State
    def undo(self):
        return self.modelObj.undoMove()
