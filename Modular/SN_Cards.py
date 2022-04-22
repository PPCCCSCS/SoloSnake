from SN_Defs import *

'''
Cards have suits, ranks, and positions. Everything else included
here is for layout purposes.
'''
class Card:
    def __init__(self,pos=[0,0],suit=CLUB,rank="",bg=WHITE,altPos=[-1,-1],tableau=-1):
        self.pos = [pos[0]*TS,pos[1]*TS]
        self.altPos = altPos
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
        self.tableau = tableau

        if self.suit == "":
            self.isPileTop = True
            #self.tableau = int(rank)
        else:
            self.isPileTop = False

    def __str__(self):
        return self.suit + self.rank

    def __repr__(self):
        return self.suit+self.rank+"@"+"X:"+str(int(self.pos[0]/TS))+",Y:"+str(int(self.pos[1]/TS))

    def testFit(self,card):
        if self.isPileTop:
            #print(self)
            if self.suit == SPADE or self.suit == CLUB:
                if card.suit == HEART or card.suit == DIAMOND:
                    if card.rank == RANKS[RANKS.index(self.rank)-1]:
                        self.isPileTop = False
                        return True
                    else:
                        return False
            elif self.suit == HEART or self.suit == DIAMOND:
                if card.suit == SPADE or card.suit == CLUB:         
                    if card.rank == RANKS[RANKS.index(self.rank)-1]:
                        self.isPileTop = False
                        return True
                    else:
                        return False
            #If the calling card is an empty pile
            elif self.suit == "" and self.rank in ["0","1","2","3","4","5","6"]:
                self.rank = self.rank + "*"
                self.isPileTop = False
                #self.rank = " "+self.rank+" "
                return True
            else:
                return False
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
                if self.rank == "0" and self.altPos[0]>0: #Empyt Tableau Spots
                    tset(RED,RED,.5,.5,.5,.5,BLACK)
                else:
                    tset(RED,RED,.5,.5,.5,.5,GREEN) #Dividers in Snake
            else:
                tset(GREY,GREY,.5,.5,.5,.5,GREY) #Dead Snake
        elif self.rank == "00":
            if not gameover:
                tset(RED,WHITE,.5,.65,.55,.35,GREEN) # Snake Head Alive
            else:
                tset(RED,WHITE,.5,.65,.55,.35,GREY) # Snake Head Dead
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

                '''
                Make the snake look in the direction of travel:
                '''

                if self.thisMove[0] > 0:
                    # To rotate 90 degrees:
                    #self.rank_disp = pygame.transform.rotate(self.rank_disp, 90)
                    self.rxoff += 2
                    self.ryoff -= 2
                    self.sxoff += 8

                elif self.thisMove[1] < 0:
                    # To rotate 180 degrees:
                    self.sxoff += 1
                    self.rxoff -= 1
                    self.syoff -= 18
                    self.ryoff += 12
                    #self.suit_disp = pygame.transform.rotate(self.suit_disp, 180)
                    #self.rank_disp = pygame.transform.rotate(self.rank_disp, 180)

                elif self.thisMove[0] < 0:
                    # To rotate -90 degrees:
                    #self.rank_disp = pygame.transform.rotate(self.rank_disp, 270)
                    self.rxoff -= 7
                    self.ryoff -= 2
                    self.sxoff -= 8
                else:
                    self.rxoff -= 3
                    self.ryoff -= 2

            else:
                self.suit_disp = f3.render("-", True, WHITE)
                self.rank_disp = f3.render("XX", True, BLACK)
                self.rxoff -= 2
        else:
            self.suit_disp = f2.render(self.suit, True, self.suit_color)
            
        if self.altPos[0] < 0:
            self.suit_rect = self.suit_disp.get_rect()
            self.suit_rect.center = [self.pos[0]+self.sxoff,self.pos[1]+self.syoff]
            self.rank_rect = self.rank_disp.get_rect()
            self.rank_rect.center = [self.pos[0]+self.rxoff,self.pos[1]+self.ryoff]

            if self.isPileTop:
                pygame.draw.rect(screen, BLUE, (self.pos[0]+1,self.pos[1]+1,TS+4,TS+4), border_radius=int(TS*.25))
            # This line draws the rounded colored squares for each card.
            # An outline could just be a slightly larger square drawn first.
            pygame.draw.rect(screen, self.bgcol, (self.pos[0]+4,self.pos[1]+4,TS-2,TS-2), border_radius=int(TS*.2))
        else:
            pygame.draw.rect(screen, self.bgcol, (self.altPos[0]+1,self.altPos[1]+1,TS-2,TS-2), border_radius=int(TS*.2))
            self.suit_rect = self.suit_disp.get_rect()
            self.suit_rect.center = [self.altPos[0]+self.sxoff,self.altPos[1]+self.syoff]
            self.rank_rect = self.rank_disp.get_rect()
            self.rank_rect.center = [self.altPos[0]+self.rxoff,self.altPos[1]+self.ryoff]
            #print(self.suit_rect.center,self.rank_rect.center,"\n\t",self.pos)
        

        screen.blit(self.suit_disp, self.suit_rect)
        screen.blit(self.rank_disp, self.rank_rect)
