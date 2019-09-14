#########################################
# File Name: Tetris.py
# Description: This is a template for Tetris Game.
# Author: ICS2OG
# Date: 28/11/2018
#########################################
from TetrisClasses import *
from random import randint
import time

import pygame
pygame.init()
HEIGHT = 600
WIDTH  = 800
GRIDSIZE = HEIGHT/24
gameWindow=pygame.display.set_mode((WIDTH,HEIGHT))

#---------------------------------------#
COLUMNS = 14                            #
ROWS = 22                               # properties of the game field
LEFT = 9                                # set them wisely !!!
RIGHT = LEFT + COLUMNS                  # 
MIDDLE = LEFT + COLUMNS/2               #
TOP = 1                                 #
BOTTOM = TOP + ROWS                     #
#---------------------------------------#

#---------------------------------------#
#   functions                           #
#---------------------------------------#
def redrawGameWindow():               
    gameWindow.blit(mainBkgd, (0, 0))
    drawGrid()
    drawUpcoming()
    drawScore()
    drawLevel()
    drawTime()
    shape.draw(gameWindow, GRIDSIZE)
    obstacles.draw(gameWindow, GRIDSIZE)
    pygame.display.update() 

def drawUpcoming():
    drawText(medFont, "Next:", WHITE, 25*GRIDSIZE, 1*GRIDSIZE)
    drawBox(24, 30, 2, 6)
    nextShape.draw(gameWindow, GRIDSIZE)

def drawScore():
    drawText(medFont, "Score:", WHITE, 25*GRIDSIZE, 7*GRIDSIZE)
    drawText(medFont, str(score), WHITE, 25*GRIDSIZE, 8*GRIDSIZE)
    drawBox(24, 30, 8, 9)

def drawLevel():
    drawText(medFont, "Level:", WHITE, 25*GRIDSIZE, 10*GRIDSIZE)
    drawText(medFont, str(level), WHITE, 25*GRIDSIZE, 11*GRIDSIZE)
    drawBox(24, 30, 11, 12)

def drawTime():
    drawText(medFont, "Time:", WHITE, 25*GRIDSIZE, 13*GRIDSIZE)
    drawText(medFont, str(elapsed), WHITE, 25*GRIDSIZE, 14*GRIDSIZE)
    drawBox(24, 30, 14, 15)

def playMenuSong():
    pygame.mixer.music.load("menu soundtrack.ogg")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops=-1)

def playMainSong():
    pygame.mixer.music.load("tetris theme.ogg")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)

def drawMenu():
    gameWindow.blit(menuBkgd, (0,0))
    drawText(bigFont, "TETRIS", BLACK, 330, 100)
    pygame.draw.rect(gameWindow, BLACK, (250, 200, 300, 40), 2)
    drawText(medFont, "PRESS SPACEBAR TO START", BLACK, 270, 205)
    drawText(medFont, "Press ESC to exit the game.", BLACK, 260, 160)
    
def drawGrid():
    """ Draw horisontal and vertical lines on the game field ONLY!
        Space between the lines is GRIDSIZE.
    """
    for line in range(LEFT, RIGHT+1):
        pygame.draw.line(gameWindow, WHITE, (line*GRIDSIZE, TOP*GRIDSIZE), (line*GRIDSIZE, BOTTOM*GRIDSIZE))
    for line in range(TOP, BOTTOM+1):
        pygame.draw.line(gameWindow, WHITE, (LEFT*GRIDSIZE, line*GRIDSIZE), (RIGHT*GRIDSIZE, line*GRIDSIZE))
        
def drawText(font, text, colour, x, y):
    graphics = font.render(text, 1, colour)
    gameWindow.blit(graphics, (x, y))

def drawBox(x1, x2, y1, y2):
    pygame.draw.line(gameWindow, WHITE, (x1*GRIDSIZE, y1*GRIDSIZE), (x2*GRIDSIZE, y1*GRIDSIZE))
    pygame.draw.line(gameWindow, WHITE, (x1*GRIDSIZE, y2*GRIDSIZE), (x2*GRIDSIZE, y2*GRIDSIZE))
    pygame.draw.line(gameWindow, WHITE, (x1*GRIDSIZE, y1*GRIDSIZE), (x1*GRIDSIZE, y2*GRIDSIZE))
    pygame.draw.line(gameWindow, WHITE, (x2*GRIDSIZE, y1*GRIDSIZE), (x2*GRIDSIZE, y2*GRIDSIZE))
        

