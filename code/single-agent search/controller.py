import copy
import controller1
class controller:


##    This function returns path in form of list of object move class defined in controller1 .It is called by view 
##    Input : Board
##            2(intial Position, Final position) -> Musketeer's Move
##    Output : list of move class objects
    
    def makeMove(self,board):
        boardState = copy.deepcopy(board)
        listOfMoves = controller1.singleAgentSearch(boardState)
        return listOfMoves


