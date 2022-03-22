import pygame
from pygame import FULLSCREEN
import random
import time

#window setup
import ctypes
user32 = ctypes.windll.user32
global scr_width
global scr_height
scr_width = user32.GetSystemMetrics(0)
scr_height = user32.GetSystemMetrics(1)
window = pygame.display.set_mode((scr_width,scr_height),FULLSCREEN)
pygame.display.set_caption("TEAK")
pygame.font.init()
from pygame.locals import *
pygame.init()

import AI as ai



class Board:
    def __init__(self):
        #Sets values        
        self.height = 20
        self.width = 30            
        self.Round = 1
        self.gen = 1

        #For showing grid
        self.thickness = 35
        self.TopCorner = scr_width//2 - self.width*self.thickness//2
        self.rect = pygame.Rect(self.TopCorner, 0, self.width*self.thickness, self.height*self.thickness)

        #ambience
        self.ambience = [pygame.mixer.Sound("sounds/GnashingandGrowling.wav")]
        #silly ambience
        #address = ["alternative#1.wav","alternative#2.wav","alternative#3.wav","alternative#4.wav","alternative#5.wav"]
        #self.ambience = []
        #for i in address:
        #    self.ambience.append(pygame.mixer.Sound(i))

    def Show(self): 
        pygame.draw.rect(window,(22,53,63),self.rect)

        #Round number
        SubFont = pygame.font.SysFont('', 100)
        Text = SubFont.render("RND "+str(self.Round), False, (130,51,60))
        window.blit(Text,(10,10))
        Text = SubFont.render("GEN "+str(self.gen), False, (130,51,60))
        window.blit(Text,(9,60))

        #ambience
        if not pygame.mixer.get_busy():
            pygame.mixer.Sound.play(random.choice(self.ambience))

