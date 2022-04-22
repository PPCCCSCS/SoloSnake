from SN_Defs import *
from SN_Cards import *
from SN_Foundations import *

'''
Klondike will display the cards in the right pane the way they would
be displayed in a regular game of Solitaire. Mostly useful for
debugging early on, but it may be a valuable display option for
the final game. Replaces the Foundation class previously implemented.
'''
class Klondike:
    def __init__(self,row=0,col=0):
        self.row = row
        self.col = col
        
        self.nextCard  = Card(suit='X')
        
        self.disCards  = []
        
        self.fHearts   = [Foundation(HEART  ,row=row,column=col+0)]
        self.fDiamonds = [Foundation(DIAMOND,row=row,column=col+1)]
        self.fClubs    = [Foundation(CLUB   ,row=row,column=col+2)]
        self.fSpades   = [Foundation(SPADE  ,row=row,column=col+3)]

        self.Tableau   = [[],[],[],[],[],[],[]]

    def drawTableTop(self):
        # Draw the stockpile, wastepile, and foundations backgrounds
        for i in (0,1,3,4,5,6):
            pygame.draw.rect(background,
                             (255,255,0),
                             (TS*(COLS+self.col+i)+(i*4)+(self.col*2)+7,
                              TS*(self.row)+4 ,
                              TS,
                              TS),
                             2,
                             border_radius=int(TS*.2))
        # Draw the Tableau backgrounds
        for i in range(7):
            pygame.draw.rect(background,
                             (255,255,0),
                             (TS*(COLS+self.col+i)+(i*4)+(self.col*2)+7,
                              TS*(self.row+1)+8 ,
                              TS,
                              TS),
                             2,
                             border_radius=int(TS*.2))

    def drawTableaus(self):
        for i,t in enumerate(self.Tableau):
            k=1
            for j,c in enumerate(t):
                if j>0:
                    k=1/3
                c.altPos = [TS*(COLS+self.col)+(c.tableau*(TS+4))+7,
                            TS*(self.row+k)+8+(j*(2*TS/3))]
                c.draw()
                
    def pushCardToTableau(self,card):

        tableau = card.tableau

        if card.suit == "":
            self.Tableau[tableau].append(card)


        elif card.suit in [HEART,DIAMOND,CLUB,SPADE]:
            if self.Tableau[tableau][-1].suit == "":
                self.Tableau[tableau].append(card)
            elif (card.suit in [HEART,DIAMOND] and self.Tableau[tableau][-1].suit in [CLUB,SPADE]) or \
                 (card.suit in [CLUB,SPADE] and self.Tableau[tableau][-1].suit in [HEART,DIAMOND]):
                if RANKS.index(card.rank) == RANKS.index(self.Tableau[tableau][-1].rank) + 1:
                    #card.altPos = [TS*(COLS+self.col)+(c.tableau*(TS+8))+7,
                    #       TS*(self.row+1)+8+8*len(self.Tableau[tableau])]
                    self.Tableau[tableau].append(card)
                    print("Appended.")
        else:
            print("Weird Card Push to Tableau")

        self.drawTableaus()

        ### DEBUGGERY ###
        '''
        for tab in self.Tableau:
            print(tab,len(tab),end=",")
        print()
        #'''
        
