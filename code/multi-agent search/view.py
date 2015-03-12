import pygame, sys, random
import os
from pygame.locals import *
import controller
import copy

controllerObj = controller.controller()
#modelObj = model.model()
# Create the constants
BOARDWIDTH = 5  # number of columns on the board
BOARDHEIGHT = 5  # number of rows on the board
CELLSIZE = 90
WINDOWWIDTH = 860
WINDOWHEIGHT = 640
FPS = 300
BLANK = None

#              R   G   B
BLACK     = (  0,  0,  0)
WHITE     = (255,255,255)
LIGHTSKY  = (239,239,239)
TURQUOISE = (207,226,243)
DARKBLUE  = ( 57,106,211)
LIGHTBLUE = (170,180,220)
GREEN     = (  0,204,  0)

BGCOLOR = LIGHTSKY
CELLCOLOR = TURQUOISE
TEXTCOLOR = WHITE
BUTTONCOLOR = TURQUOISE
BORDERCOLOR = DARKBLUE
BASICFONTSIZE = 20
BASICFONTSIZESMALL = 13



XMARGIN = 140   #int((WINDOWWIDTH-(CELLSIZE*BOARDWIDTH+(BOARDWIDTH-1)))/2)
YMARGIN = 50    #int((WINDOWHEIGHT-(CELLSIZE*BOARDHEIGHT+(BOARDHEIGHT-1)))/2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

_image_library = {} # dictionary to store images

'''Button class to draw the buttons on the top of the board and provide the highlight on mouse hover functionality'''
class Button:
	hovered = False

	def __init__(self,bType,pos):
		self.image = get_image('images/'+bType)  # load the image for the button
		self.pos = pos                 # position of the button
		self.set_rect()
		self.draw()

	def draw(self):                      # draw a circular background for the image to be used as a button
		self.circle = pygame.draw.circle(DISPLAYWINDOW,self.get_color(),(self.pos),25)
		DISPLAYWINDOW.blit(self.image,self.rect)

	def get_color(self):        # changes the color on the mouse hover event
		if self.hovered:
			return LIGHTBLUE
		else:
			return BUTTONCOLOR

	def set_rect(self):             #positions the image on the circle
		self.rect = self.image.get_rect()
		self.rect.topleft = (self.pos[0]-10,self.pos[1]-10)


