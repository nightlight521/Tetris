#########################################
# File Name: TetrisClasses.py
# Description: This file contains classes for Tetris Game
# Author: ICS2OG
# Date: 28/11/2018
#########################################
import pygame
import time

BLACK     = (  0,  0,  0)                       
RED       = (255,  0,  0)                     
GREEN     = (  0,255,  0)                     
BLUE      = (  0,  0,255)                     
ORANGE    = (255,127,  0)               
CYAN      = (  0,183,235)                   
MAGENTA   = (255,  0,255)                   
YELLOW    = (255,255,  0)
WHITE     = (255,255,255) 
COLOURS   = ( BLACK,  RED,  GREEN,  BLUE,  ORANGE,  CYAN,  MAGENTA,  YELLOW,  WHITE )
CLR_names = ("black","red","green","blue","orange","cyan","magenta","yellow","white")
FIGURES   = (  None , 'Z' ,  'S'  ,  'J' ,  'L'   ,  'I' ,   'T'   ,   'O'  , None  )

#---------------------------------------#
class Block(object):                    
    """ A square - basic building block
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        self.col = col                  
        self.row = row                  
        self.clr = clr

    def __str__(self):                  
        return "("+str(self.col)+","+str(self.row)+") "+CLR_names[self.clr]

    def draw(self, surface, gridsize=20):                     
        x = self.col * gridsize        
        y = self.row * gridsize
        CLR = COLOURS[self.clr]
        pygame.draw.rect(surface,CLR,(x,y,gridsize,gridsize), 0)
        pygame.draw.rect(surface,WHITE,(x,y,gridsize+1,gridsize+1), 1)

    def moveLeft(self):                
        self.col = self.col - 1    
        
    def moveRight(self):               
        self.col = self.col + 1   
        
    def moveDown(self):                
        self.row = self.row + 1   
        
    def moveUp(self):                  
        self.row = self.row - 1 

#---------------------------------------#
class Cluster(object):
    """ Collection of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        self.col = col                    
        self.row = row                   
        self.clr = 0
        self.blocks = [Block()]*blocksNo
        self._colOffsets = [0]*blocksNo
        self._rowOffsets = [0]*blocksNo

    def _update(self):
        for i in range(len(self.blocks)):
            blockCOL = self.col+self._colOffsets[i]
            blockROW = self.row+self._rowOffsets[i]
            blockCLR = self.clr
            self.blocks[i]= Block(blockCOL, blockROW, blockCLR)

    def draw(self, surface, gridsize):                     
        for block in self.blocks:
            block.draw(surface, gridsize)

    def collides(self, other):
        """ Compare each block from a cluster to all blocks from another cluster.
            Return True only if there is a location conflict.
        """
        for block in self.blocks:
            for obstacle in other.blocks:
                if block.col == obstacle.col and block.row == obstacle.row:
                    return True
        return False
    def append(self, other):            
        """ Append all blocks from another cluster to this one."""
        for block in other.blocks:
            self.blocks.append(block)
#---------------------------------------#
class Obstacles(Cluster):
    """ Collection of blocks on the playing field, left from previous shapes."""        
    def __init__(self, col = 0, row = 0, blocksNo = 0): # initially the playing field is empty 
        Cluster.__init__(self, col, row, blocksNo)
        self._tetris = False

    def show(self):
        for block in self.blocks:
            print block
            
    def findFullRows(self, top, bottom, columns):
        fullRows = []
        rows = []
        for block in self.blocks:                       
            rows.append(block.row)                      # make a list with only the row numbers of all blocks
            
        for row in range(top, bottom):                  # starting from the top (row 0), and down to the bottom
            if rows.count(row) == columns:              # if the number of blocks with a certain row number
                fullRows.append(row)                    # equals to the number of columns -> the row is full
        return fullRows                                 # return a list with the row numbers of the full rows

    def removeFullRows(self, fullRows):
        score = 0
        if len(fullRows) < 4:
            for row in fullRows:
                score = score + 100
        if len(fullRows) == 4 and self._tetris:
            score = score + 1200
            self._tetris = False
        elif len(fullRows) == 4:
            score = score + 800
            self._tetris = True
        for row in fullRows:                            # target full rows, STARTING FROM THE TOP (fullRows are in order)
            for i in reversed(range(len(self.blocks))): # traverse all blocks in REVERSE ORDER,
                                                        # so when popping them the index doesn't go out of range !!!
                if self.blocks[i].row == row:
                    self.blocks.pop(i)                  # remove each block that is on a full row
                elif self.blocks[i].row < row:
                    self.blocks[i].moveDown()           # move down each block that is above a full row
        return score

    def findLevel(self, score):
        if score < 1000:
            level = 1 
        if score >= 1000 and score < 2000:
            level = 2  
        if score >= 2000 and score < 3000:
            level = 3
        if score >= 3000 and score < 4000:
            level = 4
        if score >= 4000:
            level = 5
        return level
            
    def findFps(self, level):
        if level == 1:
            fps = 5
        if level == 2:
            fps = 10
        if level == 3:
            fps = 15
        if level == 4:
            fps = 20
        if level == 5:
            fps = 25
        return fps


