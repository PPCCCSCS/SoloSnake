from SN_Defs import *
from SN_Cards import *

'''
Foundations are the four piles where cards go, in order from least
to greatest, after they are removed from one of the seven piles in
play in Klondike, or one of the seven segments of the snake in this
game. The player wins when all of the cards from the Deck have been
transferred to the appropriate Foundation.
'''
class Foundation:
    def __init__(self,suit,row=0,column=0):
        self.cards  = [Card(suit=suit)]
        self.column = column
        self.row    = row

    def draw(self):
        #pass
        pygame.draw.rect(background, (255,255,0), (TS*(COLS+self.column+3)+4,TS*self.row+4 ,TS,TS),2,border_radius=int(TS*.2))

    def refresh(self):
        for i, card in enumerate(self.cards):
            card.move(self.pos[0],self.pos[1]+(TS*i))
            card.draw()
            pygame.display.flip()

