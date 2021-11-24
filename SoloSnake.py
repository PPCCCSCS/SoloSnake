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

CLOCKRATE = 60 # refreshes per second. Should be 60 eventually.
WALK      = int(CLOCKRATE)
RUN       = int(2*CLOCKRATE)
CRAWL     = int(CLOCKRATE/2)
SPEED     = RUN*2

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

SPADE   = u'\u2660'
CLUB    = u'\u2663'
HEART   = u'\u2665'
DIAMOND = u'\u2666'

# Too hard to read during gameplay, but may be useful elsewhere
SPADES   = ["🂡","🂢","🂣","🂤","🂥","🂦","🂧","🂨","🂩","🂪","🂫","🂭","🂮"]
CLUBS    = ["🃑","🃒","🃓","🃔","🃕","🃖","🃗","🃘","🃙","🃚","🃛","🃝","🃞"]
HEARTS   = ["🂱","🂲","🂳","🂴","🂵","🂶","🂷","🂸","🂹","🂺","🂻","🂽","🂾"]
DIAMONDS = ["🃁","🃂","🃃","🃄","🃅","🃆","🃇","🃈","🃉","🃊","🃋","🃍","🃎"]

# calculate window size
# game board + info display area + Border spacing
WIDTH     = (BOARDX * 4) + (TILESIZE * COLUMNS) + 6
HEIGHT    = (TILESIZE * ROWS)+6

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

        # draw playfield border
        pygame.draw.rect(background, (255,255,0), (1, 1, (TS * COLUMNS)+3, (TS * ROWS)+3), 2)

        foundation_spade = Foundation(SPADE)
        foundation_spade.draw([COLS,6])
        foundation_club = Foundation(CLUB)
        foundation_club.draw([COLS+1,6])
        foundation_heart = Foundation(HEART)
        foundation_heart.draw([COLS+2,6])
        foundation_diamond = Foundation(DIAMOND)
        foundation_diamond.draw([COLS+3,6])

        screen.blit(background,  (0,0))
        screen.blit(dispTITLE,   rectTITLE)

    '''        
    Given just a card, placeCard picks a random location on the board
    Given a position, placeCard will test that location for validity
    then place the card if empty, swap cards if another card is present
    or ?do nothing? if part of the snake is there
    '''
    def placeCard(card,pos=[0,0]):
        pass

    def tileContains(self,pos=[0,0]):
        return self.field[pos[0]][pos[1]]
        

'''
Deck is just a list of (initially) all possible playing cards. Remove
Cards from the Deck whenver they are added to the game board (there
should be no duplicates in play!)
'''
class Deck:
    def __init__(self):
        self.cards = []
        for idx, suit in enumerate(SUITS):
            for idy, rank in enumerate(RANKS):
                self.cards.append(Card([(idx+1)*TS,(idy+1)*TS],suit,rank))
    '''
    Mostly just for debugging purposes
    '''
    def printAll(self):
        for card in self.cards[::-1]:
            card.draw()

    '''
    Take a random card from the Deck if not shuffled, or the top
    card if the Deck has been shuffled in advance.
    '''
    def dealOne(self):
        pass

'''
Foundations are the four piles where cards go, in order from least
to greatest, after they are removed from one of the seven piles in
play in Klondike, or one of the seven segments of the snake in this
game. The player wins when all of the cards from the Deck have been
transferred to the appropriate Foundation.
'''
class Foundation:
    def __init__(self,suit):
        self.cards = [Card(suit='')]

    def draw(self,pos=[1,1]):
        pygame.draw.rect(background, (255,255,0), (TS*pos[0]+4,TS*pos[1]+4 ,TS,TS*14),2)

    def refresh(self):
        for i, card in enumerate(self.cards):
            card.move(self.pos[0],self.pos[1]+(TS*i))
            card.draw()
            pygame.display.flip()

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
    def __init__(self,pos=[0,0],vel=[0,WALK],length=7):
        self.pos = pos
        self.vel = vel
        self.queue = [Card(self.pos,DIAMOND,"00"),
                      Card(self.pos,"","1"),
                      Card(self.pos,"","2"),
                      Card(self.pos,"","3"),
                      Card(self.pos,"","4"),
                      Card(self.pos,"","5"),
                      Card(self.pos,"","6"),
                      Card(self.pos,"","7")]
        self.pile = []
        '''
        for suit in SUITS:
            for rank in RANKS:
                self.queue.append(Card(self.pos,suit,rank))
        '''
        self.length = len(self.queue)
        
    '''
    NOM NOM NOM
    '''
    def addCard(self,suit,rank):
        ### Simple append won't work;
        #insert at top of relevant segment
        self.queue.append(Card(self.pos,suit,rank))

    # Decisions to be made here
    def testCard(self,card):
        pass

    def draw(self,gameover=False):
        
        for i,c in enumerate(self.queue):
            if c.isNextTile():
               if i < len(self.queue)-1:
                   self.queue[i+1].nextMove =  c.thisMove
        for c in reversed(self.queue):
            c.draw(gameover)
            c.move()


    def steer(self,way):

        # Only change directions if new direction is 90 degrees from previous,
        # or if the snake isn't moving yet
        if (way[0] == 0 and self.queue[0].thisMove[0] != 0) or \
           (way[1] == 0 and self.queue[1].thisMove[1] != 0) or \
           (self.queue[0].thisMove == [0,0]):
            self.queue[0].nextMove = way

    def isInBounds(self):
        if 0 <= self.queue[0].pos[0] < TS*(COLS-1)+2 and 0 <= self.queue[0].pos[1] < TS*(ROWS-1)+2:
            return True
        else:
            return False

    def headPos(self):
        return [ int(self.queue[0].pos[0]/TS), int(self.queue[0].pos[1]/TS)]

    def tailPos(self):
        return [ int(self.queue[-1].pos[0]/TS),int(self.queue[-1].pos[1]/TS)]

    