def main():
	global FPSCLOCK,DISPLAYWINDOW,BASICFONT,BASICFONTSMALL,highlightX,highlightY,initialPos,finalPos,buttons,allmoves

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYWINDOW = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
	pygame.display.set_caption('The Three Musketeers')
	BASICFONT = pygame.font.Font('freesansbold.ttf',BASICFONTSIZE)
	BASICFONTSMALL = pygame.font.Font('freesansbold.ttf',BASICFONTSIZESMALL)

	# Button class objects as buttons
	buttons = [Button('undo.png',(90,40)),Button('reset.png',(190,40)),Button('quit.png',(290,40))] 
	
	mainBoard = getStartingBoard()  # get the starting configuration of the board
	allmoves = []
	drawBoard(mainBoard,-1,-1,allmoves)      # render the board on the screen
	spotx,spoty = (None,None)       # Stores the clicked co-ordinates
	gameOver = False				# Game Over status
	initialPos = [None,None]
	finalPos = [None,None]
	
	
	while True:          #main game loop
		direction = None  # variable to store move direction
		
		checkForQuit()    #Check if game is quit in between
		
		for button in buttons:   # renders the button objects on the screen
			if button.circle.collidepoint(pygame.mouse.get_pos()):
				button.hovered = True
			else:
				button.hovered = False
			button.draw()
		
		for event in pygame.event.get():      #event handling loop	
			if event.type == MOUSEBUTTONUP:
				
				#initialPos = [spotx,spoty]		# stores the co-ordinates of previously selected cell

				spotx,spoty = getSpotClicked(mainBoard,event.pos[0],event.pos[1])  # get the co-ordinates of newly selected cell 

				finalPos = [spotx,spoty]	# stores the co-ordinates of newly selected cell
				
				if(spotx,spoty) == (None,None):
					# Checks if the user clicked on an undo button
					if buttons[0].circle.collidepoint(event.pos): 
						'''if not gameOver:
							recentMoves = controllerObj.listOfMove()
							if len(recentMoves) > 1:
								controllerObj.undo()
								spotx,spoty  = recentMoves[-1].initialPos[0],recentMoves[-1].initialPos[1]
								del allmoves[0]
								
								controllerObj.undo()
								mainBoard = copy.deepcopy(controllerObj.modelObj.currentBoardState)
								del allmoves[0]

							drawBoard(mainBoard,spotx,spoty,allmoves)'''

					# Checks if the user has clicked on reset button		
					elif buttons[1].circle.collidepoint(event.pos): 
						'''gameOver = False
						mainBoard = getStartingBoard()
						controllerObj.reset()
						allmoves = []
						drawBoard(mainBoard,-1,-1,allmoves)'''

					# Checks if the user has clicked on quit button	
					elif buttons[2].circle.collidepoint(event.pos):  #Clicked on quit button
						print "quit button called"
						terminate()

				#else:
					# Checks if the game is over or not
					#if(not gameOver):
						#drawBoard(mainBoard,spotx,spoty,allmoves)	#Draw the board highlighting the selected cell
				
		if not gameOver:		
			controllerObj.makeMove()					# controller computing the soldiers' move
			l = controllerObj.listOfMove()				#  list containing the moves 
			initialPos = l[-1].initialPos
			finalPos = l[-1].finalPos
			if(isValidMove(mainBoard,initialPos,finalPos) and gameOver == False):
				slideAnimation(mainBoard,initialPos,finalPos,1,1)             # sliding the muskteer over the soldier
				
				mainBoard = makeMove(mainBoard,initialPos,finalPos)           # Updating the board state
			#	controllerObj.makeMove(initialPos,finalPos)					  #Making the move in controller so that model is updated

				drawBoard(mainBoard,-1,-1,allmoves)						# to remove the highlighting of a cell	
					
				if(ifGameOverMusk(mainBoard)):
					makeText('Game Over : Soldiers Win',DARKBLUE,BGCOLOR,150,80)  #For game over message			
					gameOver = True
				
				elif(ifGameOverNoSold(mainBoard)):
					makeText('Game Over : Musketeers Win',DARKBLUE,BGCOLOR,150,80)  #For game over message			
					gameOver = True

				else:	
					controllerObj.makeMove()					# controller computing the soldiers' move
					l = controllerObj.listOfMove()				#  list containing the moves 
					slideAnimation(mainBoard,l[-1].initialPos,l[-1].finalPos,2,1)   # sliding the soldier over to the empty space
					mainBoard = makeMove(mainBoard,l[-1].initialPos,l[-1].finalPos)  # Updating the board state
					
					# Checking the win state for musketeers
					if(ifGameOverSold(mainBoard)):
						makeText('Game Over : Musketeers Win',DARKBLUE,BGCOLOR,150,80)  #For game over message						
						gameOver =  True
						
		pygame.display.update()
		FPSCLOCK.tick(FPS)

def terminate():
	pygame.quit()
	sys.exit()

def checkForQuit():
	for event in pygame.event.get(QUIT):	#get all the QUIT events
		terminate()							# terminate if any QUIT events are present
	for event in pygame.event.get(KEYUP):	# get all the KEYUP events
		if event.key == K_ESCAPE:			
			terminate()						# terminate if the KEYUP event was for the Esc key
		pygame.event.post(event)			# put the other KEYUP event objects back

def isValidMove(board,initialPos,finalPos):
	# Function for checking the validity of a move for a musketeer
	if initialPos[0] == None or finalPos[0] == None:
		return False
	else:
		x0,y0 = initialPos[0],initialPos[1]
		x1,y1 = finalPos[0],finalPos[1]
		
		if (board[x0][y0] == 1 and board[x1][y1] == 2): # Checking if any soldier is an immediate neighbour of a musketeer
			if (abs(x0-x1) + abs(y0-y1)) == 1:
				return True
			else:
				makeText('Invalid Move !',DARKBLUE,BGCOLOR,200,80)
				#DISPLAYWINDOW.blit(MOVE_SURF,MOVE_RECT) # Displaying the wrong move message
		return False