#---------------------------------------#
#   Images, Text, Sounds                #
#---------------------------------------#
bigFont = pygame.font.SysFont("Century Gothic", 40)
medFont = pygame.font.SysFont("Century Gothic", 20)
menuBkgd = pygame.image.load("menu.jpg").convert()
mainBkgd = pygame.image.load("bkgd.jpg").convert()
    
#---------------------------------------#
#   main program                        #
#---------------------------------------#
floor = Floor(LEFT, BOTTOM, COLUMNS)
leftWall = Wall(LEFT-1, TOP, ROWS)
rightWall = Wall(RIGHT, TOP, ROWS)
ceiling = Floor(LEFT, TOP, COLUMNS)
clock = pygame.time.Clock()

replaying = True
while replaying:
    score = 0
    level = 1
    pointsToNextLvl = 2000
    endGame = False
    fps = 5                                # FPS stands for Frames Per Second
    shapeNo = randint(1,7)
    nextShapeNo = randint(1, 7)
    shape = Shape(MIDDLE, TOP+1, shapeNo)
    nextShape = Shape(26, 4, nextShapeNo)
    obstacles = Obstacles(LEFT, BOTTOM, 0)    # creates a cluster which holds the blocks of all obstacles
    #-----------------#
    # Starting menu   #
    #-----------------#

    #play menu music
    playMenuSong()

    #draw starting menu
    showMenu = True
    while showMenu:
        drawMenu()
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            showMenu = False
            endGame = True
        if keys[pygame.K_SPACE]:
            showMenu = False  
        else:
            pygame.event.clear()
        pygame.display.update()

    clock.tick(10)
    #stop menu music, load and play main game music        
    pygame.mixer.music.stop()
    playMainSong()

    if endGame:
        replaying = False
        
    # start timing
    BEGIN = time.time()
    referenceTime = BEGIN
        
    inPlay = True                                         
    while inPlay and not endGame:
        elapsed = round(time.time() - referenceTime, 1)
    
        redrawGameWindow()
        clock.tick(fps)
        if not shape.collides(obstacles) and not shape.collides(floor):
            shape.moveDown()
            if shape.collides(obstacles) or shape.collides(floor):
                shape.moveUp()
                obstacles.append(shape)
                shapeNo = nextShapeNo
                shape = Shape(MIDDLE, TOP+1, shapeNo)
                nextShapeNo = randint(1,7)      # and generate a new shape
                nextShape = Shape(26, 4, nextShapeNo) 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inPlay = False
                if event.key == pygame.K_UP:
                    shape.rotateClkwise()
                    if shape.collides(obstacles):
                        shape.rotateCntClkwise()
                    #-----------------------#  
                    if shape.collides(floor) or shape.collides(leftWall) or shape.collides(rightWall):
                        shape.rotateCntClkwise()
                    #-----------------------#
                if event.key == pygame.K_LEFT:
                    shape.moveLeft()
                    if shape.collides(obstacles):
                        shape.moveRight()
                    #-----------------------#  
                    if shape.collides(leftWall):
                        shape.moveRight()
                    #-----------------------#      
                if event.key == pygame.K_RIGHT:
                    shape.moveRight()
                    if shape.collides(obstacles):       # if the shape hits the floor,  
                        shape.moveLeft()              # move it back up
                    #-----------------------#  
                    if shape.collides(rightWall):
                        shape.moveLeft()
                    #-----------------------#
                if event.key == pygame.K_DOWN:
                    shape.moveDown()
                    if shape.collides(floor) or shape.collides(obstacles):       # if the shape hits the floor,  
                        shape.moveUp()              # move it back up,
                        obstacles.append(shape)     # append its blocks to the obstacles,
                        shapeNo = nextShapeNo
                        shape = Shape(MIDDLE, TOP+1, shapeNo)
                        nextShapeNo = randint(1,7)      # and generate a new shape
                        nextShape = Shape(26, 4, nextShapeNo) 
                if event.key == pygame.K_SPACE:
                    while not shape.collides(obstacles) and not shape.collides(floor):
                        shape.moveDown()
                    shape.moveUp()
                    obstacles.append(shape)
                    shapeNo = nextShapeNo
                    shape = Shape(MIDDLE, TOP+1, shapeNo)
                    nextShapeNo = randint(1,7)
                    nextShape = Shape(26, 4, nextShapeNo)
                

    #----------------------------------------------#
    # finding and removing full rows, adding score:                   
        fullRows = obstacles.findFullRows(TOP, BOTTOM, COLUMNS)
        score = score + obstacles.removeFullRows(fullRows)
        level = obstacles.findLevel(score)
        fps = obstacles.findFps(level)
    
    #---------------------------------------#
    # lol game over
        if obstacles.collides(ceiling):
            inPlay = False
    
pygame.quit()
        
        