class Safezone:
    def __init__(self, left):
        self.height = B.height * B.thickness
        self.width = B.thickness*2
        if left:
            self.coord = [B.TopCorner, 0]
        else:
            self.coord = [B.TopCorner+((B.width-1)*B.thickness)-self.width//2, 0]
        
        self.rect = (self.coord[0], self.coord[1], self.width, self.height)
        
    def Show(self):
        pygame.draw.rect(window,(90,142,84),self.rect)

    


class Player:
    def __init__(self, X, Y):
        self.coord = [X, Y]
        self.GridCoord = []
        self.CoordGridFinder()
        self.speed = 3
#        self.Nn = Networking
#        self.mesh = pygame.mask
        self.rect = pygame.Rect(self.coord[0],self.coord[1],self.width,self.height)
    
    def CoordGridFinder(self):
        #finds coords on board
        xFound = False
        yFound = False
        X = 0
        Y = 0
        for x in range(0, B.width):
            if (xFound == False) and (self.coord[0]+self.width//2 >= (B.TopCorner + B.thickness*x)) and (self.coord[0]+self.width//2 <= (B.TopCorner + B.thickness*(x+1))):
                X = x
                xFound = True
            for y in range(0, B.height):
                if (yFound == False) and (self.coord[1]+self.height//2 >= B.thickness*y) and (self.coord[1]+self.height//2 <= B.thickness*(y+1)):
                    Y = y
                    yFound = True
        
        self.GridCoord = X,Y

    def Move(self, planes):
        for i in range(0, 2): #cycles through planes
            for x in range(0, 2): 
                self.coord[i] += planes[i][x]
        self.BoundaryCheck()

    def Show(self): 
        self.CoordGridFinder()
        self.rect = pygame.Rect(self.coord[0],self.coord[1],self.width,self.height)
        window.blit(self.image, (self.coord[0],self.coord[1]))

    def AI(self):
        Hori = [0,0]
        Verti = [0,0]
        result = []
        if self.type == "runner":
            result = ai.runnerAI(self, bulldogs)
        else:
            result = ai.bulldogAI(self, runners, bulldogs)
        if result[0] > 0.5:
            #up
            Verti[0] = -self.speed
        if result[1] > 0.5:
            #down
            Verti[1] = self.speed
        if result[2] > 0.5:
            #left
            Hori[0] = -self.speed
        if result[3] > 0.5:
            #right
            Hori[1] = self.speed
        self.Move([Hori, Verti])

class Runner(Player):
    def __init__(self):
        #game details
        self.caught = False
        self.safe = False
        self.type = "runner"

        #pygame details
        self.image =  pygame.image.load("images/runner.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        #sounds
        address = ["sounds/Deathsound#1.wav","sounds/Deathsound#2.wav","sounds/Deathsound#4.wav","sounds/Deathsound#5.wav"]
        self.deathsound = []
        for i in address:
            self.deathsound.append(pygame.mixer.Sound(i))


        Sz = SafeZones[0]
        X = random.randint(Sz.coord[0], Sz.coord[0]+Sz.width-self.width)
        Y = random.randint(Sz.coord[1], Sz.coord[1]+Sz.height-self.height)
        super().__init__(X,Y)
    
    def SafeCheck(self):
        if self.coord[0] > SafeZones[1].coord[0]:
            self.safe = True
        else:
            self.safe = False
            
    def BoundaryCheck(self):
        if self.coord[0] < B.TopCorner:
            self.coord[0] += self.speed
        elif self.coord[0] > B.TopCorner+(B.width*B.thickness)-self.width:
            self.coord[0] -= self.speed
        elif self.coord[1] < 0:
            self.coord[1] += self.speed
        elif self.coord[1] > ((B.height)*B.thickness)-self.height:
            self.coord[1] -= self.speed

        self.SafeCheck()
    
    

class Bulldog(Player):
    def __init__(self):
        #game details
        self.catches = 0
        self.type = "bulldog"

        #pygame details
        self.image =  pygame.image.load("images/bulldog.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        X = scr_width//2-self.width//2
        Y = (B.height*B.thickness)//2-self.height//2
        super().__init__(X,Y)


    def Catch(self, runners):
        for i in range(0, len(runners)):
            if self.rect.colliderect(runners[i].rect):
                pygame.mixer.Sound.play(random.choice(runners[i].deathsound))
                runners[i].caught = True
                runners[i].image = pygame.image.load("images/caught.png")
                self.catches += 1

                
    def BoundaryCheck(self):
        if self.coord[0] < B.TopCorner:
            self.coord[0] += self.speed
        elif self.coord[0]+self.width > SafeZones[1].coord[0]:
            self.coord[0] -= self.speed
        elif self.coord[1] < 0:
            self.coord[1] += self.speed
        elif self.coord[1] > ((B.height)*B.thickness)-self.height:
            self.coord[1] -= self.speed

#functions
def Control():
    #end button
    details = scr_width-50, scr_height-50, 50, 50
    pygame.draw.rect(window,(255,0,0),details)
    RUN = True
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            Mx, My = pygame.mouse.get_pos()
            if Mx > scr_width-50 and Mx < scr_width and My < scr_height and My > scr_height-50:
                RUN = False
    return RUN

def Initialize():
    playerno = 100
    runners = []
    bulldogs = []
    caught = []
    for i in range(0,playerno-1):
        runners.append(Runner())
    bulldogs.append(Bulldog())

    return runners, bulldogs, caught


def Handling(runners, bulldogs, caught):
    #push all caught runners to caught list
    for i in runners:
        if i.caught:
            runners.remove(i)
            caught.append(i)

    #test if round is done
    Test = True
    for i in runners:
        if i.safe == False:
            Test = False

    if Test:
        #Prep for next round
        pygame.mixer.fadeout(500)
        time.sleep(0.5)
        B.Round += 1
        
        #reset all runners and bulldogs
        #and turn all caught runners to bulldogs
        for i in runners:
            i.__init__()
        for i in bulldogs:
            i.__init__()
        for i in caught:
            bulldogs.append(Bulldog())
        caught = []

        if len(runners) == 0:
            B.gen += 1
            B.Round = 1
            runners, bulldogs, caught = Initialize()

    return runners, bulldogs, caught



if __name__ == '__main__':
    B = Board()
    SafeZones = []
    SafeZones.append(Safezone(True))
    SafeZones.append(Safezone(False))

    #generates players
    runners, bulldogs, caught = Initialize()

    RUN = True
    while RUN:
        pygame.time.delay(1)
        window.fill((22,33,48))
        #AI
        for i in runners:
            i.AI()
        for i in bulldogs:
            i.AI()
            i.Catch(runners)

        #show
        B.Show()
        for i in SafeZones:
            i.Show()
        for i in caught:
            i.Show()
        for i in runners:
            i.Show()
        for i in bulldogs:
            i.Show()

        
        RUN = Control()
        pygame.display.update()
        runners, bulldogs, caught = Handling(runners, bulldogs, caught)
        