def ifGameOverMusk(board):
	# Checking the game over condition for musketeer i.e. if the three musketeers are in a same row or same column
	muskPos = []
	# get the musketeer positions
	for x in range(len(board)):
		for y in range(len(board[0])):
			if board[x][y] == 1:
				muskPos.append([x,y])
	# Checks if the three musketeers are in same row or same column			
	if (muskPos[0][0] == muskPos[1][0] and muskPos[0][0] == muskPos[2][0]) or (muskPos[0][1] == muskPos[1][1] and muskPos[0][1] == muskPos[2][1]):
		return True

def ifGameOverNoSold(board):
        count = 0
        for i in range(5):
                count = count + board[i].count(2)
        if count > 0:
                return False
        else:
                return True
                
def ifGameOverSold(board):
	# Checking the game over condition for soldier i.e. whether there are valid moves left for any musketeer
	muskPos = []
	# get the musketeer positions
	for x in range(len(board)):
		for y in range(len(board[0])):
			if board[x][y] == 1:
				muskPos.append([x,y])

	totalMoves = 0
	# get the no. of possible moves for each musketeer			
	for i in range(len(muskPos)):
		count = 0
		x = muskPos[i][0]
		y = muskPos[i][1]
		
		if(x < len(board)-1):
			if(board[x+1][y] == 2):
				count += 1 
				
		if (x > 0):
			if(board[x-1][y] == 2):
				count += 1
				

		if (y < len(board)-1):
			if (board[x][y+1] == 2):
				count += 1
				

		if (y > 0):
			if (board[x][y-1] == 2):
				count += 1
		#print i,'count',count		
		totalMoves += count
	#print totalMoves
	if(totalMoves > 0):
		return False
	else:
		return True

def makeMove(board,initialPos,finalPos):
	# Making the move on the board matrix
	x0,y0 = initialPos[0],initialPos[1]
	x1,y1 = finalPos[0],finalPos[1]
	move =  chr(ord('a')+x0)+str(y0+1)+" -> "+chr(ord('a')+x1)+str(y1+1)
	board[x1][y1] = board[x0][y0]
	board[x0][y0] = 0
	moveDesc = [board[x1][y1],move]
	allmoves.insert(0,moveDesc)
	drawHistoryTable(allmoves)
	
	return board
	
def getSpotClicked(board,x,y):
	# from the x & y pixel co-ordinates, get the x & y board co-ordinates
	for cellx in range(len(board)):
		for celly in range(len(board[0])):
			left,top = getLeftTopOfCell(cellx,celly)
			cellRect = pygame.Rect(left,top,CELLSIZE,CELLSIZE)
			if cellRect.collidepoint(x,y):
				return (cellx,celly)
	return (None,None)

def getLeftTopOfCell(cellx,celly):
	# get the top-left corner of a cell (pixel co-ordinates)
	left = XMARGIN + (cellx*CELLSIZE) + (cellx-1)
	top = YMARGIN + (celly*CELLSIZE) + (celly-1)
	return (top,left)

def makeText(text,color,bgcolor,top,left):
	# create the Surface and Rect objects for some text
	textSurf = BASICFONT.render(text,True,color)
	textRect = textSurf.get_rect()
	textRect.topleft = (top,left)
	DISPLAYWINDOW.blit(textSurf,textRect)
	#return (textSurf,textRect)

def makeTextSmall(text,color,top,left):
	textSurfSmall = BASICFONTSMALL.render(text,True,color)
	textRectSmall = textSurfSmall.get_rect()
	textRectSmall.topleft = (top,left)
	DISPLAYWINDOW.blit(textSurfSmall,textRectSmall)

