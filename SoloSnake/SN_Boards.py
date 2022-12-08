from SN_Defs import *
from SN_Decks import *
from SN_Layouts import *
from SN_Snakes import *

'''
Game board defaults to 20x20. Each position should be empty, initially,
but we'll populate random positions with cards from the deck after the
Snek is instantiated and set loose. Or slightly before; choices.
'''
class Board:
    def __init__(self,size=(COLS,ROWS)):
        self.field = []
        self.deck = Deck()
        self.klondike = Klondike(8,0)
        self.dealtCards = []
        self.snake = Snek([COLS//2,ROWS//2])

        for y in range(size[1]):
            temp = []
            for x in range(size[0]):
                temp.append('')
            self.field.append(temp)

        # draw playfield border
        pygame.draw.rect(background, (255,255,0), (1, 1, (TS * COLUMNS)+3, (TS * ROWS)+3), 2)

        self.klondike.drawTableTop()

        screen.blit(background,  (0,0))
        screen.blit(dispTITLE,   rectTITLE)

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
                while True:
                    tcard = self.deck.cards.pop()
                    if tcard.rank != "":
                        break
                tcard.setPos([x,y])
                self.field[x][y] = tcard
                self.dealtCards.append(tcard)
                placed = True
        
    def tileContains(self,pos=[0,0]):
        return self.field[pos[0]][pos[1]]