'''
Cards have suits, ranks, and positions. Everything else included
here is for layout purposes.
'''
class Card:
    def __init__(self,pos=[0,0],suit=CLUB,rank="",bg=WHITE):
        self.pos = [pos[0]*TS,pos[1]*TS]
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
        self.bgcol = bg
        self.thisMove = [0,0]
        self.nextMove = [0,0]
        
    def move(self):
        if self.isNextTile():
            self.thisMove = self.nextMove
        self.pos = [self.pos[0]+self.thisMove[0]/CLOCKRATE,
                    self.pos[1]+self.thisMove[1]/CLOCKRATE]

    def isNextTile(self):
        if self.pos[0]%TS == 0 and self.pos[1]%TS == 0:
            return True
        else:
            return False

    def draw(self,gameover=False):
        def tset(sc,rc,sx,sy,rx,ry,bg=WHITE):
            self.suit_color = sc
            self.rank_color = rc
            self.sxoff = int(TS*sx)+4
            self.syoff = int(TS*sy)+4
            self.rxoff = int(TS*rx)+4
            self.ryoff = int(TS*ry)+4
            self.bgcol = bg

        if self.rank == "":
            if not gameover:
                tset(GREY,GREY,.5,.38,.5,.5)
            else:
                tset(GREY,GREY,.5,.38,.5,.5,GREY)
        elif self.suit == "":
            if not gameover:
                tset(RED,RED,.5,.5,.5,.5,GREEN)
            else:
                tset(GREY,GREY,.5,.5,.5,.5,GREY)
        elif self.rank == "00":
            if not gameover:
                tset(RED,WHITE,.5,.65,.55,.35,GREEN)
            else:
                tset(RED,WHITE,.5,.65,.55,.35,GREY)
        elif self.suit == CLUB:
            if not gameover:
                tset(BLACK,BLACK,.7,.65,.3,.35)
            else:
                tset(GREY,GREY,.7,.65,.3,.35,GREY)
        elif self.suit == SPADE:
            if not gameover:
                tset(BLACK,BLACK,.75,.65,.3,.35)
            else:
                tset(GREY,GREY,.75,.65,.3,.35,GREY)
        elif self.suit == DIAMOND:
            if not gameover:
                tset(RED,BLACK,.75,.65,.3,.35)
            else:
                tset(GREY,GREY,.75,.65,.3,.35,GREY)
        elif self.suit == HEART:
            if not gameover:
                tset(RED,BLACK,.7,.65,.3,.35)
            else:
                tset(GREY,GREY,.7,.65,.3,.35,GREY)
            
        self.rank_disp = f2.render(self.rank, True, self.rank_color)
        self.rank_rect = self.rank_disp.get_rect()
        self.rank_rect.center = [self.pos[0]+self.rxoff,self.pos[1]+self.ryoff]

        if self.rank == "":
            self.suit_disp = f1.render(self.suit, True, self.suit_color)
        elif self.rank == "00":
            if gameover == False:
                self.suit_disp = f3.render(self.suit, True, self.suit_color)
                self.rank_disp = f3.render(self.rank, True, self.rank_color)
            else:
                self.suit_disp = f3.render("-", True, WHITE)
                self.rank_disp = f3.render("XX", True, BLACK)
        else:
            self.suit_disp = f2.render(self.suit, True, self.suit_color)
            
        self.suit_rect = self.suit_disp.get_rect()
        self.suit_rect.center = [self.pos[0]+self.sxoff,self.pos[1]+self.syoff]

        pygame.draw.rect(screen, self.bgcol, (self.pos[0]+4,self.pos[1]+4,TS-2,TS-2), border_radius=int(TS*.2))
        screen.blit(self.suit_disp, self.suit_rect)
        screen.blit(self.rank_disp, self.rank_rect)

def main():

    gb = Board()
    sn = Snek([10,10])
    #td = Deck()

    gameover = False

    while not gameover:

        for event in pygame.event.get():

            if event.type == pygame.KEYUP:
                if event.key == K_ESCAPE:
                    sys.exit()

                if event.key == K_LEFT:
                    sn.steer([-SPEED,0])
                if event.key == K_RIGHT:
                    sn.steer([SPEED,0])
                if event.key == K_UP:
                    sn.steer([0,-SPEED])
                if event.key == K_DOWN:
                    sn.steer([0,SPEED])

        #td.printAll()
        screen.blit(background,  (0,0))
        sn.draw()

        if not sn.isInBounds():
            gameover = True

        hp = sn.headPos()
        tp = sn.tailPos()
        # After the snake starts moving, put an S in
        # the gameboard's field each time the snake
        # moves to a new tile. If the Snake moves into
        # a tile with an S; game over!
        #
        # Will have to remove the Ss after the tail
        # of the snake leaves a square though.
        if sn.queue[0].thisMove != [0,0]:
            if sn.queue[0].isNextTile():
                if gb.tileContains(hp) == "S":
                    gameover = True
                gb.field[hp[0]][hp[1]] = "S"
                gb.field[tp[0]][tp[1]] = ""

        # update everything
        pygame.display.flip()
        clock.tick(CLOCKRATE)

    print("GAME OVER")
    screen.blit(background,  (0,0))
    sn.draw(True)
    pygame.display.flip()
    sys.exit()
        
if __name__ == "__main__":
    main()
