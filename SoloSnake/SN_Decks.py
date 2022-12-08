from SN_Defs import *
from SN_Cards import *
from random import randint, choice, shuffle

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
            try:
                return self.cards.pop(randint(0,len(self.cards)-1))
            except:
                print("What?",len(self.cards))
        else:
            return Card(suit="",rank="")
