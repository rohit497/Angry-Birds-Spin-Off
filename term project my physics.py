# term project.py
# name + andrewId + section
#Rohit Ramesh Pillai+rrpillai+Section O
######################################################################

import pygame
import math
import random
#from pygame.locals import *

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.mixer.init()
pygame.time.set_timer(pygame.USEREVENT+1, 100)
clock = pygame.time.Clock()

class Bomb(object):#initializes the bomb object
   def __init__(self, (x, y), size):
        self.size = size #defines its radius
        self.speed = 3 #start speed
        self.angle = 0 #angle at which it falls
        self.image = pygame.image.load("bomb.png").convert()
        #the image of the bomb
        self.rect = self.image.get_rect()
        #the rectangle around the image of the bomb
        self.image.set_colorkey((255,255,255))
        #makes the white part of the image transparent
        self.explodeimage = pygame.image.load("explosion.png").convert()
        #image after explosion
        self.exploderect = self.explodeimage.get_rect()
        self.explodeimage.set_colorkey((0,0,0))
        #makes the black part of the image transparent
        self.rect.x = x-size#sets the top left corner of image
        self.rect.y = y-size
        #sets the top left corner of image
        self.gravity=0.4
        self.collide=False#checks if it has collided with an object
        self.time=0 #measures time after explosion
        self.playFlag=0
        
   def display(self):#displays the bomb
       if(self.collide == False):
           game.screen.blit(self.image, self.rect)
       elif(self.collide == True)and(self.time<=25):
           self.time+=1
           game.screen.blit(self.explodeimage, self.exploderect)
       
   def move(self):#makes the bomb move vertically downward and
#moves the explosion image along with it
       self.rect.y+=self.speed
       self.speed+=self.gravity
       self.exploderect.x=self.rect.x-2*self.rect.width
       self.exploderect.y=self.rect.y-2*self.rect.height
       
   def collision(self,p2): #detects collisions between bomb and walls or bird 
   #if there are any, makes self.collide True 
          
        if(isinstance(p2,Wall)==True): #collisions with walls
            #top of the wall
            if p2.x<=self.rect.x+self.size<=p2.x+p2.width and (abs(p2.y-self.rect.y-self.size)<=self.size):
                self.collide=True
                #bottom of the wall
            elif p2.x<=self.rect.x+self.size<=p2.x+p2.width and (abs(self.rect.y+self.size-p2.y-p2.height)<=self.size):
                self.collide=True
                #left side of the wall
            elif p2.y<=self.rect.y+self.size<=p2.y+p2.height and abs(p2.x-self.rect.x-self.size)<=self.size:
                self.collide=True
                #right side of the wall
            elif p2.y<=self.rect.y+self.size<=p2.y+p2.height and abs(self.rect.x+self.size-p2.x-p2.width)<=self.size:
                self.collide=True
                #top left corner
            elif ((self.rect.x+self.size-p2.x)**2+(self.rect.y+self.size-p2.y)**2)**0.5<=self.size: 
                self.collide=True
                #top right corner
            elif ((self.rect.x+self.size-p2.x-p2.width)**2+(self.rect.y+self.size-p2.y)**2)**0.5<=self.size:
                self.collide=True
                #bottom left corner
            elif ((self.rect.x+self.size-p2.x)**2+(self.rect.y+self.size-p2.y-p2.height)**2)**0.5<=self.size: 
                self.collide=True
               #bottom right corner
            elif ((self.rect.x+self.size-p2.x-p2.width)**2+(self.rect.y+self.size-p2.y-p2.height)**2)**0.5<=self.size:
                self.collide=True
                
        elif(isinstance(p2,Bird)==True):#checks if it collides with a bird
            dx = self.rect.x +self.size - p2.rect.x
            dy = self.rect.y +self.size- p2.rect.y
            dist = math.hypot(dx, dy)#finds the distance between their centres
            if dist < self.size + p2.size:
                self.collide=True
                #indicates that the bomb has collided with something
                p2.speed=0 #stops the bird from moving
                p2.explode=True 
                return "Done" #indicates that it has collided with the bird