def drawScore(board):
	# function for drawing the score on the board
	# +10 for each soldier killed and -50 if two musketeers are in same row or same column
	
	soldRemoved = 0
	muskPos = []
	for x in range(len(board)):
		for y in range(len(board)):
			if board[x][y] == 0:
				soldRemoved += 1
			elif board[x][y] == 1:
				muskPos.append([x,y])

	totalScore = 10*soldRemoved			

	if (muskPos[0][0] == muskPos[1][0] or muskPos[0][0] == muskPos[2][0] or muskPos[1][0] == muskPos[2][0] ):
		totalScore -= 50

	if (muskPos[0][1] == muskPos[1][1] or muskPos[0][1] == muskPos[2][1] or muskPos[1][1] == muskPos[2][1] ):
		totalScore -= 50					
	

	SCORE_SURF = BASICFONT.render('Score : '+str(totalScore),True,DARKBLUE)
	SCORE_RECT = SCORE_SURF.get_rect()
	SCORE_RECT.topleft = (400,30)
	DISPLAYWINDOW.blit(SCORE_SURF,SCORE_RECT)

def getStartingBoard():
	# Return the list of lists as a board with starting configuration as
	# 0 for soldier, 1 for musketeer and 2 for blank space
	board = [[2 for x in range(BOARDWIDTH)] for x in range(BOARDHEIGHT)]
	board[0][0] = 1
	board[(BOARDWIDTH-1)/2][(BOARDWIDTH-1)/2] = 1
	board[BOARDWIDTH-1][BOARDHEIGHT-1] = 1
	return board

def drawHistoryTable(movesList):
	left,top = 600,142
	numMoves = len(movesList)

	for i in range(numMoves):
		if i==13:
			break
		color = CELLCOLOR
		if i%2 == 1:
			color = LIGHTBLUE

		if movesList[i][0] == 1:
			imageSurf = get_image('images/musketeers.png')
		else:
			imageSurf = get_image('images/soldier.png')

		imageSurf = pygame.transform.scale(imageSurf,(25,25))	
		imageRect = imageSurf.get_rect()
		imageRect.center = 	left+20,top+i*31+15

		pygame.draw.rect(DISPLAYWINDOW,BLACK,(left,top+i*31,50,30),3)
		pygame.draw.rect(DISPLAYWINDOW,color,(left,top+i*31,50,30))
		DISPLAYWINDOW.blit(imageSurf,imageRect)
			
		pygame.draw.rect(DISPLAYWINDOW,BLACK,(left+50,top+i*31,150,30),3)
		pygame.draw.rect(DISPLAYWINDOW,color,(left+50,top+i*31,150,30))
		makeTextSmall(movesList[i][1],BLACK,left+100,top+i*31+10)

	tableht = min(numMoves,13)	
	pygame.draw.rect(DISPLAYWINDOW,BORDERCOLOR,(600,110,200,(tableht+1)*31),3)	
	pygame.display.flip()
	
def drawCell(cellx,celly,number,spotx,spoty,adjx = 0,adjy = 0):
	# draw a cell at board co-ordinates cellx and celly,highlighting 
	# the cell if it is the clicked cell
	left,top = getLeftTopOfCell(cellx,celly)
	if cellx == spotx and celly == spoty:
		pygame.draw.rect(DISPLAYWINDOW,LIGHTBLUE,(left+adjx,top+adjy,CELLSIZE,CELLSIZE))
		highlightX,highlightY = cellx,celly
	else:	
		pygame.draw.rect(DISPLAYWINDOW,CELLCOLOR,(left+adjx,top+adjy,CELLSIZE,CELLSIZE))

		
	if(number == 1):
		imageSurf = get_image('images/musketeers.png')#BASICFONT.render('M',True,BLACK)
	elif(number == 2):	
		imageSurf = get_image('images/soldier.png')#BASICFONT.render('S',True,BLACK)
	elif(number == 0):
		return	

	imageRect = imageSurf.get_rect()
	imageRect.center = left + int(CELLSIZE/2)+adjx,top+int(CELLSIZE/2)+adjy
	DISPLAYWINDOW.blit(imageSurf,imageRect)
      