#---------------------------------------#
class Shape(Cluster):                     
    """ A tetromino in one of the shapes: Z,S,J,L,I,T,O; consists of 4 x Block() objects
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour        rotate clockwise/counterclockwise
                * figure/shape is defined by the colour
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        Cluster.__init__(self, col, row, blocksNo = 4)
        self.clr = clr
        self._rot = 1
        self._rotate()
        
    def __str__(self):                  
        return FIGURES[self.clr]+" ("+str(self.col)+","+str(self.row)+") "+CLR_names[self.clr]

    def _rotate(self):
        if self.clr == 1:    #           (default rotation)    
                             #   o             o o                o              
                             # o x               x o            x o          o x
                             # o                                o              o o
            _colOffsets = [[-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0], [ 1, 0, 0,-1]]
            _rowOffsets = [[ 1, 0, 0,-1], [-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0]]        
        elif self.clr == 2:  #
                             # o                 o o           o              
                             # o x             o x             x o             x o
                             #   o                               o           o o
            _colOffsets = [[-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0], [-1, 0, 0, 1]]
            _rowOffsets = [[-1, 0, 0, 1], [-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0]]
        elif self.clr == 3:  # 
                             #   o             o                o o              
                             #   x             o x o            x           o x o
                             # o o                              o               o
            _colOffsets = [[-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0], [ 1, 1, 0,-1]]
            _rowOffsets = [[ 1, 1, 0,-1], [-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0]]            
        elif self.clr == 4:  #  
                             # o o                o             o              
                             #   x            o x o             x           o x o
                             #   o                              o o         o
            _colOffsets = [[-1, 0, 0, 0], [ 1, 1, 0,-1], [ 1, 0, 0, 0], [-1,-1, 0, 1]]
            _rowOffsets = [[-1,-1, 0, 1], [-1, 0, 0, 0], [ 1, 1, 0,-1], [ 1, 0, 0, 0]]
        elif self.clr == 5:  #   o                              o
                             #   o                              x              
                             #   x            o x o o           o          o o x o
                             #   o                              o              
            _colOffsets = [[ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0], [-2,-1, 0, 1]]
            _rowOffsets = [[-2,-1, 0, 1], [ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0]]            
        elif self.clr == 6:  #
                             #   o              o                o              
                             # o x            o x o              x o         o x o
                             #   o                               o             o 
            _colOffsets = [[ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0], [ 1, 0, 0,-1]]
            _rowOffsets = [[ 1, 0, 0,-1], [ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0]]
        elif self.clr == 7:  # 
                             # o o            o o               o o          o o
                             # o x            o x               o x          o x
                             # 
            _colOffsets = [[-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0]]
            _rowOffsets = [[ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1]]
        self._colOffsets = _colOffsets[self._rot]
        self._rowOffsets = _rowOffsets[self._rot]
        self._update()

    def moveLeft(self):                
        self.col = self.col - 1                   
        self._update()
        
    def moveRight(self):               
        self.col = self.col + 1                   
        self._update()
        
    def moveDown(self):                
        self.row = self.row + 1                   
        self._update()
        
    def moveUp(self):                  
        self.row = self.row - 1                   
        self._update()

    def rotateClkwise(self):
        self._rot = (self._rot + 1)%4  
        self._rotate()

    def rotateCntClkwise(self):
        self._rot = (self._rot - 1)%4  
        self._rotate()

#---------------------------------------#
class Floor(Cluster):
    """ Horizontal line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._colOffsets[i] = i
        self._update()           
            
#---------------------------------------#
class Wall(Cluster):
    """ Vertical line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._rowOffsets[i] = i
        self._update()
