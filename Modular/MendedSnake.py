# -*- coding: utf8 -*-

"""
SNEK -- placeholder name for snake/solitaire mashup game
"""
import os, sys
from random import randint, choice, shuffle

from SN_Boards import *
from SN_Cards import *
from SN_Decks import *
from SN_Defs import *
from SN_Foundations import *
from SN_Layouts import *

def main():

    gb = Board()
    sn = gb.snake
    #print(gb.snake.queue)

    #gb.klondike.pushCardToTableau(Card(suit="",rank="3",tableau=2))
    #gb.klondike.pushCardToTableau(Card(suit="",rank="4",tableau=2))

    tmp = len(sn.queue)
    for i in range(tmp):
        
        for j in range(i):
            gb.klondike.pushCardToTableau(Card(suit="",
                                               rank=str(j),
                                               tableau=i-1))
            
    gb.klondike.drawTableaus()

    '''
    for i, sni in enumerate(sn.queue[1:]):
        for j in range(int(sni.tableau)+1):
            print("j=",j)
            gb.klondike.pushCardToTableau(Card(suit="",rank=str(j)))
    gb.klondike.drawTableaus()
    '''

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

        # Whenever the snake's head moves to a new tile, test to see if there's
        # any part of the snake in that tile, and gameover if so.
        if sn.queue[1].thisMove != [0,0]:
            if sn.queue[0].isNextTile():
                
                test_me = gb.tileContains(hp)
                
                hp_key = str([hp[0]*TS,hp[1]*TS])

                if hp_key in sn.hitboxes and sn.hitboxes[hp_key] != len(sn.queue):
                    gameover = True
                elif type(test_me) == Card:
                    
                    if not sn.addCard(test_me): # <--- add card if possible!
                        gameover = True
                    else:
                        push_me = Card(suit=test_me.suit,rank=test_me.rank)
                        push_me.tableau = sn.queue[sn.queue.index(test_me)].tableau
                        # Add card to Tableau ---> THIS NEEDS FIXING
                        print("ADDING ", push_me,push_me.tableau)
                        gb.klondike.pushCardToTableau(push_me)
                        gb.dealtCards.remove(test_me)
                        gb.field[hp[0]][hp[1]] = ''
                # Only add a new hitbox for the snake head after testing to be
                # sure it didn't collide with itself at that same location
                sn.addHitbox()    
                
        # update everything
        gb.klondike.drawTableaus()
        pygame.display.flip()
        clock.tick(CLOCKRATE)

    print("GAME OVER")
    #print(gb.klondike.Tableau)
    screen.blit(background,  (0,0))
    sn.draw(True)
    gb.klondike.drawTableaus()
    pygame.display.flip()

    sys.exit()
        
if __name__ == "__main__":
    main()