def slideAnimation(board,initialPos,finalPos,player,animationSpeed):
	x0,y0 = initialPos[0],initialPos[1]
	x1,y1 = finalPos[0],finalPos[1]
	animationSpeed = 1
	# prepare the base surface
	baseSurf = DISPLAYWINDOW.copy()
	# draw the new cell over the moving cell on the baseSurf surface
	moveLeft,moveTop = getLeftTopOfCell(x1,y1)
	pygame.draw.rect(baseSurf,CELLCOLOR,(moveLeft,moveTop,CELLSIZE,CELLSIZE))
	
	DISPLAYWINDOW.blit(baseSurf,(0,0))
	sound = pygame.mixer.Sound('../sword.wav')
	sound.play()
	for i in range(0,CELLSIZE+2,animationSpeed):
		# animate the soldier sliding over
		if(x1 == x0 + 1 and y1 == y0):
			drawCell(x0,y0,player,x0,y0,0,i)
		if(x1 == x0 - 1 and y1 == y0):
			drawCell(x0,y0,player,x0,y0,0,-i)
		if(x1 == x0 and y1 == y0 + 1):
			drawCell(x0,y0,player,x0,y0,i,0)
		if(x1 == x0 and y1 == y0 - 1):
			drawCell(x0,y0,player,x0,y0,-i,0)

		pygame.display.update()
		FPSCLOCK.tick(FPS)

def drawBoard(board,spotx,spoty,movesList):

	# function to draw the game board
	background = get_image('images/back.png')
	background = pygame.transform.scale(background,(WINDOWWIDTH,WINDOWHEIGHT))
	backRect = background.get_rect()
	DISPLAYWINDOW.blit(background,backRect)

	for cellx in range(len(board)):
		for celly in range(len(board[0])):
			drawCell(cellx,celly,board[cellx][celly],spotx,spoty)
			
	makeText('History',DARKBLUE,BGCOLOR,660,80)
	pygame.draw.rect(DISPLAYWINDOW,CELLCOLOR,(600,110,200,90))

	pygame.draw.rect(DISPLAYWINDOW,BLACK,(600,110,50,30),3)
	pygame.draw.rect(DISPLAYWINDOW,LIGHTBLUE,(600,110,50,30))

	pygame.draw.rect(DISPLAYWINDOW,BLACK,(650,110,150,30),3)
	pygame.draw.rect(DISPLAYWINDOW,LIGHTBLUE,(650,110,150,30))
	
	makeTextSmall("Player",BLACK,605,120)
	makeTextSmall("Moves",BLACK,700,120)
		
	for i in range(BOARDWIDTH):
		makeText(str(i+1),WHITE,BGCOLOR,YMARGIN + (i*CELLSIZE) + i-3 + int(CELLSIZE/2),XMARGIN-30)

	for i in range(BOARDHEIGHT):
		makeText(chr(ord('a')+i),WHITE,BGCOLOR,YMARGIN-25,XMARGIN + (i*CELLSIZE)+ i-10 + int(CELLSIZE/2) )

	for button in buttons:
		if button.circle.collidepoint(pygame.mouse.get_pos()):
			button.hovered = True
		else:
			button.hovered = False
		button.draw()		

	drawScore(board)	
	left,top = getLeftTopOfCell(0,0)
	width = BOARDWIDTH*CELLSIZE
	height = BOARDHEIGHT*CELLSIZE
	pygame.draw.rect(DISPLAYWINDOW,BORDERCOLOR,(left-5,top-5,width+13,height+13),4)
	drawHistoryTable(movesList)

def get_image(path):
	# function to store the image once loaded locally so that they are not loaded again and again
	global _image_library
	path = '../' + path
	image = _image_library.get(path)
	if image == None:

		canonicalized_path = path.replace('/',os.sep).replace('\\',os.sep)
		image = pygame.image.load(canonicalized_path)
		_image_library[path] = image
	return image

if __name__ == '__main__':
	main()


