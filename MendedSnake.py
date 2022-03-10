# -*- coding: utf8 -*-

"""
SNEK -- placeholder name for snake/solitaire mashup game
"""
import os, sys
from random import randint, choice, shuffle
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

RANKS     = ('A','2','3','4','5','6','7','8','9','10','J','Q','K')
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
# Snek start position
START      = [10,10]

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
        self.foundations = [Foundation(SPADE,0),Foundation(CLUB,1),Foundation(HEART,2),Foundation(DIAMOND,3)]
        self.dealtCards = []
        self.snake = Snek([COLS//2,ROWS//2])

        for y in range(size[1]):
            temp = []
            for x in range(size[0]):
                temp.append('')
            self.field.append(temp)

        # draw playfield border
        pygame.draw.rect(background, (255,255,0), (1, 1, (TS * COLUMNS)+3, (TS * ROWS)+3), 2)

        for i in self.foundations:
            i.draw()
                
        #foundation_diamond = Foundation(DIAMOND)
        #foundation_diamond.draw()

        screen.blit(background,  (0,0))
        screen.blit(dispTITLE,   rectTITLE)

    def showTrail(self):
        for x,line in enumerate(self.field):
            for y,tile in enumerate(line):
                if tile == "S":
                    temp = f3.render("*", True, RED)
                    trec = temp.get_rect()
                    trec.topleft=[TS*x+15,TS*y+15]
                    screen.blit(temp,trec)
                else:
                    temp = f3.render("_", True, GREY)
                    trec = temp.get_rect()
                    trec.topleft=[TS*x+15,TS*y+15]
                    screen.blit(temp,trec)
                    

    '''        
    Given just a card, placeCard picks a random location on the board
    Given a position, placeCard will test that location for validity
    then place the card if empty, swap cards if another card is present
    or ?do nothing? if part of the snake is there
    '''
    def placeCard(self,pos=[0,0]):
        placed = False
        
        while placed == False:
            x = randint(0,COLS-1)
            y = randint(0,ROWS-1)

            if self.field[x][y] == '':
                tcard = self.deck.cards.pop()
                tcard.setPos([x,y])
                self.field[x][y] = tcard
                self.dealtCards.append(tcard)
                placed = True
        
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
                self.cards.append(Card([(idx+1),(idy+1)],suit,rank))
        shuffle(self.cards)
    '''
    Mostly just for debugging purposes
    '''
    def printAll(self,full=False):
        for card in self.cards[::-1]:
            if full == False:
                print(card)
            else:
                print([card])

    '''
    Take a random card from the Deck if not shuffled, or the top
    card if the Deck has been shuffled in advance.
    '''
    def dealOne(self):
        if len(self.cards) > 0:
            print(len(self.cards))
            try:
                return self.cards.pop(randint(0,len(self.cards)-1))
            except:
                print("What?",len(self.cards))
        else:
            return Card(suit="",rank="")

'''
Foundations are the four piles where cards go, in order from least
to greatest, after they are removed from one of the seven piles in
play in Klondike, or one of the seven segments of the snake in this
game. The player wins when all of the cards from the Deck have been
transferred to the appropriate Foundation.
'''
class Foundation:
    def __init__(self,suit,column=0):
        self.cards = [Card(suit='')]
        self.column = column

    def draw(self):
        pygame.draw.rect(background, (255,255,0), (TS*(COLS+self.column)+4,TS*6+4 ,TS,TS*14),2)

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
        self.queue = [Card(self.pos,"v","00"),
                      Card(self.pos,"","0"),
                      Card(self.pos,"","1"),
                      Card(self.pos,"","2"),
                      Card(self.pos,"","3"),
                      Card(self.pos,"","4"),
                      Card(self.pos,"","5"),
                      Card(self.pos,"","6")]
        self.hitboxes = {str([int(self.queue[0].pos[0]),int(self.queue[0].pos[1])]):len(self.queue)}
        self.pile = []
        '''
        for suit in SUITS:
            for rank in RANKS:
                self.queue.append(Card(self.pos,suit,rank))
        '''
        #self.length = len(self.queue)
        
    '''
    NOM NOM NOM
    '''
    def addCard(self,card):

        success = False

        #scan queue for first match    
        index = 0
        print(self.queue[index])
        while index < len(self.queue) and not self.queue[index].testFit(card):
                index = index + 1
        if index < len(self.queue)-1:
            #insert card before correct segment
            card.pos = self.queue[index].pos
            card.thisMove = self.queue[index].thisMove
            card.nextMove = self.queue[index-2].nextMove
            self.queue.insert(index,card)
            #shift position of remaining segments back one
            while index < len(self.queue)-1:
                self.queue[index].pos = self.queue[index+1].pos
                self.queue[index].thisMove = self.queue[index+1].thisMove
                self.queue[index].nextMove = self.queue[index+1].nextMove
                        
                index = index + 1

            success = True
            
            # without this line, tail gets wobbly, board doesn't get cleaned up
            # with this line, tail occasionally gets orphaned -- missing what?
            self.queue[-1].thisMove = [0,0]
            if self.queue[-2].isNextTile():
                self.queue[-1].nextMove = self.queue[-2].thisMove

        return success
        
    def addHitbox(self):

        del_list = []
        
        for hb in self.hitboxes:
            if self.hitboxes[hb] > 0:
                self.hitboxes[hb] -= 1
            else:
                del_list.append(hb)

        for dhb in del_list:
            del self.hitboxes[dhb]
            
        self.hitboxes[str([int(self.queue[0].pos[0]),int(self.queue[0].pos[1])])] = len(self.queue)


        
    def draw(self,gameover=False):
        
        for i,c in enumerate(self.queue):
            if self.queue[0].isNextTile():
                if i < len(self.queue)-1:
                    self.queue[i+1].nextMove =  c.thisMove
                    if self.queue[i+1].thisMove == c.thisMove:
                        if self.queue[i+1].thisMove[0] != 0:
                            self.queue[i+1].pos[1] = c.pos[1]
                        else:
                            self.queue[i+1].pos[0] = c.pos[0]
                        
        for c in reversed(self.queue):
            c.draw(gameover)
            c.move(self.atNextTile())

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

    def atNextTile(self):
        if self.queue[0].isNextTile():
            return True
        else:
            return False


    
'''
Cards have suits, ranks, and positions. Everything else included
here is for layout purposes.
'''
class Card:
    def __init__(self,pos=[0,0],suit=CLUB,rank="",bg=WHITE):
        self.pos = [pos[0]*TS,pos[1]*TS]
        self.tile = [pos[0],pos[1]]
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

    def __str__(self):
        return self.suit + self.rank

    def __repr__(self):
        return self.suit+self.rank+"@"+"X:"+str(int(self.pos[0]/TS))+",Y:"+str(int(self.pos[1]/TS))

    def testFit(self,card):
        if self.suit == SPADE or self.suit == CLUB:
            if card.suit == HEART or card.suit == DIAMOND:
                if card.rank == RANKS[RANKS.index(self.rank)-1]:
                    print(card.rank)
                    return True
                else:
                    return False
        elif self.suit == HEART or self.suit == DIAMOND:
            if card.suit == SPADE or card.suit == CLUB:         
                if card.rank == RANKS[RANKS.index(self.rank)-1]:
                    print(card.rank)
                    return True
                else:
                    return False
        #If the calling card is an empty pile
        elif self.suit == "" and self.rank in ["0","1","2","3","4","5","6"]:
            self.rank = self.rank + "*"
            #self.rank = " "+self.rank+" "
            return True
        else:
            return False

    def setPos(self,pos=[0,0]):
        self.pos = [pos[0]*TS,pos[1]*TS]
        
    def move(self,is_next_tile=False):
        if is_next_tile:
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
    sn = gb.snake

    #gb.deck.printAll(True)
    
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

        if len(gb.deck.cards) > 0 and len(gb.dealtCards) < 10:
            gb.placeCard()

        for dealt in gb.dealtCards:
            dealt.draw()

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
        if sn.queue[1].thisMove != [0,0]:
            if sn.queue[0].isNextTile():
                
                test_me = gb.tileContains(hp)
                hp_key = str([hp[0]*TS,hp[1]*TS])

                if hp_key in sn.hitboxes and sn.hitboxes[hp_key] != len(sn.queue):
                    gameover = True
                elif type(test_me) == Card:
                    sn.addCard(test_me)
                    gb.dealtCards.remove(test_me)
                    gb.field[hp[0]][hp[1]] = ''
                # Only add a new hitbox for the snake head after testing to be
                # sur it didn't collide with itself at that same location
                sn.addHitbox()    
                
        # update everything
        gb.showTrail()
        pygame.display.flip()
        clock.tick(CLOCKRATE)

    print("GAME OVER")
    screen.blit(background,  (0,0))
    sn.draw(True)
    pygame.display.flip()

    sys.exit()
        
if __name__ == "__main__":
    main()
