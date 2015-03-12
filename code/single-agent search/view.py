import pygame,sys
import os
from pygame.locals import *
import controller

controllerObj = controller.controller()

BOARDWIDTH = 15
BOARDHEIGHT = 15
CELLSIZE = 35
WINDOWWIDTH = 860
WINDOWHEIGHT = 640
FPS = 300

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

XMARGIN = 60   #int((WINDOWWIDTH-(CELLSIZE*BOARDWIDTH+(BOARDWIDTH-1)))/2)
YMARGIN = 50    #int((WINDOWHEIGHT-(CELLSIZE*BOARDHEIGHT+(BOARDHEIGHT-1)))/2)

_image_library = {} # dictionary to store images


def main():
	global FPSCLOCK,DISPLAYWINDOW,BASICFONT,BASICFONTSMALL,HIGHLIGHT_RECT,HIGHLIGHT_SURF

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYWINDOW = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
	pygame.display.set_caption('Single Agent Search - The Three Musketeers Board Game')
	BASICFONT = pygame.font.Font('freesansbold.ttf',BASICFONTSIZE)
	BASICFONTSMALL = pygame.font.Font('freesansbold.ttf',BASICFONTSIZESMALL)

	HIGHLIGHT_SURF,HIGHLIGHT_RECT = makeText('Highlight',WHITE,GREEN,WINDOWWIDTH-120,20)

	mainBoard = getStartingBoard()	
	drawBoard(mainBoard)

	while True:
		
		checkForQuit()
		
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONUP:
				if HIGHLIGHT_RECT.collidepoint(event.pos):
					tracePath(mainBoard)

		if event.type == QUIT:
			pygame.quit()
			sys.exit()

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

def getLeftTopOfCell(cellx,celly):
	left = XMARGIN + (cellx*CELLSIZE) + (cellx-1)
	top = YMARGIN + (celly*CELLSIZE) + (celly-1)
	return (top,left)	

def makeText(text,color,bgcolor,top,left):
	textSurf = BASICFONT.render(text,True,color,bgcolor)
	textRect = textSurf.get_rect()
	textRect.topleft = (top,left)
	return (textSurf,textRect)

def makeTextSmall(text,color,top,left):
	textSurf = BASICFONTSMALL.render(text,True,color)
	textRect = textSurf.get_rect()
	textRect.topleft = (top,left)
	DISPLAYWINDOW.blit(textSurf,textRect)
	
def drawCell(cellx,celly,number,adjx=0,adjy=0):
	left,top = getLeftTopOfCell(cellx,celly)
	pygame.draw.rect(DISPLAYWINDOW,CELLCOLOR,(left+adjx,top+adjy,CELLSIZE,CELLSIZE))
	if number == 1:
		imageSurf = get_image('../images/musketeers.png')
	elif number == 2:
		imageSurf = get_image('../images/soldier.png')
	elif number == 3:
		imageSurf = get_image('../images/diamond.jpg')
	elif number == 0:
		return

	imageSurf = pygame.transform.scale(imageSurf,(30,30))	
	imageRect = imageSurf.get_rect()
	imageRect.center = left + int(CELLSIZE/2)+adjx, top+int(CELLSIZE/2)+adjy
	DISPLAYWINDOW.blit(imageSurf,imageRect)

def drawBoard(board):
	background = get_image('../images/back.png')
	background = pygame.transform.scale(background,(WINDOWWIDTH,WINDOWHEIGHT))
	backRect = background.get_rect()
	DISPLAYWINDOW.blit(background,backRect)

	for cellx in range(len(board)):
		for celly in range(len(board[0])):
			drawCell(cellx,celly,board[cellx][celly])

	for i in range(len(board[0])):
		makeTextSmall(str(i+1),WHITE,YMARGIN + (i*CELLSIZE) + i-3 + int(CELLSIZE/2),XMARGIN-22)

	for i in range(len(board)):
		makeTextSmall(chr(ord('a')+i),WHITE,YMARGIN-20,XMARGIN + (i*CELLSIZE) + i-10 + int(CELLSIZE/2))
			
	left,top = getLeftTopOfCell(0,0)
	width = BOARDWIDTH*CELLSIZE
	height = BOARDHEIGHT*CELLSIZE
	pygame.draw.rect(DISPLAYWINDOW,BORDERCOLOR,(left-5,top-5,width+23,height+23),4)
	DISPLAYWINDOW.blit(HIGHLIGHT_SURF,HIGHLIGHT_RECT)

def getStartingBoard():
	board = []
	inp = open('input.txt','r')
	board = [[int(n) for n in line.split()] for line in inp]
	inp.close()
	return board

def tracePath(board):
	moves = controllerObj.makeMove(board)
	for i in range(len(moves)-1):
		start_pos = moves[i]
		end_pos = moves[i+1]
		top1,left1 = getLeftTopOfCell(start_pos[0],start_pos[1])
		top2,left2 = getLeftTopOfCell(end_pos[0],end_pos[1])
		coord1 = (top1 + CELLSIZE/2,left1+CELLSIZE/2)
		coord2 = (top2 + CELLSIZE/2,left2+CELLSIZE/2)
		pygame.draw.line(DISPLAYWINDOW,BLACK,coord1,coord2,2)



def get_image(path):
	global _image_library
	image = _image_library.get(path)
	if image == None:
		canonicalized_path = path.replace('/',os.sep).replace('\\',os.sep)
		image = pygame.image.load(canonicalized_path)
		_image_library[path] = image
	return image

if __name__ == '__main__':
	main()