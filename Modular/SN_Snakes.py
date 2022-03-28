from SN_Defs import *
from SN_Cards import *

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
        while index < len(self.queue) and not self.queue[index].testFit(card):
                index = index + 1
        if index < len(self.queue):#-1:
            #insert card before correct segment
            card.isPileTop = True
            card.pos = self.queue[index].pos
            card.thisMove = self.queue[index].thisMove
            card.nextMove = self.queue[index-2].nextMove
            card.tableau = self.queue[index].tableau
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
        else:
            success = False

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
    
