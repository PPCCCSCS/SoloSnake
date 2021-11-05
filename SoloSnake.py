# -*- coding: utf8 -*-

"""
SNEK -- placeholder name for snake/solitaire mashup game
"""
import os, sys
from random import randint, choice
import pygame
from pygame.locals import *

pygame.init()

# playing field position and tile size
BX  = BOARDX    = 40
BY  = BOARDY    = 40
TS  = TILESIZE  = 40

# Gameplay area
COLS = COLUMNS  = 20
ROWS            = 20

CLOCKRATE = 1 # refreshes per second. Should be 60 eventually.

WHITE     = 255,255,255
BLACK     = 0,0,0
CYAN      = 0,255,255
YELLOW    = 255,255,0
PURPLE    = 128,0,128
GREEN     = 0,128,0
RED       = 255,0,0
BLUE      = 0,0,255
ORANGE    = 255,165,0

SPADE   = u'\u2660'
CLUB    = u'\u2663'
HEART   = u'\u2665'
DIAMOND = u'\u2666'

SPADES   = ["🂡","🂢","🂣","🂤","🂥","🂦","🂧","🂨","🂩","🂪","🂫","🂭","🂮"]
CLUBS    = ["🃑","🃒","🃓","🃔","🃕","🃖","🃗","🃘","🃙","🃚","🃛","🃝","🃞"]
HEARTS   = ["🂱","🂲","🂳","🂴","🂵","🂶","🂷","🂸","🂹","🂺","🂻","🂽","🂾"]
DIAMONDS = ["🃁","🃂","🃃","🃄","🃅","🃆","🃇","🃈","🃉","🃊","🃋","🃍","🃎"]

# calculate window size
# game board + info display area + Border spacing
WIDTH     = (BOARDX * 3) + (TILESIZE * COLUMNS) + (TS*3)
HEIGHT    = (BOARDY * 2) + (TILESIZE * ROWS)

# Snek Title Top Left Position
STTL       = [TILESIZE*(COLUMNS+1.5),BOARDY]
# Next Title Top Left Position
NTTL       = [int(TILESIZE*(COLUMNS+3.5)),BOARDY*4]
# Next Box Top Left Position
NBTL       = [TILESIZE*(COLUMNS+2),TILESIZE*6]
# Playfield Top Left Position
PFTL       = [BOARDX,BOARDY]

# create a clock for flow control
clock = pygame.time.Clock()

# set up font rendering (for title)
pygame.init()
pygame.font.init()

# c:\windows\fonts
f0 = pygame.font.Font("ARIALNB.TTF",128)
f1 = pygame.font.Font("ARIALNB.TTF",64)
f2 = pygame.font.Font("ARIALNB.TTF",32)
f3 = pygame.font.Font("ARIALNB.TTF",24)

TITLE       = "SNEK"
textTITLE   = "SNEK"
dispTITLE   = f1.render(textTITLE, True, PURPLE)
rectTITLE = dispTITLE.get_rect()
rectTITLE.topleft=STTL

dispSPADE = f3.render(SPADE, True, RED)
rectSPADE = dispSPADE.get_rect()
rectSPADE.topleft=[TS*(COLUMNS+1)+ 20,TS*3]

dispCLUB = f3.render(CLUB, True, RED)
rectCLUB = dispCLUB.get_rect()
rectCLUB.topleft=[TS*(COLUMNS+2)+ 25,TS*3]

dispHEART = f3.render(HEART, True, RED)
rectHEART = dispHEART.get_rect()
rectHEART.topleft=[TS*(COLUMNS+3)+ 30,TS*3]

dispDIAMOND = f3.render(DIAMOND, True, RED)
rectDIAMOND = dispDIAMOND.get_rect()
rectDIAMOND.topleft=[TS*(COLUMNS+4)+ 35,TS*3]

# set up the display area
screen = pygame.display.set_mode((WIDTH,HEIGHT))
background = pygame.Surface((WIDTH,HEIGHT))

keys = pygame.key.get_pressed()
clock = pygame.time.Clock()

'''
Game board defaults to 20x20. Each position should be empty, initially,
but we'll populate random positions with cards from the deck after the
Snek is instantiated and set loose. Or slightly before; choices.
'''
class Board:
    def __init__(self,size=(COLS,ROWS)):
        self.field = []
        self.deck = Deck()
        for y in range(size[1]):
            temp = []
            for x in range(size[0]):
                temp.append('')
            self.field.append(temp)
    # pick a random card from the deck, move it to the field
    def dealOne(self):
        pass

'''
Deck is just a list of (initially) all possible playing cards. Remove
Cards from the Deck whenver they are added to the game board (there
should be no duplicates in play!)
'''
class Deck:
    def __init__(self):
        self.cards = []
        for suit in (SPADE,CLUB,HEART,DIAMOND):
            for rank in ('A','2','3','4','5','6','7','8','9','10','J','Q','K'):
                self.cards.append(Card([-1,-1],suit,rank))                

