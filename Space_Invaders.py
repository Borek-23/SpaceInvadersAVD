import sys
import pygame
import Invader
import Missile
from pygame.locals import *

#Define colour for converting asstets to get rid of their background
WHITE = (255, 255, 255)

class SpaceInvaders:

    # Constructor of the basic game class.
    # This constructor calls initialize and main_loop method.
    def __init__(self):
        self.initialize()
        self.main_loop()
        import Invader

    # Initialization method. Allows the game to initialize different
    # parameters and load assets before the game runs
    def initialize(self):
        pygame.init()
        pygame.key.set_repeat(1, 1)

        self.width = 1024
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.caption = "Space Invader!"
        pygame.display.set_caption(self.caption)
                
        self.framerate = 30

        self.clock = pygame.time.Clock()
        #Set game state        
        self.gameState = 1

        self.font = pygame.font.Font(None, 40)

        #Load intial sounds they are present from begining of gameplay
        self.explosionSound = pygame.mixer.Sound("explosion.wav")
        self.shootSound = pygame.mixer.Sound("shoot.wav")
        self.fastinvader1Sound = pygame.mixer.Sound("fastinvader1.wav")

        #Initialize game state method
        self.initializeGameVariables()

    def initializeGameVariables(self):
        self.starfieldImg = pygame.image.load('n_star.png')
        self.invaderImg = pygame.image.load('inv_1a.png').convert()
        self.invader2 = pygame.image.load('inv_2a.png').convert()
        self.invader3 = pygame.image.load('inv_3a.png').convert()
        self.invader4 = pygame.image.load('inv_4a.png').convert()
        self.invader5 = pygame.image.load('inv_5a.png').convert()
        self.rocketLauncherImg = pygame.image.load('launcher.png').convert()        
        self.missileImg = pygame.image.load('bullet.png')

        self.invaderImg.set_colorkey(WHITE)
        self.invader2.set_colorkey(WHITE)
        self.invader3.set_colorkey(WHITE)
        self.invader4.set_colorkey(WHITE)
        self.invader5.set_colorkey(WHITE)
        self.rocketLauncherImg.set_colorkey(WHITE)

        self.rocketXPos = 512

        self.alienDirection = -1            
        self.alienSpeed = 25

        self.ticks = 0

        self.AlreadySpeedUp = False
        #Initialize list of invaders
        self.invaders = []

        #Set invaders and rows
        self.noInvaders = 11
        self.noRows = 5
        #Set intial position of invaders y,x
        xPos = 250
        yPos = 75
        #Now generate invaders using for loop
        for j in range(self.noRows):
            for i in range(self.noInvaders):
                invader = Invader.Invader() #Attribute variable to the class Invader
                invader.setPosX(xPos) #Setting X position of the FIRST invader
                invader.setPosY(yPos) #Setting Y position of invaders
                self.invaders.append(invader) #Adding invaders to the list
                xPos += 32 #Movement of an invader in X axis
            yPos += 40
            xPos = 250

        self.missileFired = None

        self.playerScore = 0

        self.playerLives = 4

        
    # main loop method keeps the game running. This method continuously
    # calls the update and draw methods to keep the game alive.
    def main_loop(self):
        self.clock = pygame.time.Clock()
        while True:
            gametime = self.clock.get_time()
            self.update(gametime)
            self.draw(gametime)
            self.clock.tick(self.framerate)
            
     # Update method contains game update logic, such as updating the game
    # variables, checking for collisions, gathering input, and
    # playing audio.
    def update(self, gametime):        
        if self.gameState == 1:
            self.updateStarted(gametime)
        elif self.gameState == 2:
            self.updatePlaying(gametime)
        elif self.gameState == 3:
            self.updateEnded(gametime)
    
    def updateStarted(self, gametime):
        events = pygame.event.get()
        #Searching for player keyboard input and making S key setting
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.gameState = 2
                elif event.key == pygame.K_END:
                    pygame.quit()
                    sys.exit()
                    break

    def updatePlaying(self, gametime):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_END:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RIGHT:
                    self.rocketXPos = self.rocketXPos + 6
                elif event.key == pygame.K_LEFT:
                    self.rocketXPos = self.rocketXPos - 6
                elif event.key == pygame.K_SPACE and self.missileFired == None:
                    self.missileFired = Missile.Missile(self.rocketXPos, 650)
                    self.shootSound.play()
                    self.missileFired.move()


        isInvaderRemaining = False
        for i in range(self.noInvaders * self.noRows):
            if self.invaders[i] != None:
                isInvaderRemaining = True
                break
        if isInvaderRemaining == False:
            self.gameState = 3
            return
        #Checking if missile fired and waiting for it to disappear first
        if self.missileFired != None:
            self.missileFired.move()
            if self.missileFired.getPosY() < -10:
                self.missileFired = None
        
        #Position of rocket launcher going through the screen
        if self.rocketXPos < 100:
            self.rocketXPos = 100
            self.rocketXPos = 924

        if self.rocketXPos > 924:
            self.rocketXPos = 924
            self.rocketXPos = 100

        self.ticks = self.ticks + gametime

        if self.ticks > 500:

            # Movements of rows of invaders
            for i in range(self.noInvaders * self.noRows):
                if self.invaders[i] is not None:
                    self.invaders[i].moveHorizontal(self.alienSpeed * self.alienDirection)

                self.fastinvader1Sound.play()

            leftMostInvader = None
            rightMostInvader = None

            #To detect whether there are any invaders left in row
            for i in range(self.noInvaders):
                if self.invaders[i] != None:
                    leftMostInvader = self.invaders[i]
                    break
                
            for i in range(self.noInvaders -1, -1, -1):
                if self.invaders[i] != None:
                    rightMostInvader = self.invaders[i]
                    break

            PosX = 100
            if leftMostInvader.getPosX() < 100:
                self.alienDirection = +1

                xPos = 100
                for i in range(self.noInvaders * self.noRows):
                    if self.invaders[i] != None:
                        self.invaders[i].moveVertical(8)
                        #self.invaders[i].setPosX(xPos)
                    xPos = xPos + self.invaderImg.get_width()

            if rightMostInvader.getPosX() > 924:
                self.alienDirection = -1

                xPos = 924 - self.invaderImg.get_width() * 11
                for i in range(self.noInvaders * self.noRows):
                    if self.invaders[i] != None:
                        self.invaders[i].moveVertical(8)
                        #self.invaders[i].setPosX(xPos)
                    xPos = xPos + self.invaderImg.get_width()

            #Making invaders speed up when the reach certain Y point on Y axis
            if self.AlreadySpeedUp == False:
                for i in range((self.noRows * self.noInvaders) - 1, -1, -1):
                    if self.invaders[i] is not None:
                        if int(self.invaders[i].getPosY()) > 400:
                            self.alienSpeed += 15
                            self.AlreadySpeedUp = True
                            break
                        
            self.ticks = 0
        
        #Collision detection
        if self.missileFired != None:
            rectMissile = pygame.Rect(self.missileFired.getPosX(), self.missileFired.getPosY(), self.missileImg.get_width(), self.missileImg.get_height())
            for i in range((self.noInvaders * self.noRows)-1, -1, -1):
                if self.invaders[i] is not None:
                        rectInvader = pygame.Rect(self.invaders[i].getPosX(), self.invaders[i].getPosY(), self.invaderImg.get_width(), self.invaderImg.get_height())
                        if rectMissile.colliderect(rectInvader):
                            self.missileFired = None
                            self.invaders[i] = None

                            self.playerScore = self.playerScore + 100

                            self.explosionSound.play()
                            break

        
    def updateEnded(self, gametime):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_END:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    self.initializeGameVariables()
                    self.gameState = 1

     # Draw method, draws the current state of the game on the screen                        
    def draw(self, gametime):              
        if self.gameState == 1:
            self.drawStarted(gametime)
        elif self.gameState == 2:
            self.drawPlaying(gametime)
        elif self.gameState == 3:
            self.drawEnded(gametime)

    def drawStarted(self, gametime):
        self.screen.blit(self.starfieldImg, (0, 0))

        width, height = self.font.size("S P A C E   I N V A D E R S!")
        text = self.font.render("S P A C E   I N V A D E R S!", True, (64, 224, 208))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos, 75))

        width, height = self.font.size("INSTRUCTIONS:")
        text = self.font.render("INSTRUCTIONS:", True, (205, 92, 92))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos, 250))

        width, height = self.font.size("PRESS  '<--'  TO  GO  LEFT  ;  PRESS  '-->'  TO  GO  RIGHT")
        text = self.font.render("PRESS  '<--'  TO  GO  LEFT  ;  PRESS  '-->'  TO  GO  RIGHT", True, (205, 92, 92))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos, 300))

        width, height = self.font.size("PRESS  'SPACE BAR'  TO  SHOOT")
        text = self.font.render("PRESS  'SPACE BAR'  TO  SHOOT", True, (205, 92, 92))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos, 340))

        width, height = self.font.size("P R E S S   'S'   T O   S T A R T")
        text = self.font.render("P R E S S   'S'   T O   S T A R T", True, (34, 139, 34))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos, 500))

        width, height = self.font.size("P R E S S   'END'   T O   Q U I T")
        text = self.font.render("P R E S S   'E N D'   T O   Q U I T", True, (208, 32, 144))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos, 560))

        pygame.display.flip()
        

    def drawPlaying(self, gametime):
        self.screen.blit(self.starfieldImg, (0,0))
        #Drawing the score 
        score_text = self.font.render("Score : %d" %self.playerScore, True, (0, 0, 255))
        self.screen.blit(score_text, (15, 15))
        #Drawing lives by another drawing method
        self.screen.blit(self.font.render("Lives: {}".format(self.playerLives), 1, (0, 0, 255)), (385, 15))
        
        self.screen.blit(self.rocketLauncherImg, (self.rocketXPos, 668))
        if self.missileFired != None:
            self.screen.blit(self.missileImg, (self.missileFired.getPosX(), self.missileFired.getPosY() - self.missileImg.get_height()))
 
        #Drawing different alien for each row of invaders
        for i in range(self.noRows * self.noInvaders):
                if self.invaders[i] is not None:
                    if i <  11:
                        self.screen.blit(self.invaderImg, self.invaders[i].getPosition())
                    elif i < 22:
                         self.screen.blit(self.invader2, self.invaders[i].getPosition())
                    elif i < 33:
                        self.screen.blit(self.invader3, self.invaders[i].getPosition())
                    elif i < 44:
                        self.screen.blit(self.invader4, self.invaders[i].getPosition())
                    elif i < 55:
                        self.screen.blit(self.invader5, self.invaders[i].getPosition())
        
        pygame.display.flip()
               

    def drawEnded(self, gametime):
        self.screen.blit(self.starfieldImg, (0, 0))

        width, height = self.font.size("P L A Y   A G A I N , O R   G I V E   U P ?")
        text = self.font.render("P L A Y   A G A I N , O R   G I V E   U P ?", True, (64, 224, 208))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos, 100))

        width, height = self.font.size("P R E S S   'R'   T O   R E S T A R T")
        text = self.font.render("P R E S S   'R'   T O   R E S T A R T", True, (34, 139, 34))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos, 300))

        width, height = self.font.size("P R E S S   'END'   T O   Q U I T")
        text = self.font.render("P R E S S   'E N D'   T O   Q U I T", True, (208, 32, 144))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos, 380))

        score_text = self.font.render("Score : %d" %self.playerScore, True, (0, 0, 255))
        xPos = (1024 - width)/2
        self.screen.blit(score_text, (xPos, 512))

        pygame.display.flip()


if __name__ == "__main__":
    game = SpaceInvaders()
