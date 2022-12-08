import pygame
from pygame.locals import *

# playing field position and tile size
BX  = BOARDX    = 40
BY  = BOARDY    = 40
TS  = TILESIZE  = 40

# Gameplay area
COLS = COLUMNS  = 20
ROWS            = 20

CLOCKRATE = 60 # refreshes per second. Should be 60 eventually.
WALK      = int(4*CLOCKRATE)
RUN       = int(8*CLOCKRATE)
SHUFFLE   = int(2*CLOCKRATE)
CRAWL     = int(CLOCKRATE)
SPEED     = SHUFFLE

WHITE     = 255,255,255
BLACK     = 0,0,0
CYAN      = 0,255,255
YELLOW    = 255,255,0
PURPLE    = 128,0,128
GREEN     = 0,128,0
RED       = 255,0,0
BLUE      = 0,0,255
ORANGE    = 255,165,0
GREY      = 127,127,127

RANKS     = ('','A','2','3','4','5','6','7','8','9','10','J','Q','K')
SUITS     = (u'\u2660',u'\u2663',u'\u2665',u'\u2666')

HSPADE   = u'\u2664'
HCLUB    = u'\u2667'
HHEART   = u'\u2661'
HDIAMOND = u'\u2662'
SPADE    = u'\u2660'
CLUB     = u'\u2663'
HEART    = u'\u2665'
DIAMOND  = u'\u2666'

# Too hard to read during gameplay, but may be useful elsewhere
SPADES   = ["🂡","🂢","🂣","🂤","🂥","🂦","🂧","🂨","🂩","🂪","🂫","🂭","🂮"]
CLUBS    = ["🃑","🃒","🃓","🃔","🃕","🃖","🃗","🃘","🃙","🃚","🃛","🃝","🃞"]
HEARTS   = ["🂱","🂲","🂳","🂴","🂵","🂶","🂷","🂸","🂹","🂺","🂻","🂽","🂾"]
DIAMONDS = ["🃁","🃂","🃃","🃄","🃅","🃆","🃇","🃈","🃉","🃊","🃋","🃍","🃎"]

# calculate window size
# game board + info display area + Border spacing
WIDTH     = (TILESIZE * COLUMNS) + (BOARDX * 7) + 33
HEIGHT    = (TILESIZE * ROWS)+6

# Snek Title Top Left Position
STTL       = [TILESIZE*(COLUMNS+1.5),BOARDY]
# Next Title Top Left Position
NTTL       = [int(TILESIZE*(COLUMNS+3.5)),BOARDY*4]
# Next Box Top Left Position
NBTL       = [TILESIZE*(COLUMNS+2),TILESIZE*6]
# Playfield Top Left Position
PFTL       = [BOARDX,BOARDY]
# Snek start position
START      = [10,10]

# set up font rendering (for title)
pygame.init()
pygame.font.init()

# create a clock for flow control
clock = pygame.time.Clock()

# c:\windows\fonts
f0 = pygame.font.Font("ARIALNB.TTF",128)
f1 = pygame.font.Font("ARIALNB.TTF",64)
f2 = pygame.font.Font("ARIALNB.TTF",32)
f3 = pygame.font.Font("ARIALNB.TTF",24)

TITLE       = "SOLO SNAKE"
textTITLE   = "SOLO SNAKE"
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