'''
Snek is essentially a list of cards (and suit segments) that 'moves'
through the positions on the Board, while maintaining a history of the
places where it's been. Individual Cards collected by the Snek are
added to its body, and move from location to location in the Snek's
history as the game clock progresses. Only the head of the Snek is
responsible for detecting collisions, but the Snek must test for its
own segments, the borders of the game board, and any of the scattered
Cards that it hasn't collected yet. Colliding with itself or the
borders is an instant game over, but when the Snek collides with a
card, an additional test must be performed to determine if that card
is a valid solitaire move; if yes, the card is added to the Snek's
queue, and gameplay continues. If no, well, game-over man.
'''
class Snek:
    def __init__(self,pos=[0,0],vel=[0,-1],length=7):
        self.pos = pos
        self.vel = vel
        self.queue = []
        self.length = length
        self.past = []

    def addCard(self,suit,rank):
        self.past.append(Card(len(self.queue),suit,rank))

    # Decisions to be made here
    def testCard(self,card):
        pass
    
'''
class Pile:
'''    

class Card:
    def __init__(self,pos=[0,0],suit=CLUB,rank="A"):
        self.pos = pos
        self.suit = suit
        self.rank = rank
        self.suit_disp = None
        self.suit_rect = None
        self.rank_disp = None
        self.rank_rect = None
        self.sxoff = 0
        self.syoff = 0
        self.rxoff = 0
        self.ryoff = 0

        if self.suit == CLUB:
            self.suit_color = BLACK
            self.rank_color = BLACK
            self.sxoff = int(TS*.70)
            self.syoff = int(TS*.65)
            self.rxoff = int(TS*.30)
            self.ryoff = int(TS*.35)
        elif self.suit == SPADE:
            self.suit_color = BLACK
            self.rank_color = BLACK
            self.sxoff = int(TS*.75)
            self.syoff = int(TS*.65)
            self.rxoff = int(TS*.30)
            self.ryoff = int(TS*.35)
        elif self.suit == DIAMOND:
            self.suit_color = RED
            self.rank_color = BLACK
            self.sxoff = int(TS*.75)
            self.syoff = int(TS*.65)
            self.rxoff = int(TS*.30)
            self.ryoff = int(TS*.35)
        elif self.suit == HEART:
            self.suit_color = RED
            self.rank_color = BLACK
            self.sxoff = int(TS*.70)
            self.syoff = int(TS*.65)
            self.rxoff = int(TS*.30)
            self.ryoff = int(TS*.35)
            

        self.rank_disp = f2.render(self.rank, True, self.rank_color)
        self.rank_rect = self.rank_disp.get_rect()
        self.rank_rect.center = [self.pos[0]+self.rxoff,self.pos[1]+self.ryoff]

        self.suit_disp = f2.render(self.suit, True, self.suit_color)
        self.suit_rect = self.suit_disp.get_rect()
        self.suit_rect.center = [self.pos[0]+self.sxoff,self.pos[1]+self.syoff]

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.pos[0],self.pos[1],TS,TS), border_radius=int(TS*.2))
        screen.blit(self.suit_disp, self.suit_rect)
        screen.blit(self.rank_disp, self.rank_rect)
        pygame.display.flip()

def main():

    # draw playfield border
    pygame.draw.rect(background, (255,255,0), (BX, BY, (TS * COLUMNS), (TS * ROWS)), 2) 
    pygame.draw.rect(background, (255,255,0), (TS*(COLUMNS+1)+ 5,TS*3 ,TS,TS*14),2)
    pygame.draw.rect(background, (255,255,0), (TS*(COLUMNS+2)+10,TS*3 ,TS,TS*14),2)
    pygame.draw.rect(background, (255,255,0), (TS*(COLUMNS+3)+15,TS*3 ,TS,TS*14),2)
    pygame.draw.rect(background, (255,255,0), (TS*(COLUMNS+4)+20,TS*3 ,TS,TS*14),2)

    test_heart   = Card([200,200],HEART,"A")
    test_diamond = Card([250,200],DIAMOND,"2")
    test_club    = Card([300,200],CLUB,"10")
    test_spade   = Card([350,200],SPADE,"4")

    while(1):

        screen.blit(background,  (0,0))
        screen.blit(dispTITLE,   rectTITLE)
        screen.blit(dispSPADE,   rectSPADE)
        screen.blit(dispCLUB,    rectCLUB)
        screen.blit(dispHEART,   rectHEART)
        screen.blit(dispDIAMOND, rectDIAMOND)

        test_heart.draw()
        test_diamond.draw()
        test_club.draw()
        test_spade.draw()
        #pygame.draw.circle(screen, RED, [400,400], 20)

        # update everything
        pygame.display.flip()
        clock.tick(CLOCKRATE)
        
        
if __name__ == "__main__":
    main()