class Target(object): #initializes a target object
         
    def __init__(self, color, (x, y), size):
        self.x = x
        self.y = y
        #initializes the centre of the target
        self.size = size#radius of target
        self.colour = color#color of target
        
    def display(self):#displays the target
        pygame.draw.circle(game.screen, self.colour, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(game.screen, (255,255,255), (int(self.x), int(self.y)), self.size/2)
        pygame.draw.circle(game.screen, self.colour, (int(self.x), int(self.y)), self.size/4)
        pygame.draw.circle(game.screen, (255,255,255), (int(self.x), int(self.y)), self.size/8)
        pygame.draw.circle(game.screen, self.colour, (int(self.x), int(self.y)), self.size/16)
        
    def __repr__(self):
        return "Target((%d,%d,%d),(%d,%d),%d)"%(self.colour[0],self.colour[1],self.colour[2],self.x,self.y,self.size)
        
class Wall(object):#initializes the wall object

    def __init__(self,color,(x,y),width,height):
        self.x = x
        self.y = y
        #initializes the top left of the rectangle
        self.width = width #width of rectangle
        self.height = height #height of rectangle
        self.colour = color #color of rectangle
        if(self.width>self.height):
             self.rotate=0 #indicates the rectangle is horizontal
        else:
            self.rotate=1 #indicates the rectangle is vertical
        
    def display(self): #displays the wall
        pygame.draw.rect(game.screen,self.colour,(int(self.x), int(self.y),self.width,self.height))
        #draws the lines indicating end of a brick
        if(self.rotate==0):
          div=self.width/10  
          for i in xrange(div):
            pygame.draw.line(game.screen,(0,0,0),((i+1)*self.width/div+self.x,self.y),((i+1)*self.width/div+self.x,self.y+self.height))
        else:
          div=self.height/10   
          for i in xrange(div):
            pygame.draw.line(game.screen,(0,0,0),(self.x,(i+1)*self.height/div+self.y),(self.width+self.x,self.y+(i+1)*self.height/div))
        
    def __repr__(self):
        return "Wall((%d,%d,%d),(%d,%d),%d,%d)"%(self.colour[0],self.colour[1],self.colour[2],self.x,self.y,self.width,self.height)

class Bird(object): #initializes the bird object
    def __init__(self, color, (x, y), size):
        self.initX=x 
        self.initY=y
        #initial position of the bird
        self.size = size #radius of bird
        self.colour = color #color of bird
        self.speed = 0 #speed of bird
        self.angle = 0 #angle of bird
        self.gravity = (math.pi, 0.4) #gravity vector
        self.image = pygame.image.load("red-big.png").convert()
        #image of bird before it explodes
        self.rect = self.image.get_rect()
        #gets rectangle around the image
        self.explodeimage = pygame.image.load("burnt bird.png").convert()
        #image of bird after it explodes
        self.exploderect = self.explodeimage.get_rect()
        #gets rectangle around the image
        self.explodeimage.set_colorkey((255,255,255))
        self.image.set_colorkey((255,255,255))
        #makes the white part of the images transparent
        self.rect.x = x-size
        self.rect.y = y-size
        #sets the top left corner of the image
        self.lastPoint=0
        #stores the last point where the bird bounces
        self.bounces=0
        #counts the number of times the bird bounces at the last point
        self.explode=False#indicates if the bird has exploded or not
        
    def display(self):#displays the bird
        if(self.explode==False):
            game.screen.blit(self.image, self.rect)
        else:
            game.screen.blit(self.explodeimage, self.exploderect)
        
    def __repr__(self):
        return "Bird((%d,%d,%d),(%d,%d),%d)"%(self.colour[0],self.colour[1],self.colour[2],self.rect.x,self.rect.y,self.size)
          
    def move(self):#moves the bird
        #modified from http://www.petercollingridge.co.uk/book/export/html/6 
        self.rect.x += math.sin(self.angle) * self.speed
        self.rect.y -= math.cos(self.angle) * self.speed
        self.exploderect.x=self.rect.x
        self.exploderect.y=self.rect.y
        drag = 0.998
        self.angle,self.speed=self.addVectors(self.gravity)
        self.speed*=drag
        
    def addVectors(self, (angle2, length2)):#from http://www.petercollingridge.co.uk/book/export/html/6
        #involves gravity for the bird's motion
        x  = math.sin(self.angle) * self.speed + math.sin(angle2) * length2
        y  = math.cos(self.angle) * self.speed + math.cos(angle2) * length2
        length = math.hypot(x, y)
        angle = 0.5 * math.pi - math.atan2(y, x)
        return (angle, length)
        
    def collision(self,p2):   
          
        if(isinstance(p2,Wall)==True):#checks if the bird collides with a wall
            #top of the wall
            if p2.x<=self.rect.x+self.size<=p2.x+p2.width and (abs(p2.y-self.rect.y-self.size)<=self.size):
                return (self.rect.x+self.size,p2.y,True)
            #bottom of the wall
            elif p2.x<=self.rect.x+self.size<=p2.x+p2.width and (abs(self.rect.y+self.size-p2.y-p2.height)<=self.size):
                return (self.rect.x+self.size,p2.y+p2.height,True)
            #left side of the wall
            elif p2.y<=self.rect.y+self.size<=p2.y+p2.height and abs(p2.x-self.rect.x-self.size)<=self.size:
                return(p2.x,self.rect.y+self.size,True)
            #right side of the wall
            elif p2.y<=self.rect.y+self.size<=p2.y+p2.height and abs(self.rect.x+self.size-p2.x-p2.width)<=self.size:
                return(p2.x+p2.width,self.rect.y+self.size,True)
            #top left corner of the wall
            elif ((self.rect.x+self.size-p2.x)**2+(self.rect.y+self.size-p2.y)**2)**0.5<=self.size: 
                return ((self.rect.x+self.size)*(1+math.cos(math.pi/4)),(self.rect.y+self.size)*(1+math.sin(math.pi/4)),"L",True)
            #top right corner of the wall   
            elif ((self.rect.x+self.size-p2.x-p2.width)**2+(self.rect.y+self.size-p2.y)**2)**0.5<=self.size:
                return ((self.rect.x+self.size)*(1+math.cos(math.pi/4)),(self.rect.y+self.size)*(1+math.sin(math.pi/4)),"R",True)
            #bottom left corner of the wall   
            elif ((self.rect.x+self.size-p2.x)**2+(self.rect.y+self.size-p2.y-p2.height)**2)**0.5<=self.size: 
                return ((self.rect.x+self.size)*(1+math.cos(math.pi/4)),(self.rect.y+self.size)*(1-math.sin(math.pi/4)),"L",True)
            #bottom right corner of the wall
            elif ((self.rect.x+self.size-p2.x-p2.width)**2+(self.rect.y+self.size-p2.y-p2.height)**2)**0.5<=self.size:
                return ((self.rect.x+self.size)*(1+math.cos(math.pi/4)),(self.rect.y+self.size)*(1-math.sin(math.pi/4)),"R",True)
        
        elif(isinstance(p2,Target)==True):#checks if the bird collides with a target
            dx = self.rect.x +self.size - p2.x
            dy = self.rect.y +self.size- p2.y
            dist = math.hypot(dx, dy)#calculates the distance between their centres
            if dist < self.size + p2.size:
                return True
                
        return False #if no collision at all, returns False 
            
    def wallCollide(self,p2):
        #calculates the rebound angle after colliding with a wall
        collide=self.collision(p2)
        if(collide!=False):
            elasticity=0.75 
            if(collide[1]==p2.y):
                #angle after colliding with top of wall
                self.angle = 3*math.pi-self.angle
                if(collide[0]==self.lastPoint):
#checks if the bird is bouncing at particular point or not
                    self.bounces+=1
                else:
                    self.lastPoint=collide[0]
                    self.bounces=0
            elif(collide[0]==p2.x or (collide[0]==(self.rect.x+self.size)*(1+math.cos(math.pi/4))and collide[2]=="L")):
         #calculates angle after bouncing off left wall
                self.angle=2*math.pi-self.angle
            elif(collide[1]==p2.y+p2.height):
        #calculates angle after bouncing off bottom of wall
                self.angle = math.pi/2+self.angle
            elif(collide[0]==p2.x+p2.width or (collide[0]==(self.rect.x+self.size)*(1+math.cos(math.pi/4))and collide[2]=="R")):
        #calculates angle after bouncing off right wall
                self.angle = 3*math.pi/2+self.angle
            self.speed *= elasticity#decreases the bird's speed after a collision
            self.move()#moves the bird in the direction of the new angle
            
            
class CreatedLevel(object):#displays the created level 
 def __init__(self,width,height,num):
     self.screen = pygame.display.set_mode((width, height))
     #creates a screen
     self.font = pygame.font.Font(None, 18)
     #defines a font to display in-game stats
     self.endFont = pygame.font.Font(None, 36)
     #defines a font to display end game text
     self.endFlag=0#checks if the level is over
     self.tries=0#indicates the number of tries the user has
     self.num=num
     self.wallList=[]#a list of all the walls in the level
     self.circle=None
     self.target=None
     self.birdline=None
     #initiaizes all objects to None 
     self.contents=self.readFile("SavedLevel"+self.num+".txt")
     if(self.contents!="0"):
         for line in self.contents.splitlines():
             if(line[0]=="W"):
                 self.wallList.append(eval(line))
             elif(line[0]=="T"):
                 self.target=eval(line)
             elif(line[0]=="B"):
                 self.birdline=line
                 self.circle=eval(line)
#reads the file where all the data is stored and creates the objects
     self.image = pygame.image.load("background.png").convert()
     self.imagerect = self.image.get_rect()
#loads the background image
     self.highScore=int(self.readFile("CreatedLevel"+self.num+"HighScore.txt"))
#gets the highscore from the file
     
 def initAnimation(self):
    if(self.birdline!=None):
        self.circle=eval(self.birdline)#initializes the bird object
    self.screenXSize,self.screenYSize=self.screen.get_size()
#finds height and width of the screen
    self.initBomb()
    self.MousePressed=False
    self.MouseDown=False 
#checks if the mouse is pressed or not
    self.MouseReleased=False 
#checks if the mouse is released or not
    self.done = False
#checks if the user closed the window
    self.score=0
#stores the users score in the current turn of the level
    self.stopFlag=0#checks if the current try is done or not
    self.back=False #checks if the user pressed the back button
    self.menu=0#checks if the user has pressed the menu button
    self.endMusicFlag=0#checks if the music at end level has been played or not
    self.result=None#gets the result of the collide function of the bomb
    pygame.mixer.music.load("Red Bird noise.mp3")
    
 def initBomb(self):#initializes the bomb object
     if(self.circle!=None):
         self.bomb=Bomb((random.randint(self.circle.rect.x+40,self.circle.rect.x+100),0),15)
     
 def highlightButtons(self):#highlights all buttons on the menu screen
     pos=pygame.mouse.get_pos()
     if(self.menu==1):
        if(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=60)and(pos[1]>=20):  
            pygame.draw.rect(self.screen,(255,0,0),(5,15,70,50))
        elif(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=130)and(pos[1]>=90):
            pygame.draw.rect(self.screen,(255,0,0),(5,85,70,50))
        elif(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=200)and(pos[1]>=160):
            pygame.draw.rect(self.screen,(255,0,0),(5,155,70,50))
        elif(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=270)and(pos[1]>=230):
            pygame.draw.rect(self.screen,(255,0,0),(5,225,70,50))
     elif(self.endFlag==1):
        if(pos[0]>=200)and(pos[0]<=260)and(pos[1]<=90)and(pos[1]>=50):
             pygame.draw.rect(self.screen,(255,0,0),(195,45,70,50))
        elif(pos[0]>=100)and(pos[0]<=160)and(pos[1]<=90)and(pos[1]>=50):
             pygame.draw.rect(self.screen,(255,0,0),(95,45,70,50))
     elif(pos[0]>=0)and(pos[0]<=50)and(pos[1]<=30)and(pos[1]>=0):
         pygame.draw.rect(self.screen,(255,0,0),(0,0,55,35))
      
 def display(self):#displays all elements on the screen
     self.screen.fill((0, 0, 0))
     self.screen.blit(self.image, self.imagerect)
     if(self.contents=="0")or(self.contents==''):#checks if there are any objects saved or not
         self.screen.blit(self.endFont.render("No Created Level", True, (255,255,255)), (100,100))
     else:#if there are saved objects, displays them 
         if(self.MouseReleased==True):
             self.bomb.display()
             if(self.circle!=None)and(self.bomb.collide==True)and(self.bomb.playFlag==0):
        #checks if the bomb has collided with something and play sound if it has
                 pygame.mixer.music.load("bomb sound.mp3")
                 pygame.mixer.music.play()
                 self.bomb.playFlag=1
         if(self.MouseReleased==False)and(self.circle!=None):
#if mouse isn't released, then draws bounding box around bird
            pygame.draw.lines(self.screen,(0,0,0),True,[(self.circle.initX-30-self.circle.size,self.circle.initY-self.circle.size)
        ,(self.circle.initX+self.circle.size,self.circle.initY-self.circle.size), 
        (self.circle.initX+self.circle.size,self.circle.initY+30+self.circle.size)
        ,(self.circle.initX-30-self.circle.size,self.circle.initY+30+self.circle.size)])
         if(self.circle!=None): 
             self.circle.display()
         if(self.target!=None):
             self.target.display()
         if(len(self.wallList)!=0):
             for wall in self.wallList:
                 wall.display()
     self.highlightButtons()
     pygame.draw.rect(self.screen,(200,150,175),(0,0,50,30))
     self.screen.blit(self.font.render("Menu", True, (255,255,255)),(10,10))
     self.screen.blit(self.font.render("Score:"+str(self.score), True, (255,255,255)), (150, 0))
     self.screen.blit(self.font.render("HighScore:"+str(self.highScore), True, (255,255,255)), (235, 0))
     self.screen.blit(self.font.render("Tries:"+str(self.tries), False, (255,255,255)), (350, 0))       
     if(self.endFlag==1):#checks if game is over
        if(self.tries==0):#if out of tries, plays lost level sound 
            if(self.endMusicFlag==0):
                 pygame.mixer.music.load("Level Lost sound.mp3")
                 pygame.mixer.music.play()
                 self.endMusicFlag=1
            self.screen.blit(self.endFont.render("You Lose", True, (255,255,255)), (100, 100))
        else:#if tries left, plays won level sound
            if(self.endMusicFlag==0):
                 pygame.mixer.music.load("End level sound.mp3")
                 pygame.mixer.music.play()
                 self.endMusicFlag=1
            self.screen.blit(self.endFont.render("You Win", True, (255,255,255)), (100, 100))
            if(self.score>self.highScore):
                self.screen.blit(self.endFont.render("New High Score!", True, (255,0,0)), (80, 130))
        pygame.draw.rect(self.screen,(100,200,150),(100,50,60,40))
        self.screen.blit(self.font.render("Restart", True, (255,255,255)),(110,65))
        pygame.draw.rect(self.screen,(100,200,150),(200,50,60,40))
        self.screen.blit(self.font.render("Back", True, (255,255,255)),(210,65))
     elif(self.menu==1):
        self.displayMenu()
     pygame.display.flip()
     clock.tick(60)
     
 def onTimerFired(self):#carries out events when timer is fired
     if(((self.bomb.time>25)or(((self.bomb.rect.x+2*self.bomb.size<0)or(self.bomb.rect.x>=self.screenXSize))\
        or((self.bomb.rect.y+2*self.bomb.size<0) or(self.bomb.rect.y>=self.screenYSize))))and self.result==None and self.circle!=None):
#checks if the bomb goes off screen or has exploded more than a certain time ago
#before initializing a new bomb
        self.initBomb()
     for wall in self.wallList:
#checks if the bird has collided with a wall at low speed or bounced at a point  
#more than 10 times. If yes, the turn is over.
            if((self.circle.collision(wall)!=False)and(self.circle.speed<2))or(self.circle.bounces>3):
                self.circle.speed=0
                self.circle.gravity=(0,0)
                self.stopFlag=1
                break
     if(self.stopFlag==0): #if turn isn't over, moves the bird        
        self.circle.move()
        if(self.bomb.collide==False):
            self.bomb.move()
        if(self.result==None):#if bomb hasn't collided with bird, keeps checking
            self.result=self.bomb.collision(self.circle)
        for wall in self.wallList:#checks if anything collides with the walls
            self.circle.wallCollide(wall)
            self.bomb.collision(wall)
        if(self.circle.collision(self.target)==True):
            #if it collides with target, game is over
            self.endFlag=1
        elif(((self.circle.rect.x+2*self.circle.size<0)or(self.circle.rect.x>=self.screenXSize))\
        or(self.circle.rect.y>=self.screenYSize)):
        #checks if bird goes off screen. If yes, turn is over
            self.stopFlag=1
     if(self.tries == 0):#ends game if out of tries
        self.endFlag=1
     if(self.endFlag==1):#assign score if game is over
         if(self.tries==0):
             self.score=0
         else:
             if(self.score==0):
                self.score+=5000+(self.tries-1)*10000
                if(self.score>self.highScore):
#writes into the file if score is greater than highScore & game is over
                    self.writeFile("CreatedLevel"+self.num+"HighScore.txt",str(self.score))
     elif(self.stopFlag==1):#if game not over but turn is over, resets game
                self.tries-=1
                self.initAnimation()
            
 def onMousePressed(self):#handles all mouse pressed events
   pos=pygame.mouse.get_pos()
   if(self.circle!=None):  
     if(((pos[0]-self.circle.rect.x-self.circle.size)**2+(pos[1]-self.circle.rect.y-self.circle.size)**2)**0.5<=self.circle.size) \
     and self.MouseReleased==False and self.tries>0:
         if(self.MousePressed==False):
#checks if mouse was pressed inside the bird or not.
             self.MousePressed=True 
             self.MouseDown=True 
     if(pos[0]>self.circle.initX-30)and(pos[0]<=self.circle.initX)and \
     (pos[1]<self.circle.initY+30)and(pos[1]>=self.circle.initY)and(self.MouseReleased==False)and self.tries>0:
#limits the dragging of the bird to a bounding box
            self.circle.rect.x=pos[0]-self.circle.size
            self.circle.rect.y=pos[1]-self.circle.size
            if(self.circle.speed==0):
#makes the speed proportional to the amount dragged and calculates angle of release
                self.circle.speed=1
            elif(self.circle.speed<12):
                self.circle.speed=0.8*(max(abs(pos[0]-self.circle.initX),abs(pos[1]-self.circle.initY)))
            dx=self.circle.initX-self.circle.rect.x-self.circle.size
            dy=self.circle.rect.y+self.circle.size-self.circle.initY
            if(dy==0):
                self.circle.angle=math.pi/2
            else: 
                self.circle.angle=math.atan(float(dx)/dy)
     elif(self.endFlag==1):
#if game is over, checks if restart or back buttons are pressed
        if(pos[0]>=200)and(pos[0]<=260)and(pos[1]<=90)and(pos[1]>=50):
             self.back=True
        elif(pos[0]>=100)and(pos[0]<=160)and(pos[1]<=90)and(pos[1]>=50):
             self.endFlag=0
             if(len(self.wallList)<3):
                 self.tries = 3
             else:
                 self.tries = len(self.wallList)
             self.highScore=int(self.readFile("CreatedLevel"+self.num+"HighScore.txt"))
             self.initAnimation()
   if(pos[0]>=0)and(pos[0]<=60)and(pos[1]<=40)and(pos[1]>=0):
#checks if menu button is pressed
         self.menu=1
   elif(self.menu==1):
#if in menu mode, checks if any of the menu buttons are pressed
        if(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=60)and(pos[1]>=20):  
            self.endFlag=0
            if(len(self.wallList)<3):
                 self.tries = 3
            else:
                 self.tries = len(self.wallList)
            self.highScore=int(self.readFile("CreatedLevel"+self.num+"HighScore.txt"))
            self.initAnimation()
        elif(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=130)and(pos[1]>=90):
            self.menu=0
        elif(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=200)and(pos[1]>=160):
            HelpScreen(self.screenXSize,self.screenYSize).run()
        elif(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=270)and(pos[1]>=230):
            self.back=True
            
 def displayMenu(self):#displays the menu
     pygame.draw.rect(self.screen,(128,128,128),(0,0,100,self.screenYSize))
     self.highlightButtons()
     pygame.draw.rect(self.screen,(100,200,150),(10,20,60,40))
     self.screen.blit(self.font.render("Restart", True, (255,255,255)),(20,30))
     pygame.draw.rect(self.screen,(100,200,150),(10,90,60,40))
     self.screen.blit(self.font.render("Back to", True, (255,255,255)),(20,100))
     self.screen.blit(self.font.render("Game", True, (255,255,255)),(20,115))
     pygame.draw.rect(self.screen,(100,200,150),(10,160,60,40))
     self.screen.blit(self.font.render("Help", True, (255,255,255)),(20,170))
     pygame.draw.rect(self.screen,(100,200,150),(10,230,60,40))
     self.screen.blit(self.font.render("Back to", True, (255,255,255)),(11,240))
     self.screen.blit(self.font.render("Main Menu", True, (255,255,255)),(11,255))
     
 def onMouseReleased(self):#resets mouse pressed to false & mouse released to true
    if(self.MousePressed==True):
        pygame.mixer.music.play()
        self.MouseReleased=True
        self.MousePressed=False
        self.MouseDown=False
             
 def readFile(self,filename, mode="rt"):#from course notes
#returns the highScore in the file
        try:
           with open(filename, mode) as fin:
              return fin.read()
        except:
            return "0"
            
 def writeFile(self,filename, contents, mode="wt"):#from course notes
#writes the highScore into the file
    # wt = "write text"
        with open(filename, mode) as fout:
            fout.write(contents)
    
 def run(self):#runs the level
    self.initAnimation()
    if(len(self.wallList)<3):
        self.tries = 3
    else:
        self.tries = len(self.wallList)
    while not self.done and not self.back:
            if(self.tries==0):
                self.endFlag=1 
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            self.done = True
                    if event.type == pygame.USEREVENT+1 and self.MouseReleased and self.endFlag==0 and self.menu==0:
                        self.onTimerFired()
                    if (event.type == pygame.MOUSEBUTTONDOWN or self.MousePressed):
                        self.onMousePressed() 
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.onMouseReleased()
                        
            self.display()
            
    pygame.mixer.music.load("BackGround Music.mp3") 
    pygame.mixer.music.play(-1)        
    if(self.done==True):        
        pygame.quit()
        
class LevelTwo(object):#displays the second level 
 def __init__(self,width,height):
     self.screen = pygame.display.set_mode((width, height))
     #creates a screen
     self.font = pygame.font.Font(None, 18)
     #defines a font to display in-game stats
     self.endFont = pygame.font.Font(None, 36)
     #defines a font to display end game details
     self.endFlag=0#checks if the level is over
     self.tries=0#indicates no. of tries the user has
     self.wallList=[]
     wall1=Wall((204,102,0),(290,40),10,85)
     wall2=Wall((204,102,0),(200,130),10,80)
     wall3=Wall((204,102,0),(200,210),80,10)
     wall4=Wall((204,102,0),(270,125),40,10)
     self.wallList.append(wall1)
     self.wallList.append(wall2)
     self.wallList.append(wall3)
     self.wallList.append(wall4)
     self.target=Target((255,0,0),(330,200),30)
     #creates all obstacles and goals in the level
     self.image = pygame.image.load("background.png").convert()
     self.imagerect = self.image.get_rect()
    #loads background image and gets rectangle associated with it
     self.highScore=int(self.readFile("Level2HighScore.txt"))
     #gets highscore from the file

 def initAnimation(self):                
    self.circle=Bird((0,255,0),(30,200),15)#creates a bird object
    self.screenXSize,self.screenYSize=self.screen.get_size()
    #gets width and height of screen
    self.initBomb()
    self.MousePressed=False 
    self.MouseDown=False 
#checks if the mouse is pressed or not
    self.MouseReleased=False
#checks if the mouse is pressed or not 
    self.done = False
#checks if user closed the window or not
    self.score=0#keeps track of score
    self.stopFlag=0#checks if a try is over or not
    self.back=False#checks if user pressed the back button or not
    self.menu=0#checks if user pressed the menu button
    self.endMusicFlag=0#checks if the music at end level has been played or not
    self.result=None#checks if the bomb collided with something
    pygame.mixer.music.load("Red Bird noise.mp3")
    
 def initBomb(self):#initializes a bomb object 
     self.bomb=Bomb((random.randint(self.circle.rect.x+40,self.circle.rect.x+100),0),15)
    
 def highlightButtons(self):#highlights all buttons in the level
     pos=pygame.mouse.get_pos()
     if(self.menu==1):
        if(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=60)and(pos[1]>=20):  
            pygame.draw.rect(self.screen,(255,0,0),(5,15,70,50))
        elif(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=130)and(pos[1]>=90):
            pygame.draw.rect(self.screen,(255,0,0),(5,85,70,50))
        elif(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=200)and(pos[1]>=160):
            pygame.draw.rect(self.screen,(255,0,0),(5,155,70,50))
        elif(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=270)and(pos[1]>=230):
            pygame.draw.rect(self.screen,(255,0,0),(5,225,70,50))
     elif(self.endFlag==1):
        if(pos[0]>=200)and(pos[0]<=260)and(pos[1]<=90)and(pos[1]>=50):
             pygame.draw.rect(self.screen,(255,0,0),(195,45,70,50))
        elif(pos[0]>=100)and(pos[0]<=160)and(pos[1]<=90)and(pos[1]>=50):
             pygame.draw.rect(self.screen,(255,0,0),(95,45,70,50))
     elif(pos[0]>=0)and(pos[0]<=50)and(pos[1]<=30)and(pos[1]>=0):
         pygame.draw.rect(self.screen,(255,0,0),(0,0,55,35))
    
 def display(self):#displays all elements in the level
     self.screen.fill((0, 0, 0))
     self.screen.blit(self.image, self.imagerect)
     self.highlightButtons()
     if(self.MouseReleased==False):
         #if mouse isn't released, then draws bounding box around bird
        pygame.draw.lines(self.screen,(0,0,0),True,[(self.circle.initX-30-self.circle.size,self.circle.initY-self.circle.size)
        ,(self.circle.initX+self.circle.size,self.circle.initY-self.circle.size), 
        (self.circle.initX+self.circle.size,self.circle.initY+30+self.circle.size)
        ,(self.circle.initX-30-self.circle.size,self.circle.initY+30+self.circle.size)])
     if(self.MouseReleased==True):
        #checks if the bomb has collided with something and play sound if it has
         self.bomb.display()
         if(self.bomb.collide==True)and(self.bomb.playFlag==0):
             pygame.mixer.music.load("bomb sound.mp3")
             pygame.mixer.music.play()
             self.bomb.playFlag=1
     self.circle.display()
     self.target.display()
     for wall in self.wallList:
         wall.display()
     pygame.draw.rect(self.screen,(200,150,175),(0,0,50,30))
     self.screen.blit(self.font.render("Menu", True, (255,255,255)),(10,10))
     self.screen.blit(self.font.render("Score:"+str(self.score), True, (255,255,255)), (150, 0))
     self.screen.blit(self.font.render("HighScore:"+str(self.highScore), True, (255,255,255)), (235, 0))
     self.screen.blit(self.font.render("Tries:"+str(self.tries), False, (255,255,255)), (350, 0))       
     if(self.endFlag==1):#checks if game is over
        if(self.tries==0):#if out of tries, play lost level sound
            if(self.endMusicFlag==0):
                 pygame.mixer.music.load("Level Lost sound.mp3")
                 pygame.mixer.music.play()
                 self.endMusicFlag=1
            self.screen.blit(self.endFont.render("You Lose", True, (255,255,255)), (100, 100))
        else:#else, plays won level sound
            if(self.endMusicFlag==0):
                 pygame.mixer.music.load("End level sound.mp3")
                 pygame.mixer.music.play()
                 self.endMusicFlag=1
            self.screen.blit(self.endFont.render("You Win", True, (255,255,255)), (100, 100))
            if(self.score>self.highScore):
                self.screen.blit(self.endFont.render("New High Score!", True, (255,0,0)), (80, 130))
        pygame.draw.rect(self.screen,(100,200,150),(100,50,60,40))
        self.screen.blit(self.font.render("Restart", True, (255,255,255)),(110,65))
        pygame.draw.rect(self.screen,(100,200,150),(200,50,60,40))
        self.screen.blit(self.font.render("Back", True, (255,255,255)),(210,65))
     elif(self.menu==1):
        self.displayMenu()
     pygame.display.flip()
     clock.tick(60)
     
 def displayMenu(self):#displays the menu
     pygame.draw.rect(self.screen,(128,128,128),(0,0,100,self.screenYSize))
     self.highlightButtons()
     pygame.draw.rect(self.screen,(100,200,150),(10,20,60,40))
     self.screen.blit(self.font.render("Restart", True, (255,255,255)),(20,30))
     pygame.draw.rect(self.screen,(100,200,150),(10,90,60,40))
     self.screen.blit(self.font.render("Back to", True, (255,255,255)),(20,100))
     self.screen.blit(self.font.render("Game", True, (255,255,255)),(20,115))
     pygame.draw.rect(self.screen,(100,200,150),(10,160,60,40))
     self.screen.blit(self.font.render("Help", True, (255,255,255)),(20,170))
     pygame.draw.rect(self.screen,(100,200,150),(10,230,60,40))
     self.screen.blit(self.font.render("Back to", True, (255,255,255)),(11,240))
     self.screen.blit(self.font.render("Main Menu", True, (255,255,255)),(11,255))
     
 def onTimerFired(self):#carries out events when timer is fired
     if(((self.bomb.time>25)or(((self.bomb.rect.x+2*self.bomb.size<0)or(self.bomb.rect.x>=self.screenXSize))\
        or((self.bomb.rect.y+2*self.bomb.size<0) or(self.bomb.rect.y>=self.screenYSize))))and self.result==None):
#checks if the bomb goes off screen or has exploded more than a certain time ago
#before initializing a new bomb
        self.initBomb()
     for wall in self.wallList:
            if((self.circle.collision(wall)!=False)and(self.circle.speed<2))or(self.circle.bounces>3):
#checks if the bird has collided with a wall at low speed or bounced at a point  
#more than 10 times. If yes, the turn is over.
                self.circle.speed=0
                self.circle.gravity=(0,0)
                self.stopFlag=1
                break
     if(self.stopFlag==0): #if turn isn't over, moves the bird           
        self.circle.move()
        if(self.bomb.collide==False):
            self.bomb.move()
        if(self.result==None):#if bomb hasn't collided with bird, keeps checking
            self.result=self.bomb.collision(self.circle)
        for wall in self.wallList:#checks if anything collides with the walls
            self.circle.wallCollide(wall)
            self.bomb.collision(wall)
        if(self.circle.collision(self.target)==True):
        #if it collides with target, game is over
            self.endFlag=1
        elif(((self.circle.rect.x+2*self.circle.size<0)or(self.circle.rect.x>=self.screenXSize))\
        or(self.circle.rect.y>=self.screenYSize)):
        #if bird goes off screen, turn is over
            self.stopFlag=1
     if(self.tries == 0):#if out of turns, level is over
        self.endFlag=1
     if(self.endFlag==1):#if level is over, assigns score
         if(self.tries==0):
             self.score=0
         else:
             if(self.score==0):
                self.score+=5000+(self.tries-1)*10000
                if(self.score>self.highScore):
#writes into the file if score is greater than highScore & game is over
                    self.writeFile("Level2HighScore.txt",str(self.score))
     elif(self.stopFlag==1):#if game not over but turn is over, resets game
                self.tries-=1
                self.initAnimation()
            
 def onMousePressed(self):#handles all mouse pressed events
     pos=pygame.mouse.get_pos()
     if(((pos[0]-self.circle.rect.x-self.circle.size)**2+(pos[1]-self.circle.rect.y-self.circle.size)**2)**0.5<=self.circle.size) \
     and self.MouseReleased==False and self.tries>0:
    #checks if mouse was pressed inside the bird
         if(self.MousePressed==False):
             self.MousePressed=True 
             self.MouseDown=True 
     if(pos[0]>self.circle.initX-30)and(pos[0]<=self.circle.initX)and \
     (pos[1]<self.circle.initY+30)and(pos[1]>=self.circle.initY)and(self.MouseReleased==False)and self.tries>0:
         #limits the dragging of the bird to a bounding box
            self.circle.rect.x=pos[0]-self.circle.size
            self.circle.rect.y=pos[1]-self.circle.size
            if(self.circle.speed==0):
#makes the speed proportional to the amount dragged and calculates angle of release
                self.circle.speed=1
            elif(self.circle.speed<12):
                self.circle.speed=0.8*(max(abs(pos[0]-self.circle.initX),abs(pos[1]-self.circle.initY)))
            dx=self.circle.initX-self.circle.rect.x-self.circle.size
            dy=self.circle.rect.y+self.circle.size-self.circle.initY
            if(dy==0):
                self.circle.angle=math.pi/2
            else: 
                self.circle.angle=math.atan(float(dx)/dy)
     elif(self.endFlag==1):
#if game is over, checks if restart or back buttons are pressed
        if(pos[0]>=200)and(pos[0]<=260)and(pos[1]<=90)and(pos[1]>=50):
             self.back=True
        elif(pos[0]>=100)and(pos[0]<=160)and(pos[1]<=90)and(pos[1]>=50):
             self.endFlag=0
             if(len(self.wallList)<3):
                 self.tries = 3
             else:
                 self.tries = len(self.wallList)
             self.highScore=int(self.readFile("Level2HighScore.txt"))
             self.initAnimation()
     elif(pos[0]>=0)and(pos[0]<=60)and(pos[1]<=40)and(pos[1]>=0):
#checks if menu button is pressed
         self.menu=1
     elif(self.menu==1):
#if in menu mode, checks if any of the menu buttons are pressed 
        if(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=60)and(pos[1]>=20):  
            self.endFlag=0
            if(len(self.wallList)<3):
                 self.tries = 3
            else:
                 self.tries = len(self.wallList)
            self.highScore=int(self.readFile("Level2HighScore.txt"))
            self.initAnimation()
        elif(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=130)and(pos[1]>=90):
            self.menu=0
        elif(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=200)and(pos[1]>=160):
            HelpScreen(self.screenXSize,self.screenYSize).run()
        elif(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=270)and(pos[1]>=230):
            self.back=True
            
 def onMouseReleased(self):#resets mouse pressed to false & mouse released to true
    if(self.MousePressed==True):
        pygame.mixer.music.play()
        self.MouseReleased=True
        self.MousePressed=False
        self.MouseDown=False
             
 def readFile(self,filename, mode="rt"):#from course notes
#returns the highScore in the file
        try:
           with open(filename, mode) as fin:
              return fin.read()
        except:
            return "0"
            
 def writeFile(self,filename, contents, mode="wt"):#from course notes
#writes the highScore into the file
    # wt = "write text"
        with open(filename, mode) as fout:
            fout.write(contents)
    
 def run(self):#runs the level
    self.initAnimation()
    if(len(self.wallList)<3):
        self.tries = 3
    else:
        self.tries = len(self.wallList)
    while not self.done and not self.back:
            if(self.tries==0):
                self.endFlag=1 
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            self.done = True
                    if event.type == pygame.USEREVENT+1 and self.MouseReleased and self.endFlag==0 and self.menu==0:
                        self.onTimerFired()
                    if (event.type == pygame.MOUSEBUTTONDOWN or self.MousePressed):
                        self.onMousePressed() 
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.onMouseReleased()
         
            self.display()
    pygame.mixer.music.load("BackGround Music.mp3") 
    pygame.mixer.music.play(-1)        
    if(self.done==True):        
        pygame.quit()
            
            
class LevelOne(object):#displays the first level
 def __init__(self,width,height):
     self.screen = pygame.display.set_mode((width, height))
     #creates a screen
     self.font = pygame.font.Font(None, 18)
     #defines a font to display in-game stats
     self.endFont = pygame.font.Font(None, 36)
     #defines a font to display end level details
     self.endFlag=0#checks if the level is over
     self.tries=0#keeps track of number of tries the user has left
     self.wallList=[]
     self.wall1=Wall((204,102,0),(150,150),250,10)
     self.wall2=Wall((204,102,0),(200,210),80,10)
     self.wallList.append(self.wall1)
     self.wallList.append(self.wall2)
     self.target=Target((255,0,0),(350,250),50)
     #initializes all obstacles and target in the game
     self.image = pygame.image.load("background.png").convert()
     self.imagerect = self.image.get_rect()
     #loads the background and gets the rect associated with it
     self.highScore=int(self.readFile("Level1HighScore.txt"))
     #gets the highscore of the level

 def initAnimation(self):                
    self.circle=Bird((0,255,0),(30,200),15)#initializes a bird object
    self.screenXSize,self.screenYSize=self.screen.get_size()
    #width and height of the screen 
    self.initBomb()
    self.MousePressed=False 
    self.MouseDown=False 
#checks if the mouse is pressed or not
    self.MouseReleased=False
#checks if the mouse is released or not
    self.done = False#checks if user quit the window
    self.score=0#keeps track of user's score
    self.stopFlag=0#checks if the turn is over
    self.back=False#checks if user pressed the back button
    self.menu=0#checks if user pressed the menu button
    self.endMusicFlag=0#checks if endlevel music was played
    self.result=None#checks if bomb collided with anything
    pygame.mixer.music.load("Red Bird noise.mp3")
    
 def initBomb(self):#initializes a bomb object
     self.bomb=Bomb((random.randint(self.circle.rect.x+40,self.circle.rect.x+100),0),15)
    
 def highlightButtons(self):#highlights all buttons on the level
     pos=pygame.mouse.get_pos()
     if(self.menu==1):
        if(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=60)and(pos[1]>=20):  
            pygame.draw.rect(self.screen,(255,0,0),(5,15,70,50))
        elif(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=130)and(pos[1]>=90):
            pygame.draw.rect(self.screen,(255,0,0),(5,85,70,50))
        elif(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=200)and(pos[1]>=160):
            pygame.draw.rect(self.screen,(255,0,0),(5,155,70,50))
        elif(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=270)and(pos[1]>=230):
            pygame.draw.rect(self.screen,(255,0,0),(5,225,70,50))
     elif(self.endFlag==1):
        if(pos[0]>=200)and(pos[0]<=260)and(pos[1]<=90)and(pos[1]>=50):
             pygame.draw.rect(self.screen,(255,0,0),(195,45,70,50))
        elif(pos[0]>=100)and(pos[0]<=160)and(pos[1]<=90)and(pos[1]>=50):
             pygame.draw.rect(self.screen,(255,0,0),(95,45,70,50))
     elif(pos[0]>=0)and(pos[0]<=50)and(pos[1]<=30)and(pos[1]>=0):
         pygame.draw.rect(self.screen,(255,0,0),(0,0,55,35))
     
 def display(self):#displays all elements involved in the level
     self.screen.fill((0, 0, 0))
     self.screen.blit(self.image, self.imagerect)
     self.highlightButtons()
     if(self.MouseReleased==False):
         #if mouse isn't released, then draws bounding box around bird
        pygame.draw.lines(self.screen,(0,0,0),True,[(self.circle.initX-30-self.circle.size,self.circle.initY-self.circle.size)
        ,(self.circle.initX+self.circle.size,self.circle.initY-self.circle.size), 
        (self.circle.initX+self.circle.size,self.circle.initY+30+self.circle.size)
        ,(self.circle.initX-30-self.circle.size,self.circle.initY+30+self.circle.size)])
     if(self.MouseReleased==True):
         self.bomb.display()
         if(self.bomb.collide==True)and(self.bomb.playFlag==0):
        #checks if bomb has collided with something. if it has, play sound
             pygame.mixer.music.load("bomb sound.mp3")
             pygame.mixer.music.play()
             self.bomb.playFlag=1
     self.circle.display()
     self.target.display()
     for wall in self.wallList:
         wall.display()
     pygame.draw.rect(self.screen,(200,150,175),(0,0,50,30))
     self.screen.blit(self.font.render("Menu", True, (255,255,255)),(10,10))
     self.screen.blit(self.font.render("Score:"+str(self.score), True, (255,255,255)), (150, 0))
     self.screen.blit(self.font.render("HighScore:"+str(self.highScore), True, (255,255,255)), (235, 0))
     self.screen.blit(self.font.render("Tries:"+str(self.tries), False, (255,255,255)), (350, 0))       
     if(self.endFlag==1):#checks if level is over
        if(self.tries==0):
            if(self.endMusicFlag==0):#if out of tries, play lost level sound
                 pygame.mixer.music.load("Level Lost sound.mp3")
                 pygame.mixer.music.play()
                 self.endMusicFlag=1
            self.screen.blit(self.endFont.render("You Lose", True, (255,255,255)), (100, 100))
        else:#else, play end level sound
            if(self.endMusicFlag==0):
                 pygame.mixer.music.load("End level sound.mp3")
                 pygame.mixer.music.play()
                 self.endMusicFlag=1
            self.screen.blit(self.endFont.render("You Win", True, (255,255,255)), (100, 100))
            if(self.score>self.highScore):
                self.screen.blit(self.endFont.render("New High Score!", True, (255,0,0)), (80, 130))
        pygame.draw.rect(self.screen,(100,200,150),(100,50,60,40))
        self.screen.blit(self.font.render("Restart", True, (255,255,255)),(110,65))
        pygame.draw.rect(self.screen,(100,200,150),(200,50,60,40))
        self.screen.blit(self.font.render("Back", True, (255,255,255)),(210,65))
     elif(self.menu==1):
        self.displayMenu()
     pygame.display.flip()
     clock.tick(60)
     
 def displayMenu(self):#displays the menu
     pygame.draw.rect(self.screen,(128,128,128),(0,0,100,self.screenYSize))
     self.highlightButtons()
     pygame.draw.rect(self.screen,(100,200,150),(10,20,60,40))
     self.screen.blit(self.font.render("Restart", True, (255,255,255)),(20,30))
     pygame.draw.rect(self.screen,(100,200,150),(10,90,60,40))
     self.screen.blit(self.font.render("Back to", True, (255,255,255)),(20,100))
     self.screen.blit(self.font.render("Game", True, (255,255,255)),(20,115))
     pygame.draw.rect(self.screen,(100,200,150),(10,160,60,40))
     self.screen.blit(self.font.render("Help", True, (255,255,255)),(20,170))
     pygame.draw.rect(self.screen,(100,200,150),(10,230,60,40))
     self.screen.blit(self.font.render("Back to", True, (255,255,255)),(11,240))
     self.screen.blit(self.font.render("Main Menu", True, (255,255,255)),(11,255))
     
 def onTimerFired(self):#carries out events when the timer is fired
     if(((self.bomb.time>25)or(((self.bomb.rect.x+2*self.bomb.size<0)or(self.bomb.rect.x>=self.screenXSize))\
        or((self.bomb.rect.y+2*self.bomb.size<0) or(self.bomb.rect.y>=self.screenYSize))))and self.result==None):
#checks if the bomb goes off screen or has exploded more than a certain time ago
#before initializing a new bomb
            self.initBomb()
     for wall in self.wallList:
#checks if the bird has collided with a wall at low speed or bounced at a point  
#more than 10 times. If yes, the turn is over.
            if((self.circle.collision(wall)!=False)and(self.circle.speed<2))or(self.circle.bounces>3):
                self.circle.speed=0
                self.circle.gravity=(0,0)
                self.stopFlag=1
                break
     if(self.stopFlag==0):   #if turn isn't over, moves the bird       
        self.circle.move()
        if(self.bomb.collide==False):
            self.bomb.move()
        if(self.result==None):#if bomb hasn't collided with bird, keeps checking
            self.result=self.bomb.collision(self.circle)
        for wall in self.wallList:#checks if anything has collided with the walls
            self.circle.wallCollide(wall)
            self.bomb.collision(wall)
        if(self.circle.collision(self.target)==True):
        #if it collides with target, game is over
            self.endFlag=1
        elif(((self.circle.rect.x+2*self.circle.size<0)or(self.circle.rect.x>=self.screenXSize))\
        or(self.circle.rect.y>=self.screenYSize)):
         #if bird goes off screen, turn is over
            self.stopFlag=1
     if(self.tries == 0):#if out of tries, level is over
        self.endFlag=1
     if(self.endFlag==1):#if level is over, assigns score
         if(self.tries==0):
             self.score=0
         else:
             if(self.score==0):
                self.score+=5000+(self.tries-1)*10000
                if(self.score>self.highScore):
#writes into the file if score is greater than highScore & game is over
                    self.writeFile("Level1HighScore.txt",str(self.score))
     elif(self.stopFlag==1):#if game not over but turn is over, resets game
                self.tries-=1
                self.initAnimation()
            
 def onMousePressed(self):#handles all mouse pressed events
     pos=pygame.mouse.get_pos()
     if(((pos[0]-self.circle.rect.x-self.circle.size)**2+(pos[1]-self.circle.rect.y-self.circle.size)**2)**0.5<=self.circle.size) \
     and self.MouseReleased==False and self.tries>0:
#checks if mouse was pressed inside the bird
         if(self.MousePressed==False):
             self.MousePressed=True 
             self.MouseDown=True 
     if(pos[0]>self.circle.initX-30)and(pos[0]<=self.circle.initX)and \
     (pos[1]<self.circle.initY+30)and(pos[1]>=self.circle.initY)and(self.MouseReleased==False)and self.tries>0:
    #limits the dragging of the bird to a bounding box
            self.circle.rect.x=pos[0]-self.circle.size
            self.circle.rect.y=pos[1]-self.circle.size
            if(self.circle.speed==0):
#makes the speed proportional to the amount dragged and calculates angle of release
                self.circle.speed=1
            elif(self.circle.speed<12):
                self.circle.speed=0.8*(max(abs(pos[0]-self.circle.initX),abs(pos[1]-self.circle.initY)))
            dx=self.circle.initX-self.circle.rect.x-self.circle.size
            dy=self.circle.rect.y+self.circle.size-self.circle.initY
            if(dy==0):
                self.circle.angle=math.pi/2
            else: 
                self.circle.angle=math.atan(float(dx)/dy)
     elif(self.endFlag==1):
         #if game is over, checks if restart or back buttons are pressed
        if(pos[0]>=200)and(pos[0]<=260)and(pos[1]<=90)and(pos[1]>=50):
             self.back=True
        elif(pos[0]>=100)and(pos[0]<=160)and(pos[1]<=90)and(pos[1]>=50):
             self.endFlag=0
             if(len(self.wallList)<3):
                 self.tries = 3
             else:
                 self.tries = len(self.wallList)
             self.highScore=int(self.readFile("Level1HighScore.txt"))
             self.initAnimation()
     elif(pos[0]>=0)and(pos[0]<=60)and(pos[1]<=40)and(pos[1]>=0):
    #checks if menu button is pressed
         self.menu=1
     elif(self.menu==1):
         #if in menu mode, checks if any menu button is pressed
        if(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=60)and(pos[1]>=20):  
            self.endFlag=0
            if(len(self.wallList)<3):
                 self.tries = 3
            else:
                 self.tries = len(self.wallList)
            self.highScore=int(self.readFile("Level1HighScore.txt"))
            self.initAnimation()
        elif(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=130)and(pos[1]>=90):
            self.menu=0
        elif(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=200)and(pos[1]>=160):
            HelpScreen(self.screenXSize,self.screenYSize).run()
        elif(pos[0]>=10)and(pos[0]<=70)and(pos[1]<=270)and(pos[1]>=230):
            self.back=True
            
 def onMouseReleased(self):#resets mouse pressed to false & mouse released to true
    if(self.MousePressed==True):
        pygame.mixer.music.play() 
        self.MouseReleased=True
        self.MousePressed=False
        self.MouseDown=False
             
 def readFile(self,filename, mode="rt"):#from course notes
#returns the highScore in the file
        try:
           with open(filename, mode) as fin:
              return fin.read()
        except:
            return "0"
            
 def writeFile(self,filename, contents, mode="wt"):#from course notes
#writes the highScore into the file
    # wt = "write text"
        with open(filename, mode) as fout:
            fout.write(contents)
    
 def run(self):#runs the level
    self.initAnimation()
    if(len(self.wallList)<3):
        self.tries = 3
    else:
        self.tries = len(self.wallList)
    while not self.done and not self.back:
            if(self.tries==0):
                self.endFlag=1 
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            self.done = True
                    if event.type == pygame.USEREVENT+1 and self.MouseReleased and self.endFlag==0 and self.menu==0:
                        self.onTimerFired()
                    if (event.type == pygame.MOUSEBUTTONDOWN or self.MousePressed):
                        self.onMousePressed() 
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.onMouseReleased()
         
            self.display()
            
    pygame.mixer.music.load("BackGround Music.mp3")
    pygame.mixer.music.play(-1)             
    if(self.done==True):        
        pygame.quit()
            
class LevelEditor(object):
 def __init__(self,width,height,num):
     self.screen = pygame.display.set_mode((width, height))
     self.width=width
     self.height=height
     self.font = pygame.font.Font(None, 18)
     self.image = pygame.image.load("background.png").convert()
     self.imagerect = self.image.get_rect()
     self.num=num
     
 def checkAllObjects(self,pos):#checks if mouse was pressed in any object
     for i in xrange(len(self.objectList)):
         if(isinstance(self.objectList[i],Wall)==True):
             if(pos[0]<=self.objectList[i].x+self.objectList[i].width)and(pos[0]>=self.objectList[i].x)\
             and(pos[1]<=self.objectList[i].y+self.objectList[i].height)and(pos[1]>=self.objectList[i].y):
                 if(self.deleteMode==False):
                     self.currentObj=self.objectList[i]
                 else:
                     self.objectList.remove(self.objectList[i])
                 return True
         elif(isinstance(self.objectList[i],Target)==True):
             if(((pos[0]-self.objectList[i].x)**2+(pos[1]-self.objectList[i].y)**2)**0.5<=self.objectList[i].size):
                 if(self.deleteMode==False):
                     self.currentObj=self.objectList[i]
                 else:
                     self.objectList.remove(self.objectList[i])
                 return True
         elif(isinstance(self.objectList[i],Bird)==True):
             if(((pos[0]-self.objectList[i].rect.x-self.objectList[i].size)**2+
             (pos[1]-self.objectList[i].rect.y-self.objectList[i].size)**2)**0.5<=self.objectList[i].size):
                 if(self.deleteMode==False):
                     self.currentObj=self.objectList[i]
                 else:
                     self.objectList.remove(self.objectList[i])
                 return True
     return False
     
 def readFile(self,filename, mode="rt"):#from course notes
#returns the highScore in the file
        try:
           with open(filename, mode) as fin:
              return fin.read()
        except:
            return "0"
     
 def writeFile(self,filename, contents, mode="wt"):#from course notes
#writes the highScore into the file
    # wt = "write text"
        with open(filename, mode) as fout:
            fout.write(contents)
            
 def reloadLevel(self):#gets all objects saved in the file and allows editing
     self.contents=self.readFile("SavedLevel"+self.num+".txt")
     if(self.contents!="0"):
         for line in self.contents.splitlines():
             self.objectList.append(eval(line))
     
 def saveLevel(self):#saves the created objects into a file
     string=""
     for obj in self.objectList:
         string+=obj.__repr__()+"\n"
     self.writeFile("SavedLevel"+self.num+".txt",string)
     
 def highlightButtons(self):#highlights all the buttons in the level editor
     pos=pygame.mouse.get_pos()
     if(pos[0]>=5)and(pos[0]<=65)and(pos[1]<=45)and(pos[1]>=5):
         pygame.draw.rect(self.screen,(255,0,0),(0,0,70,50))
     elif(pos[0]>=135)and(pos[0]<=195)and(pos[1]<=45)and(pos[1]>=5):
         pygame.draw.rect(self.screen,(255,0,0),(130,0,70,50))
     elif(pos[0]>=335)and(pos[0]<=395)and(pos[1]<=45)and(pos[1]>=5):
         pygame.draw.rect(self.screen,(255,0,0),(330,0,70,50))
     elif(pos[0]>=70)and(pos[0]<=130)and(pos[1]<=45)and(pos[1]>=5):
         pygame.draw.rect(self.screen,(255,0,0),(65,0,70,50))
     elif(pos[0]>=270)and(pos[0]<=330)and(pos[1]<=45)and(pos[1]>=5):
         pygame.draw.rect(self.screen,(255,0,0),(265,0,70,50))
     elif(pos[0]>=200)and(pos[0]<=260)and(pos[1]<=45)and(pos[1]>=5):
         pygame.draw.rect(self.screen,(255,0,0),(195,0,70,50))
     elif(pos[0]>=5)and(pos[0]<=65)and(pos[1]<=87)and(pos[1]>=47):
         pygame.draw.rect(self.screen,(255,0,0),(0,42,70,50))
     elif(pos[0]>=335)and(pos[0]<=395)and(pos[1]<=87)and(pos[1]>=47):
         pygame.draw.rect(self.screen,(255,0,0),(330,42,70,50))
     elif(pos[0]>=270)and(pos[0]<=330)and(pos[1]<=87)and(pos[1]>=47):
         pygame.draw.rect(self.screen,(255,0,0),(265,42,70,50))
     elif(pos[0]>=70)and(pos[0]<=130)and(pos[1]<=87)and(pos[1]>=47):
         pygame.draw.rect(self.screen,(255,0,0),(65,42,70,50))
     
 def onMousePressed(self):#handles all mouse pressed events
     pos=pygame.mouse.get_pos()
     if(pos[0]>=5)and(pos[0]<=65)and(pos[1]<=45)and(pos[1]>=5):
         self.makeWall()
         self.deleteMode=False
     elif(pos[0]>=135)and(pos[0]<=195)and(pos[1]<=45)and(pos[1]>=5):
         self.makeTarget()
         self.deleteMode=False
     elif(pos[0]>=335)and(pos[0]<=395)and(pos[1]<=45)and(pos[1]>=5):
         self.makeBird()
         self.deleteMode=False
     elif(pos[0]>=70)and(pos[0]<=130)and(pos[1]<=45)and(pos[1]>=5):
         self.increaseDimension()
         self.deleteMode=False
     elif(pos[0]>=270)and(pos[0]<=330)and(pos[1]<=45)and(pos[1]>=5):
         self.decreaseDimension()
         self.deleteMode=False
     elif(pos[0]>=200)and(pos[0]<=260)and(pos[1]<=45)and(pos[1]>=5):
         self.deleteMode=True
     elif(pos[0]>=5)and(pos[0]<=65)and(pos[1]<=87)and(pos[1]>=47):
         self.back=True
     elif(pos[0]>=335)and(pos[0]<=395)and(pos[1]<=87)and(pos[1]>=47):
         self.saveLevel()
     elif(pos[0]>=270)and(pos[0]<=330)and(pos[1]<=87)and(pos[1]>=47):
         self.rotateWall()
     elif(pos[0]>=70)and(pos[0]<=130)and(pos[1]<=87)and(pos[1]>=47):
         HelpScreen(self.width,self.height).run()
     elif(isinstance(self.currentObj,Wall)==True)and(pos[0]<=self.currentObj.x+self.currentObj.width)\
     and(pos[0]>=self.currentObj.x)and(pos[1]<=self.currentObj.y+self.currentObj.height)\
     and(pos[1]>=self.currentObj.y):
#if pressed inside a wall, either deletes it if on delete mode or moves it
         if(self.deleteMode==False):
             self.onMouseMotion("MousePressed")
         else:
             self.objectList.remove(self.currentObj)
     elif((isinstance(self.currentObj,Target)==True)and(((pos[0]-self.currentObj.x)**2\
     +(pos[1]-self.currentObj.y)**2)**0.5<=self.currentObj.size)):
#if pressed inside a target either deletes it if on delete mode or moves it
         if(self.deleteMode==False):
             self.onMouseMotion("MousePressed")
         else:
             self.objectList.remove(self.currentObj)
     elif((isinstance(self.currentObj,Bird)==True)and(((pos[0]-self.currentObj.rect.x-self.currentObj.size)**2\
     +(pos[1]-self.currentObj.rect.y-self.currentObj.size)**2)**0.5<=self.currentObj.size)):
#if pressed inside a bird, either deletes it if on delete mode or moves it
         if(self.deleteMode==False):
             self.onMouseMotion("MousePressed")
         else:
             self.objectList.remove(self.currentObj)
     else:
         flag=self.checkAllObjects(pos)
         if(flag==False)or(len(self.objectList)==0):
            self.deleteMode=False
            self.currentObj=None
            
 def rotateWall(self):#makes a wall vertical or horizontal
     if(isinstance(self.currentObj,Wall)==True):
         self.currentObj.width,self.currentObj.height=self.currentObj.height,self.currentObj.width
         if(self.currentObj.rotate==0):
             self.currentObj.rotate=1
         else:
             self.currentObj.rotate=0
         
 def decreaseDimension(self):#reduces the size of wall or target
     if(isinstance(self.currentObj,Wall)==True):
         if(self.currentObj.width>0 and self.currentObj.rotate==0):
             self.currentObj.width-=5
         elif(self.currentObj.height>0 and self.currentObj.rotate==1):
             self.currentObj.height-=5
     elif(isinstance(self.currentObj,Target)==True):
         if(self.currentObj.size>0):
             self.currentObj.size-=5
         
 def increaseDimension(self):#increases the size of wall or target
     if(isinstance(self.currentObj,Wall)==True):
         if(self.currentObj.width<self.screenXSize and self.currentObj.rotate==0):
             self.currentObj.width+=5
         elif(self.currentObj.height<self.screenYSize and self.currentObj.rotate==1):
             self.currentObj.height+=5
     elif(isinstance(self.currentObj,Target)==True):
         if(self.currentObj.size<self.screenXSize):
             self.currentObj.size+=5
             
 def onMouseMotion(self,event):
#if mouse is moved when left button is pressed, moves the current object selected
#with it
     pos=pygame.mouse.get_pos()
     if (event=="MousePressed" or event.buttons[0]==1):
         if((isinstance(self.currentObj,Target)==True)or(isinstance(self.currentObj,Wall)==True)):
             self.currentObj.x = pos[0]
             self.currentObj.y = pos[1]
         elif(isinstance(self.currentObj,Bird)==True):
             self.currentObj.rect.x=pos[0]-self.currentObj.size
             self.currentObj.rect.y=pos[1]-self.currentObj.size
     
 def makeWall(self):#creates a wall object and makes it the current object
     self.objectList.append(Wall((204,102,0),(self.defaultX,self.defaultY),self.defaultWidth,self.defaultHeight))
     self.currentObj=self.objectList[len(self.objectList)-1] 
     
 def makeTarget(self):#creates a target object and makes it the current object
     count=0
     for obj in self.objectList:
         if(isinstance(self.currentObj,Target)==True):
             count+=1
     if(count==0):
         self.objectList.append(Target((255,0,0),(self.defaultX,self.defaultY),self.defaultSize))
         self.currentObj=self.objectList[len(self.objectList)-1] 
     
 def makeBird(self):#creates a bird object and makes it the current object
     count=0
     for obj in self.objectList:
         if(isinstance(self.currentObj,Bird)==True):
             count+=1
     if(count==0):
         self.objectList.append(Bird((0,255,0),(self.defaultX,self.defaultY),self.defaultSize))
         self.currentObj=self.objectList[len(self.objectList)-1] 
     
 def display(self):#displays all elements on the level editor
     self.screen.fill((0, 0, 0))
     self.screen.blit(self.image, self.imagerect)
     self.highlightButtons()
     pygame.draw.rect(self.screen,(100,200,150),(5,5,60,40))
     self.screen.blit(self.font.render("Wall", True, (255,255,255)),(10,15))
     pygame.draw.rect(self.screen,(100,200,150),(135,5,60,40))
     self.screen.blit(self.font.render("Target", True, (255,255,255)), (145,15))
     pygame.draw.rect(self.screen,(100,200,150),(335,5,60,40))
     self.screen.blit(self.font.render("Bird", True, (255,255,255)), (350,15))
     pygame.draw.rect(self.screen,(200,100,125),(70,5,60,40))
     self.screen.blit(self.font.render("Increase", True, (255,255,255)), (75,15))
     self.screen.blit(self.font.render("size", True, (255,255,255)), (75,30))
     pygame.draw.rect(self.screen,(200,100,125),(270,5,60,40))
     self.screen.blit(self.font.render("Decrease", True, (255,255,255)), (273,15))
     self.screen.blit(self.font.render("size", True, (255,255,255)), (275,30))
     pygame.draw.rect(self.screen,(100,200,150),(200,5,60,40))
     self.screen.blit(self.font.render("Delete", True, (255,255,255)), (210,15))
     pygame.draw.rect(self.screen,(230,190,175),(5,47,60,40))
     self.screen.blit(self.font.render("Done", True, (255,255,255)), (10,57))
     pygame.draw.rect(self.screen,(230,190,175),(335,47,60,40))
     self.screen.blit(self.font.render("Save", True, (255,255,255)), (350,57))
     pygame.draw.rect(self.screen,(200,100,125),(270,47,60,40))
     self.screen.blit(self.font.render("Rotate", True, (255,255,255)), (280,57))
     self.screen.blit(self.font.render("Wall", True, (255,255,255)), (285,70))
     pygame.draw.rect(self.screen,(230,190,175),(70,47,60,40))
     self.screen.blit(self.font.render("Help", True, (255,255,255)), (80,57))
     for structure in self.objectList:
         structure.display()
     pygame.display.flip()
     clock.tick(60)
     
 def initAnimation(self):
     self.screenXSize,self.screenYSize=self.screen.get_size()
     self.defaultX=self.screenXSize/2
     self.defaultY=self.screenYSize/2
     #default starting point for all objects
     self.defaultWidth=100
     #default width for a wall
     self.defaultHeight=10
     #default height for a wall
     self.defaultSize=15
     #default radius of bird and target
     self.objectList=[]
     #list of all objects created
     self.done=False#checks if user closed the windows
     self.currentObj=None
     self.deleteMode=False#checks if objects are to be deleted
     self.back=False#checks if the user clicked the done button
     
 def run(self):#runs the level editor
     self.initAnimation()
     self.reloadLevel()
     while not self.done and not self.back:
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 self.done = True
             if event.type == pygame.MOUSEBUTTONDOWN:
                 self.onMousePressed()
             if event.type == pygame.MOUSEMOTION:
                 self.onMouseMotion(event)
         self.display()
     if(self.done==True):    
         pygame.quit()
         
         
class DisplayLevels(object):#displays the levels present in the game
    def __init__(self,width,height):
     self.width=width
     self.height=height
     self.screen = pygame.display.set_mode((width, height))
     
    def initAnimation(self):#initializes variables reqd for this screen
     self.font = pygame.font.Font(None, 18)
     self.done=False
     self.image = pygame.image.load("level screen.jpg").convert()
     self.imagerect = self.image.get_rect()
     self.back=False
     
    def highlightButtons(self):#highlights all buttons on the screen
        pos=pygame.mouse.get_pos()
        if(pos[0]>=80)and(pos[0]<=160)and(pos[1]<=260)and(pos[1]>=220):
            pygame.draw.rect(self.screen,(255,0,0),(75,215,90,50))
        elif(pos[0]>=180)and(pos[0]<=260)and(pos[1]<=260)and(pos[1]>=220):
            pygame.draw.rect(self.screen,(255,0,0),(175,215,90,50))
        elif(pos[0]>=280)and(pos[0]<=360)and(pos[1]<=260)and(pos[1]>=220):
            pygame.draw.rect(self.screen,(255,0,0),(275,215,90,50))
        elif(pos[0]>=360)and(pos[0]<=400)and(pos[1]<=300)and(pos[1]>=270):
            pygame.draw.rect(self.screen,(255,0,0),(355,265,45,35))
     
    def onMousePressed(self):#checks if buttons on screen are pressed or not
        pos=pygame.mouse.get_pos()
        if(pos[0]>=80)and(pos[0]<=160)and(pos[1]<=260)and(pos[1]>=220):
            LevelOne(self.width,self.height).run()
        elif(pos[0]>=180)and(pos[0]<=260)and(pos[1]<=260)and(pos[1]>=220):
            DisplaySaveOptions(self.width,self.height,1).run()
        elif(pos[0]>=280)and(pos[0]<=360)and(pos[1]<=260)and(pos[1]>=220):
            LevelTwo(self.width,self.height).run()
        elif(pos[0]>=360)and(pos[0]<=400)and(pos[1]<=300)and(pos[1]>=270):
            self.back=True
     
    def display(self):#displays all elements on screen
     self.screen.fill((0, 0, 0))
     self.screen.blit(self.image, self.imagerect)
     self.highlightButtons()
     pygame.draw.rect(self.screen,(100,200,150),(80,220,80,40))
     self.screen.blit(self.font.render("Level 1", True, (255,255,255)),(83,230))
     pygame.draw.rect(self.screen,(100,200,150),(280,220,80,40))
     self.screen.blit(self.font.render("Level 2", True, (255,255,255)),(285,230))
     pygame.draw.rect(self.screen,(100,200,150),(180,220,80,40))
     self.screen.blit(self.font.render("Created", True, (255,255,255)),(185,230))
     self.screen.blit(self.font.render("Level", True, (255,255,255)),(185,245))
     pygame.draw.rect(self.screen,(100,200,150),(360,270,40,30))
     self.screen.blit(self.font.render("Back", True, (255,255,255)),(365,280))
     pygame.display.flip()
     clock.tick(60)
     
    def run(self):#runs the display screen
     self.initAnimation()
     while not self.done and not self.back:
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 self.done = True
             if event.type == pygame.MOUSEBUTTONDOWN:
                 self.onMousePressed()
         self.display()
     if(self.done==True):    
         pygame.quit()
         
class DisplaySaveOptions(object):
    def __init__(self,width,height,val):
     self.width=width
     self.height=height
     self.val=val
     self.screen = pygame.display.set_mode((width, height))
     
    def initAnimation(self):#initializes variables reqd for this screen
     self.font = pygame.font.Font(None, 18)
     self.done=False
     if(self.val==0):
         self.image = pygame.image.load("create level background.jpg").convert()
     else:
         self.image = pygame.image.load("create level play.png").convert()
     self.imagerect = self.image.get_rect()
     self.back=False
     
    def highlightButtons(self):#highlights all buttons on the screen
        pos=pygame.mouse.get_pos()
        if(pos[0]>=80)and(pos[0]<=160)and(pos[1]<=260)and(pos[1]>=220):
            pygame.draw.rect(self.screen,(255,0,0),(75,215,90,50))
        elif(pos[0]>=180)and(pos[0]<=260)and(pos[1]<=260)and(pos[1]>=220):
            pygame.draw.rect(self.screen,(255,0,0),(175,215,90,50))
        elif(pos[0]>=280)and(pos[0]<=360)and(pos[1]<=260)and(pos[1]>=220):
            pygame.draw.rect(self.screen,(255,0,0),(275,215,90,50))
        elif(pos[0]>=360)and(pos[0]<=400)and(pos[1]<=300)and(pos[1]>=270):
            pygame.draw.rect(self.screen,(255,0,0),(355,265,45,35))
     
    def onMousePressed(self):#checks if buttons on screen are pressed or not
        pos=pygame.mouse.get_pos()
        if(pos[0]>=80)and(pos[0]<=160)and(pos[1]<=260)and(pos[1]>=220):
            if(self.val==0):
                LevelEditor(self.width,self.height,"1").run()
            else:
                CreatedLevel(self.width,self.height,"1").run()
        elif(pos[0]>=180)and(pos[0]<=260)and(pos[1]<=260)and(pos[1]>=220):
            if(self.val==0):
                LevelEditor(self.width,self.height,"2").run()
            else:
                CreatedLevel(self.width,self.height,"2").run()
        elif(pos[0]>=280)and(pos[0]<=360)and(pos[1]<=260)and(pos[1]>=220):
            if(self.val==0):
                LevelEditor(self.width,self.height,"3").run()
            else:
                CreatedLevel(self.width,self.height,"3").run()
        elif(pos[0]>=360)and(pos[0]<=400)and(pos[1]<=300)and(pos[1]>=270):
            self.back=True
     
    def display(self):#displays all elements on screen
     self.screen.fill((0, 0, 0))
     self.screen.blit(self.image, self.imagerect)
     self.highlightButtons()
     pygame.draw.rect(self.screen,(100,200,150),(80,220,80,40))
     self.screen.blit(self.font.render("Save 1", True, (255,255,255)),(83,230))
     pygame.draw.rect(self.screen,(100,200,150),(280,220,80,40))
     self.screen.blit(self.font.render("Save 3", True, (255,255,255)),(285,230))
     pygame.draw.rect(self.screen,(100,200,150),(180,220,80,40))
     self.screen.blit(self.font.render("Save 2", True, (255,255,255)),(185,230))
     pygame.draw.rect(self.screen,(100,200,150),(360,270,40,30))
     self.screen.blit(self.font.render("Back", True, (255,255,255)),(365,280))
     pygame.display.flip()
     clock.tick(60)
     
    def run(self):#runs the display screen
     self.initAnimation()
     while not self.done and not self.back:
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 self.done = True
             if event.type == pygame.MOUSEBUTTONDOWN:
                 self.onMousePressed()
         self.display()
     if(self.done==True):    
         pygame.quit()
     
class PlayGame(object):#displays intermediate screen 
    def __init__(self,width,height):
     self.width=width
     self.height=height
     self.screen = pygame.display.set_mode((width, height))
     
    def initAnimation(self):#initializes variables reqd in the screen
     self.font = pygame.font.Font(None, 18)
     self.done=False
     self.image = pygame.image.load("start screen.jpg").convert()
     self.imagerect = self.image.get_rect()
     self.back=False
     
    def highlightButtons(self):#highlights all buttons on screen
        pos=pygame.mouse.get_pos()
        if(pos[0]>=80)and(pos[0]<=160)and(pos[1]<=260)and(pos[1]>=220):
            pygame.draw.rect(self.screen,(255,0,0),(75,215,90,50))
        elif(pos[0]>=280)and(pos[0]<=360)and(pos[1]<=260)and(pos[1]>=220):
            pygame.draw.rect(self.screen,(255,0,0),(275,215,90,50))
        elif(pos[0]>=360)and(pos[0]<=400)and(pos[1]<=300)and(pos[1]>=270):
            pygame.draw.rect(self.screen,(255,0,0),(355,265,45,35))
     
    def onMousePressed(self):#checks if any button on screen is pressed
        pos=pygame.mouse.get_pos()
        if(pos[0]>=80)and(pos[0]<=160)and(pos[1]<=260)and(pos[1]>=220):
            DisplaySaveOptions(self.width,self.height,0).run()
        elif(pos[0]>=280)and(pos[0]<=360)and(pos[1]<=260)and(pos[1]>=220):
            DisplayLevels(self.width,self.height).run()
        elif(pos[0]>=360)and(pos[0]<=400)and(pos[1]<=300)and(pos[1]>=270):
            self.back=True
        
    def display(self):#displays the buttons and image
     self.screen.fill((0, 0, 0))
     self.screen.blit(self.image, self.imagerect)
     self.highlightButtons()
     pygame.draw.rect(self.screen,(100,200,150),(80,220,80,40))
     self.screen.blit(self.font.render("Create Level", True, (255,255,255)),(83,230))
     pygame.draw.rect(self.screen,(100,200,150),(280,220,80,40))
     self.screen.blit(self.font.render("Play Levels", True, (255,255,255)),(285,230))
     pygame.draw.rect(self.screen,(100,200,150),(360,270,40,30))
     self.screen.blit(self.font.render("Back", True, (255,255,255)),(365,280))
     pygame.display.flip()
     clock.tick(60)
     
    def run(self):#runs the screen
     self.initAnimation()
     while not self.done and not self.back:
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 self.done = True
             if event.type == pygame.MOUSEBUTTONDOWN:
                 self.onMousePressed()
         self.display()
     if(self.done==True):    
         pygame.quit()
     
class HelpScreen(object):#displays the help screen
    def __init__(self,width,height):
     self.width=width
     self.height=height
     self.screen = pygame.display.set_mode((width, height))
     
    def initAnimation(self):#initializes variables reqd in help screen
     self.font = pygame.font.Font(None, 25)
     self.done=False
     self.image = pygame.image.load("HelpScreen.jpg").convert()
     self.imagerect = self.image.get_rect()
     self.back=False
     
    def display(self):#displays all the instructions
     self.screen.fill((0, 0, 0))
     self.screen.blit(self.image, self.imagerect)
     self.highlightButtons()
     self.screen.blit(self.font.render("Gameplay:", True, (0,255,0)),(10,10))
     self.screen.blit(self.font.render("Click on the bird and drag back to release it", True, (0,255,0)),(10,30))
     self.screen.blit(self.font.render("Try to hit the target by bouncing off the walls", True, (0,255,0)),(10,50))
     self.screen.blit(self.font.render("Level Editor:", True, (0,0,255)),(10,150))
     self.screen.blit(self.font.render("Click on the buttons to create birds, targets", True, (0,0,255)),(10,170))
     self.screen.blit(self.font.render("or walls", True, (0,0,255)),(10,190))
     self.screen.blit(self.font.render("You can create only one bird and target", True, (0,0,255)),(10,210))
     self.screen.blit(self.font.render("When you are done creating your level, save it", True, (0,0,255)),(10,230))
     self.screen.blit(self.font.render("The done button will take you back to the", True, (0,0,255)),(10,250))
     self.screen.blit(self.font.render("main menu", True, (0,0,255)),(10,270))
     pygame.draw.rect(self.screen,(100,200,150),(360,270,40,30))
     self.screen.blit(self.font.render("Back", True, (255,255,255)),(365,280))
     pygame.display.flip()
     clock.tick(60)
     
    def highlightButtons(self):#highlights all buttons on the screen
     pos=pygame.mouse.get_pos()
     if(pos[0]>=360)and(pos[0]<=400)and(pos[1]<=300)and(pos[1]>=270):
         pygame.draw.rect(self.screen,(255,0,0),(355,265,45,35))
     
    def onMousePressed(self):#checks if any of the buttons on screen are pressed
     pos=pygame.mouse.get_pos()
     if(pos[0]>=360)and(pos[0]<=400)and(pos[1]<=300)and(pos[1]>=270):
         self.back=True
     
    def run(self):#runs the screen 
     self.initAnimation()
     while not self.done and not self.back:
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 self.done = True
             if event.type == pygame.MOUSEBUTTONDOWN:
                 self.onMousePressed()
         self.display()
     if(self.done==True):    
         pygame.quit()
    
    
class Game(object):#starts the game
 def __init__(self,width,height):
     self.width=width
     self.height=height
     self.screen = pygame.display.set_mode((width, height))
     pygame.mixer.music.load("BackGround Music.mp3")
     
 def initAnimation(self):#initializes variables reqd in the start screen
     self.font = pygame.font.Font(None, 18)
     self.done=False
     self.image = pygame.image.load("newstartscreen.jpg").convert()
     pygame.mixer.music.play(-1)
     self.imagerect = self.image.get_rect()
     self.back=False
     
 def highlightButtons(self):#highlights buttons
     pos=pygame.mouse.get_pos()
     if(pos[0]>=80)and(pos[0]<=160)and(pos[1]<=260)and(pos[1]>=220):
        pygame.draw.rect(self.screen,(255,0,0),(75,215,90,50))
     elif(pos[0]>=280)and(pos[0]<=360)and(pos[1]<=260)and(pos[1]>=220):
         pygame.draw.rect(self.screen,(255,0,0),(275,215,90,50))
     elif(pos[0]>=360)and(pos[0]<=400)and(pos[1]<=300)and(pos[1]>=270):
         pygame.draw.rect(self.screen,(255,0,0),(355,265,45,35))
     
 def onMousePressed(self):#checks if the mouse is pressed in any of the buttons
   pos=pygame.mouse.get_pos()
   if(pos[0]>=0)and(pos[0]<=self.width)and(pos[1]>=0)and(pos[1]<=self.height):
     if(pos[0]>=80)and(pos[0]<=160)and(pos[1]<=260)and(pos[1]>=220):
         PlayGame(self.width,self.height).run()
     elif(pos[0]>=280)and(pos[0]<=360)and(pos[1]<=260)and(pos[1]>=220):
         HelpScreen(self.width,self.height).run()
     elif(pos[0]>=360)and(pos[0]<=400)and(pos[1]<=300)and(pos[1]>=270):
         self.back=True
     
 def display(self):#displays all buttons
     self.screen.fill((0, 0, 0))
     self.screen.blit(self.image, self.imagerect)
     self.highlightButtons()
     pygame.draw.rect(self.screen,(100,200,150),(80,220,80,40))
     self.screen.blit(self.font.render("Play Game", True, (255,255,255)),(90,230))
     pygame.draw.rect(self.screen,(100,200,150),(280,220,80,40))
     self.screen.blit(self.font.render("Help Screen", True, (255,255,255)),(285,230))
     pygame.draw.rect(self.screen,(100,200,150),(360,270,40,30))
     self.screen.blit(self.font.render("Quit", True, (255,255,255)),(365,280))
     pygame.display.flip()
     clock.tick(60)
     
 def run(self):#runs the program
     self.initAnimation()
     while not self.done and not self.back:
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 self.done = True
             if event.type == pygame.MOUSEBUTTONDOWN:
                 self.onMousePressed()
             
         self.display()
     pygame.quit()
     
game=Game(400,300)
game.run()
