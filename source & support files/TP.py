
from __future__ import with_statement # for Python 2.5 and 2.6
import contextlib # for urllib.urlopen()
import urllib
import os
import pygame
import random
import copy

black = (0, 0, 0)
white = (255, 255, 255)
blue = ( 139, 69, 19)
red = ( 225, 182, 193)
green = ( 0, 255, 0)
pink = (199,21,133)
purple = (221,160,221)

class LittleYellowsAdventure():
    def init(self):
        pygame.init()
        self.subInit1()
        self.subInit2()
        self.subInit3()
        self.subInit4()
        
    def run(self):
        
        clock = pygame.time.Clock()
        self.soundBgm.play(-1)
        while not self.exitGame:
            
            if self.gameStart==False and self.goToResult==False:
                self.beforeStart()

            if self.gameStart:
                self.removeUseless()
                self.canvas.blit(self.bgImage,self.bgLoc)
                if self.goToResult:
                    self.showResult()
                    if (event.type==pygame.MOUSEBUTTONDOWN and 
                        self.restartButton3.collidepoint
                        (pygame.mouse.get_pos())):
                            self.restart()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exitGame = True
                    if event.type==pygame.MOUSEBUTTONDOWN and self.gameover:
                        if (self.restartButton1.collidepoint(pygame.mouse.get_pos())):
                            self.restart()
                        if self.continueButton2.collidepoint(
                            pygame.mouse.get_pos()):
                            self.goToResult = True
                            self.showResult()
                    if event.type == pygame.KEYDOWN and self.gameover:
                        if event.key == pygame.K_RIGHT:
                            self.goToResult = True
                            self.showResult()
                        if event.key==pygame.K_r:
                            self.gameover = False
                            self.goToResult = False
                            self.init()
                    if event.type==pygame.MOUSEBUTTONDOWN and not self.gameover:
                        if (self.restartButton4.collidepoint(
                            pygame.mouse.get_pos())):
                            self.init()
                        if (self.pauseButton.collidepoint(
                            pygame.mouse.get_pos())):
                            self.isPause = not (self.isPause)
                    if (event.type == pygame.KEYDOWN and not self.gameover 
                    and not self.isPause):
                        if event.key == pygame.K_SPACE:
                            self.addBullet(self.player,self.bulletList,
                                self.facingRight,self.facingLeft)
                            self.soundShoot.play()
                        if event.key == pygame.K_RIGHT:
                            if (self.ground7.rect.right<=self.canvasWidth):
                                self.toTheEnd = True
                                self.player.isWalking
                            if (self.bgShift> self.bgLength-self.canvasWidth or 
                                self.player.rect.x<self.canvasWidth/2):
                                self.player.isWalking=True
                            else:  
                                self.playerHitSth()
                        if event.key == pygame.K_LEFT:
                            smallMinusValue = -1
                            self.player.vx = smallMinusValue
                            self.player.isWalking=True
                        if event.key==pygame.K_r:
                            self.init()
                        
                        if event.key == pygame.K_UP:
                            
                            if self.player.isJumpDown==False:
                                self.player.isJumpUp=True
                                self.soundJump.play()
                    if event.type == pygame.KEYUP:
                        if (event.key == pygame.K_RIGHT or 
                            event.key == pygame.K_LEFT):
                            self.player.isWalking=False
                            self.bgIsShifting=False
                            self.bgShiftV=0
                            self.bgShift=0
                            self.player.goToBgShift = False
                            self.player.vx=0
                            self.toTheEnd = False

                playerHitEnemy = pygame.sprite.spritecollide(self.player,
                    self.enemyList,False)
                if not self.gameover and not self.isPause:
                    self.timerCount()
                self.canvasAni()
                
                self.keysAndFlagScreen()
                    
                self.frogAni()
                


                if not self.isFreeMode:
                    self.gameoverFunc()
                self.gameoverAndWinScreen()
                
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
    def keysAndFlagScreen(self):
        self.drawPlatformGreen=False
        self.drawPlatformRed=False
        self.drawPlatformYellow=False
        self.drawFlag = False
        playerHitFruit = pygame.sprite.spritecollide(self.player,
            self.fruitList,True)
        if len(playerHitFruit)>0:
            for fruit in playerHitFruit:
                self.score+=1
                if isinstance(fruit,GreenKey):
                    self.getGreenKey=True
                    self.drawPlatformGreen = True
                if isinstance(fruit,RedKey):
                    self.getRedKey=True
                    self.drawPlatformRed = True
                if isinstance(fruit,YellowKey):
                    self.getYellowKey=True
                    self.drawPlatformYellow = True
                if isinstance(fruit,BlueKey):
                    self.drawFlag = True
                if isinstance(fruit,Flag):
                    self.getFlag = True
        if self.getFlag and self.switchToBossMode==False:
            self.bossModeFunc()
            self.switchToBossMode = True
        if self.drawPlatformGreen:
            
            self.platformGreen = self.getPlatform(self.ground7.rect.x+100,
                self.ground7.rect.top-self.player.rect.height)
            self.platformList.add(self.platformGreen)
            
            self.redKey = RedKey()
            self.redKey.rect.x = self.platformGreen.rect.x + \
            self.platformGreen.rect.width/2
            self.redKey.rect.bottom = self.platformGreen.rect.top
            self.fruitList.add(self.redKey)
            self.drawPlatformGreen = False
        if self.drawPlatformRed:
            
            self.platformRed = self.getPlatform(self.platformGreen.rect.left+
                self.platformGreen.rect.width*3/4,self.platformGreen.rect.top-
                self.player.rect.height*1.5)
            self.platformList.add(self.platformRed)
            
            self.yellowKey = YellowKey()
            self.yellowKey.rect.x = self.platformRed.rect.x + \
            self.platformRed.rect.width/2
            self.yellowKey.rect.bottom = self.platformRed.rect.top
            self.fruitList.add(self.yellowKey)
            self.drawPlatformRed = False
        if self.drawPlatformYellow:
            self.platformYellow = self.getPlatform(self.platformGreen.rect.left-
                self.platformGreen.rect.width*3/4,self.platformGreen.rect.top-
                self.player.rect.height*1.5)
            self.platformList.add(self.platformYellow)
            self.blueKey = BlueKey()
            self.blueKey.rect.x = self.platformYellow.rect.x +\
             self.platformRed.rect.width/2
            self.blueKey.rect.bottom = self.platformRed.rect.top
            self.fruitList.add(self.blueKey)
            
            self.drawPlatformRed = False
        if self.drawFlag:
            self.flag = Flag()
            self.flag.rect.x = self.platformGreen.rect.x + \
            self.platformRed.rect.width/2
            self.flag.rect.bottom = self.platformYellow.rect.top - 150
            self.fruitList.add(self.flag)
            self.drawFlag=False


        self.progressScreen()
                
        if not self.goToResult:
            if self.getFlag:
                for bullet in self.bulletList:
                    if isinstance(bullet,VerticalBullet):
                        self.bulletList.remove(bullet)
                self.platformList.remove(self.platformGreen)
                self.platformList.remove(self.platformRed)
                self.platformList.remove(self.platformYellow)
                self.platformList.remove(self.floatingPlatform3)
                for fruit in self.fruitList:
                    self.fruitList.remove(fruit)
                textString2 = "Frog Blood"
                text2 = self.font.render(textString2, True, red)
                self.canvas.blit(text2, [self.canvasWidth-320,180])
                textString2 = "Little Yellow Blood"
                text2 = self.font.render(textString2, True, red)
                self.canvas.blit(text2, [self.canvasWidth-320,50])

    def timerCount(self):
        self.playerJump(self.player,self.canvasHeight,
            self.platformList,self.groundHeight,self.slopeList)
        self.timeCounter+=1
        if self.timeCounter==60:
            self.timerSecond +=1
            self.timeCounter=0
        if self.timerSecond==60:
            self.timerMin+=1
            self.timerSecond=0
        if (self.timeCounter%60==0 and self.timerSecond%2==0 and 
            not self.getFlag):
            self.fruitList = self.getFruitList(self.fruitList,
                self.allButPlayer,self.player,self.bgIsShifting)
    def frogAni(self):
        self.frog.rect.x-=50
        frogHitBullet = pygame.sprite.spritecollide(self.frog,
            self.bulletList,False)
        if (len(frogHitBullet)>0 and self.frog.rect.bottom == 
            self.canvasHeight-self.groundHeight):
            self.frog.rect.x+=20
            self.frog.isJumpUp=True
        self.frog.rect.x+=50
        frogHitBullet = pygame.sprite.spritecollide(self.frog,
            self.bulletList,False)
        if (len(frogHitBullet)>0 and self.frog.rect.bottom == 
            self.canvasHeight-self.groundHeight):
            self.frog.rect.x-=20
            self.frog.isJumpUp=True
        if self.bloodBar.rect.x<self.canvasWidth-100:
            if (self.timeCounter==1 and self.timerSecond%3==0 and 
                self.frog.rect.bottom == 
                self.canvasHeight-self.groundHeight):
                self.frog.isJumpUp=True
        if self.bloodBar.rect.x>self.canvasWidth-100:
            if (self.timeCounter==1 and self.timerSecond%1==0 and 
                self.frog.rect.bottom == 
                self.canvasHeight-self.groundHeight):
                self.frog.isJumpUp=True
        playerHitFrog = \
        pygame.sprite.collide_rect(self.player,self.frog)
        
        if playerHitFrog:
            self.bloodBar2.rect.x+=1

            
        frogHitBullet = pygame.sprite.spritecollide(self.frog,
            self.bulletList,True)
        if len(frogHitBullet)>0:
            self.bloodBar.rect.x+=20
            
        if self.bloodBar.rect.x>self.canvasWidth:
            self.win=True
            self.gameover = True
            self.player.rect.bottom = \
            self.canvasHeight-self.groundHeight
            for bullet in self.bulletList:
                self.bulletList.remove(bullet)
            self.frogList.remove(self.frog)

        if self.bloodBar2.rect.x>self.canvasWidth:
            self.gameover = True
    def progressScreen(self):
        if self.timerSecond%5==0 and self.getGreenKey:

            bullet = VerticalBullet()
            bullet.rect.x =self.floatingPlatform3.rect.x+\
            self.floatingPlatform3.rect.width/2
            bullet.rect.y =self.floatingPlatform3.rect.bottom
            if len(self.bulletList)<3:
                self.bulletList.add(bullet)
        if not self.goToResult:
            textString = "Fruits  "+str(self.score)
            textString+= "  Timer  {0:02}:{1:02}".format(self.timerMin,
                self.timerSecond)
            text = self.font.render(textString, True, pink)
            self.canvas.blit(text, [50,50])
            
            if not self.gameover:
                text1 = self.font.render("Restart", True, purple)
                self.canvas.blit(text1, 
                    [110,110])
                try:
                    if self.restartButton4.collidepoint(pygame.mouse.get_pos()):
                        self.restartButton4=self.canvas.blit(
                            pygame.transform.scale
                            (self.buttonImageList[7],(70,70)),[40,90])
                    else:
                        self.restartButton4=self.canvas.blit(
                            self.buttonImageList[7],
                            [50,100])
                except:
                    self.restartButton4=self.canvas.blit(
                        self.buttonImageList[7],
                            [50,100])
                
                if not self.isPause:
                    text2 = self.font.render("Pause", True, purple)
                    self.canvas.blit(text2, 
                        [110,180])

                    try:
                        if self.pauseButton.collidepoint(
                            pygame.mouse.get_pos()):
                            self.pauseButton=self.canvas.blit(
                                pygame.transform.scale(
                                    self.buttonImageList[8],(70,70)),[40,
                                150])
                        else:
                            self.pauseButton=self.canvas.blit(
                                self.buttonImageList[8],
                            [50,170])
                    except:
                        self.pauseButton=self.canvas.blit(
                            self.buttonImageList[8],
                        [50,170])

            if self.isPause and not self.gameover:
                text2 = self.font.render("Continue", True, purple)
                self.canvas.blit(text2, 
                    [110,180])
                try:
                    if self.pauseButton.collidepoint(pygame.mouse.get_pos()):
                        self.pauseButton=self.canvas.blit(
                            pygame.transform.scale(
                            self.buttonImageList[9],(70,70)),[40,
                            150])
                    else:
                        self.pauseButton=self.canvas.blit(
                            self.buttonImageList[9],
                        [50,170])
                except:
                    self.pauseButton=self.canvas.blit(self.buttonImageList[9],
                    [50,170])
    def gameoverAndWinScreen(self):
        if not self.goToResult:
            if self.gameover and not self.win:
                
                text = self.font2.render("Game over", True, blue)
                self.canvas.blit(text, [self.canvasWidth/2-100,
                    self.canvasHeight/4])
                try:
                    if self.continueButton2.collidepoint(
                        pygame.mouse.get_pos()):
                        self.continueButton2=self.canvas.blit(
                            pygame.transform.scale(
                                self.buttonImageList[1],(70,70)),
                            [self.canvasWidth/2+140,self.canvasHeight/4-10])
                    else:
                        self.continueButton2=self.canvas.blit(
                            self.buttonImageList[1],
                            [self.canvasWidth/2+150,self.canvasHeight/4])
                except:
                    self.continueButton2=self.canvas.blit(
                        self.buttonImageList[1],
                            [self.canvasWidth/2+150,self.canvasHeight/4])


                
                text2 = self.font2.render("Restart", True, blue)
                self.canvas.blit(text2, 
                    [self.canvasWidth/2-100,self.canvasHeight/4+100])
                try:
                    if self.restartButton1.collidepoint(pygame.mouse.get_pos()):
                        self.restartButton1=self.canvas.blit(
                            pygame.transform.scale(
                                self.buttonImageList[6],(70,70)),
                            [self.canvasWidth/2+140,self.canvasHeight/4+90])
                    else:
                        self.restartButton1=self.canvas.blit(
                            self.buttonImageList[6],
                            [self.canvasWidth/2+150,self.canvasHeight/4+100])
                except:
                    self.restartButton1=self.canvas.blit(
                        self.buttonImageList[6],
                            [self.canvasWidth/2+150,self.canvasHeight/4+100])
            if self.gameover and self.win:
                text = self.font2.render("Win!!", True, blue)
                self.canvas.blit(text, [self.canvasWidth/2-100,
                    self.canvasHeight/4])
                try:
                    if self.continueButton2.collidepoint(
                        pygame.mouse.get_pos()):
                        self.continueButton2=self.canvas.blit(
                            pygame.transform.scale(
                                self.buttonImageList[1],(70,70)),
                            [self.canvasWidth/2+140,self.canvasHeight/4-10])
                    else:
                        self.continueButton2=self.canvas.blit(
                            self.buttonImageList[1],
                            [self.canvasWidth/2+150,self.canvasHeight/4])
                except:
                    self.continueButton2=self.canvas.blit(
                        self.buttonImageList[1],
                            [self.canvasWidth/2+150,self.canvasHeight/4])


                
                text2 = self.font2.render("Restart", True, blue)
                self.canvas.blit(text2, 
                    [self.canvasWidth/2-100,self.canvasHeight/4+100])
                try:
                    if self.restartButton1.collidepoint(pygame.mouse.get_pos()):
                        self.restartButton1=self.canvas.blit(
                            pygame.transform.scale(
                                self.buttonImageList[6],(70,70)),
                            [self.canvasWidth/2+140,self.canvasHeight/4+90])
                    else:
                        self.restartButton1=self.canvas.blit(
                            self.buttonImageList[6],
                            [self.canvasWidth/2+150,self.canvasHeight/4+100])
                except:
                    self.restartButton1=self.canvas.blit(
                        self.buttonImageList[6],
                            [self.canvasWidth/2+150,self.canvasHeight/4+100])
    def canvasAni(self):
        self.allButPlayer = self.getAllButPlayer(self.platformList,
            self.enemyList,self.fruitList,self.slopeList,self.rockList,
            self.monkeyList)
        self.isPlayerOutOfCanvas(self.player,self.canvasWidth,
            self.canvasHeight)
        self.bulletFly(self.bulletList,self.enemyList,self.canvasWidth,
            self.platformList)
        if ((self.player.isWalking and self.player.vx>0) or 
        self.toTheEnd):
            self.changeWalkingImageRight()
        if self.player.isWalking and self.player.vx<0:
            self.changeWalkingImageLeft()
        playerHitplatform = pygame.sprite.spritecollide(self.player,
            self.platformList,False)
        if(len(playerHitplatform)>0):
            for platform in playerHitplatform:
                self.player.rect.x = platform.rect.left-\
                self.player.rect.width
                playerHitplatform=[]
                self.player.vx=0
            self.player.isWalking=False
            self.bgIsShifting=False
            self.player.goToBgShift=False
        if self.bgIsShifting:
            self.changeWalkingImageRight()
            if self.ground7.rect.right<=self.canvasWidth:
                self.bgIsShifting=False
            else:
                self.shiftAll(self.player,self.allButPlayer,
                    self.platformList,self.bgShift)
        if not self.goToResult:
            self.updatesAndDraws(self.canvas,self.bulletList,
                self.enemyList,self.platformList,self.playerList,
                self.fruitList,self.gameover,self.timerSecond,
                self.slopeList,self.rockList,self.monkeyList)
        if (self.player.goToBgShift):
            self.bgIsShifting=True
            self.shiftVUpdate()
    def playerHitSth(self):
        playerHitSth = pygame.sprite.spritecollide\
        (self.player,self.platformList,False)
        if(len(playerHitSth)>0):
            for platform in playerHitSth:
                if self.player.vx>0:
                    self.player.rect.x = \
                    platform.rect.left-\
                    self.player.rect.width
                if self.player.vx<0:
                    self.player.rect.x =\
                     platform.rect.right
                playerHitplatform=[]
                self.bgIsShifting = False
                self.bgShiftV=0
                self.bgShift=0
        else:
            self.bgIsShifting=True
            self.bgShiftV = self.player.vx
        self.shiftVUpdate()
    def restart(self):

        self.gameover = False
        self.goToResult = False
        self.init()
    def removeUseless(self):
        for sprite in self.allButPlayer:
            if (sprite.rect.right<0 or 
                sprite.rect.bottom>self.canvasHeight):
                self.allButPlayer.remove(sprite)
    def bossModeFunc(self):
        for element in self.allButPlayer:
            self.allButPlayer.remove(element)
        for element in self.platformList:
            self.platformList.remove(element)
        for enemy in self.enemyList:
            self.enemyList.remove(enemy)
        bgImage = pygame.image.load("bg2.png").convert()
        ground2 = pygame.image.load("ground2.png").convert()
        ground2=pygame.transform.scale(ground2,(350,70))
        self.bgImage = bgImage

        for i in xrange(4):
            ground = Ground()
            ground.image = ground2
            ground.rect.x = 0+i*ground.rect.width
            ground.rect.bottom = self.canvasHeight
            self.platformList.add(ground)
    def readFile(self,filename, mode="rt"):
        # rt = "read text"
        with open(filename, mode) as fin:
            return fin.read()
    # from notes
    def writeFile(self,filename, contents, mode="wt"):
        # wt = "write text"
        with open(filename, mode) as fout:
            fout.write(contents)
    
    def showResult(self):
        self.totalScore = self.score*20 - (self.timerSecond+self.timerMin*60)
        if self.totalScore<0 or self.isFreeMode:
            self.totalScore=0
        if self.win:
            textString3 = "Get wife back? Yes!!"
        else:
            textString3 = "Get wife back? No..."
        text3 = self.font2.render(textString3, True, blue)
        self.canvas.blit(text3, [100,self.canvasHeight/2-200])
        
        textString4 = "Fruits: " + str(self.score)
        text4 = self.font2.render(textString4, True, blue)
        self.canvas.blit(text4, [100,self.canvasHeight/2-100])
        
        textString5 = "Time: {0:02}:{1:02}".format(self.timerMin,
            self.timerSecond)
        text5 = self.font2.render(textString5, True, blue)
        self.canvas.blit(text5, [100,self.canvasHeight/2])
        textString6 = "Total Score: "+str(self.totalScore)
        text6 = self.font2.render(textString6, True, pink)
        self.canvas.blit(text6, [100,self.canvasHeight/2+100])
        textString8 = "Restart"
        text8 = self.font2.render(textString8, True, blue)
        self.canvas.blit(text8, 
            [100,self.canvasHeight/2+200])
        try:
            if self.restartButton3.collidepoint(pygame.mouse.get_pos()):
                self.restartButton3=self.canvas.blit(pygame.transform.scale(
                    self.buttonImageList[6],(70,70)),[300-10,
                self.canvasHeight/2+190])
            else:
                self.restartButton3=self.canvas.blit(self.buttonImageList[6],
                    [300,self.canvasHeight/2+200])
        except:
            self.restartButton3=self.canvas.blit(self.buttonImageList[6],
                    [300,self.canvasHeight/2+200])
        
        
        if self.oldHighScoreString==self.highScoreString:
                self.highScoreString+=str(self.totalScore)+' '
        self.writeFile(self.path, self.highScoreString)
        textString9List = (self.highScoreString.split())
        temp = map(int,textString9List)
        temp.sort()

        temp=temp[::-1]
        
        for i in xrange(len(temp)):
            if i<5:
                if temp[i]==self.totalScore:
                    text9 = self.font2.render(str(i+1)+'.'+
                        str(temp[i]), True, pink)
                else:
                    text9 = self.font2.render(str(i+1)+'.'+str(temp[i]),
                     True, blue)
                self.canvas.blit(text9, [self.canvasWidth/2+200,100*(i+2)])
        text10 = self.font2.render('High Scores', True, blue)
        self.canvas.blit(text10, [self.canvasWidth/2+200,100])

    def gameoverFunc(self):
        playerHitEnemy = pygame.sprite.spritecollide(self.player,
            self.enemyList,
            False)
        playerHitRock = pygame.sprite.spritecollide(self.player,self.rockList,
            False)
        playerHitMonkey = pygame.sprite.spritecollide(self.player,
            self.monkeyList,
            False)
        playerHitBullet = pygame.sprite.spritecollide(self.player,
            self.bulletList,
            False)

        if (self.player.rect.bottom==self.canvasHeight or len(playerHitEnemy)>0
         or len(playerHitRock)>0 or len(playerHitMonkey)>0 or 
         len(playerHitBullet)):                
            for enemy in playerHitEnemy:
                if self.player.isJumpDown:
                    self.player.rect.bottom = enemy.rect.top
            self.player.isWalking=False
            self.player.isJumpDown = False
            
            self.player.vy=0
            self.bgIsShifting=False
            self.gameover=True
    
    def getPillarsAndEnemy(self,platformList,enemyList,canvasHeight,
        groundHeight,player,gameover,bgIsShifting):
        gap=50
        pillarLeft = self.getPillar(500,canvasHeight-groundHeight)
        pillarRight = self.getPillar(500+gap*7,canvasHeight-groundHeight)
        
        platformList.add(pillarLeft)
        platformList.add(pillarRight)
        
        enemy = EnemyBackForth(pillarLeft,pillarRight,player,gameover,
            bgIsShifting)
        enemy.rect.left = pillarLeft.rect.right
        enemy.rect.bottom = self.canvasHeight-self.groundHeight
        enemyList.add(enemy)
    def getGroundAndMonkey(self,monkeyList,platformList,canvasWidth,
        canvasHeight,groundHeight):
        ground = self.getLongGround(1200,canvasHeight-groundHeight)
        platformList.add(ground)
        monkey = Monkey(ground)
        monkeyList.add(monkey)
    def arrange(self,canvasWidth,canvasHeight,groundWidth,groundHeight,player):
        gap = 50
        smallGap = 10

        for i in xrange(2):
            ground = self.getGround(i*(groundWidth),canvasHeight-groundHeight)
            self.platformList.add(ground)
        
        platform1 = self.getPlatform(groundWidth*2+smallGap*2,canvasHeight-
            groundHeight-player.rect.height)
        platform2 = self.getPlatform(platform1.rect.right+smallGap*3,
            platform1.rect.top-player.rect.height) 
        platform4 = self.getPlatform(platform2.rect.right+gap,
            platform2.rect.bottom+gap*3)
        self.platformList.add(platform1)
        self.platformList.add(platform2)
        self.platformList.add(platform4)

        floatingPlatform1 = FloatingPlatform(platform4.rect.right+smallGap,
            platform4.rect.right+gap*5,player)
        floatingPlatform1.rect.x = platform4.rect.right+gap
        floatingPlatform1.rect.y = gap*8
        self.platformList.add(floatingPlatform1)


        ground3 = self.getGround(floatingPlatform1.rect.right+
            floatingPlatform1.rect.width+smallGap*2,canvasHeight-groundHeight)
        self.platformList.add(ground3)

        slope1 = self.getSlope(ground3.rect.right+smallGap*3,self.canvasHeight)
        self.slopeList.add(slope1)
        self.rockList = self.getRockList(self.slopeList,canvasHeight)
        
        octopus1 = Octopus(self.slopeList,canvasHeight)
        octopus1.rect.x = slope1.rect.right+smallGap
        octopus1.rect.y = canvasHeight*2/3
        self.octopusList.add(octopus1)
        
        floatingPlatform2 = FloatingPlatform(slope1.rect.right,
            slope1.rect.right+gap*2,player)
        floatingPlatform2.rect.x = slope1.rect.right+smallGap*5
        floatingPlatform2.rect.y = gap*8
        self.platformList.add(floatingPlatform2)
        
        
        ground4 = self.getGround(floatingPlatform2.rightBoundary+
            floatingPlatform2.rect.width,canvasHeight-groundHeight)
        self.platformList.add(ground4)

        ground5 = self.getLongGround(ground4.rect.right,canvasHeight-
            groundHeight)
        self.platformList.add(ground5)

        pillarLeft = self.getPillar(ground5.rect.left,canvasHeight-
            groundHeight)
        pillarRight = self.getPillar(pillarLeft.rect.right+gap*7,canvasHeight-
            groundHeight)
        
        self.platformList.add(pillarLeft)
        self.platformList.add(pillarRight)
        
        snail = EnemyBackForth(pillarLeft,pillarRight,player,self.gameover,
            self.bgIsShifting)
        snail.rect.left = pillarLeft.rect.right
        snail.rect.bottom = canvasHeight-groundHeight
        self.snailList.add(snail)

        ground6 = self.getLongGround(ground5.rect.right+gap,canvasHeight-
            groundHeight)
        self.platformList.add(ground6)
        monkey = Monkey(ground6)
        self.monkeyList.add(monkey)
 
        platform5 = self.getPlatformWithTorch(ground6.rect.right,
            ground6.rect.top+35)
        self.platformList.add(platform5)

        self.ground7 = self.getLongGround(platform5.rect.right,canvasHeight-
            groundHeight)
        self.platformList.add(self.ground7)
        
        greenKey = GreenKey()
        greenKey.rect.x = self.ground7.rect.x
        greenKey.rect.bottom = self.ground7.rect.top
        self.fruitList.add(greenKey)

        self.floatingPlatform3 = FloatingPlatform(self.ground7.rect.x-2*gap,
            self.ground7.rect.right-gap*9,player)
        self.floatingPlatform3.rect.x = self.ground7.rect.x
        self.floatingPlatform3.rect.y = gap*2
        self.floatingPlatform3.image = pygame.image.load("blackTile.png").convert()
        self.floatingPlatform3.image = pygame.transform.scale(
            self.floatingPlatform3.image,(350/2,35))
        self.floatingPlatform3.image.set_colorkey(white)
        self.platformList.add(self.floatingPlatform3)
        
        self.frog = Frog()
        self.frog.rect.right = self.ground7.rect.right
        self.frog.rect.bottom = self.ground7.rect.top
        self.frogList.add(self.frog)
    def getAllButPlayer(self,platformList,enemyList,fruitList,slopeList,
        rockList,monkeyList):
        allButPlayer = pygame.sprite.Group()
        for platform in platformList:
            allButPlayer.add(platform)
        for enemy in enemyList:
            allButPlayer.add(enemy)
        for fruit in fruitList:
            allButPlayer.add(fruit)
        for slope in slopeList:
            allButPlayer.add(slope)
        for rock in rockList:
            allButPlayer.add(rock)
        for monkey in monkeyList:
            allButPlayer.add(monkey)
        for frog in self.frogList:
            allButPlayer.add(frog)
        return allButPlayer
    def getFruitList(self,fruitList ,allButPlayer,player,bgIsShifting):        
        if self.player.vx>0 or bgIsShifting:
            cherry = Cherry()
            cherry.rect.left = self.player.rect.right + 200
            cherry.rect.y = random.randrange(player.rect.y-165,player.rect.y)
            cherryHitSth = pygame.sprite.spritecollide(cherry,allButPlayer,
                False)
            if len(cherryHitSth)==0:
                fruitList.add(cherry)  
        return fruitList
    def getPlatform(self,x,bottom):
        platform = Platform()
        platform.rect.x = x
        platform.rect.bottom = bottom
        return platform
    def getPlatformWithTorch(self,x,bottom):
        platform = PlatformWithTorch()
        platform.rect.x = x
        platform.rect.bottom = bottom
        return platform
    def getPillar(self,x,y):
        platform = Pillar()
        platform.rect.x = x
        platform.rect.bottom = y
        return platform
    def getFloatingPlatform(self,leftBoundary,y,rightBoundary):
        platform = FloatingPlatform(leftBoundary,rightBoundary)
        platform.rect.x = leftBoundary
        platform.rect.y = y
        return platform
    def getGround(self,x,y):
        ground = Ground()
        ground.rect.x = x
        ground.rect.y = y
        return ground
    def getLongGround(self,x,y):
        ground = LongGround()
        ground.rect.x = x
        ground.rect.y = y
        return ground
    def getSlope(self,left,bottom):
        slope = Slope()
        slope.rect.left=left
        slope.rect.bottom = bottom
        return slope
    def getEnemyList(self,canvasWidth,canvasHeight,player,platformList,
        octopusList,snailList):
        enemyList = pygame.sprite.Group()
        for platform in platformList:
            if type(platform)==Platform:
                enemy=Enemy(platform)
                enemy.rect.x = platform.rect.x + platform.rect.width -\
                 enemy.rect.width
                enemy.rect.bottom = platform.rect.top
                enemyList.add(enemy)
            if type(platform)==PlatformWithTorch:
                enemy=Torch(player)
                enemy.rect.x = platform.rect.x+platform.rect.width/2
                enemy.rect.bottom = platform.rect.y
                enemyList.add(enemy)
        for octopus in octopusList:
            enemyList.add(octopus)
        for snail in snailList:
            enemyList.add(snail)
        return enemyList
    def getRockList(self,slopeList,canvasHeight):

        rockList = pygame.sprite.Group()
        for slope in slopeList:
            rock = Rock(slope,canvasHeight)
            rockList.add(rock)        
        return rockList
    def shiftVUpdate(self):
        if self.bgShiftV<2:
            self.bgShiftV+=self.bgShiftA
    def shiftAll(self,player,allButPlayer,platformList,bgShift):

        if self.bgShift<5:
            self.bgShift+=self.bgShiftV
        
        for sprite in allButPlayer:
            if isinstance(sprite,FloatingPlatform):
                
                sprite.leftBoundary-=int(self.bgShift)
                
                sprite.rightBoundary-=int(self.bgShift)
                
                
            sprite.rect.x-=int(self.bgShift)
            
                

        playerHitSth = pygame.sprite.spritecollide(player,platformList,False)
        if(len(playerHitSth)>0):
            for platform in playerHitSth:
                if player.vx>0:
                    player.rect.x = platform.rect.left-player.rect.width
                if player.vx<0:
                    player.rect.x = platform.rect.right
                playerHitplatform=[]
                self.bgIsShifting = False
                self.bgShiftV=0
                self.bgShift=0
    def playerJump(self,player,canvasHeight,platformList,groundHeight,
        slopeList):
        if( player.isJumpUp==True):

            if (player.vy<=0):
                player.jumpUp()
                if (player.vy==0):
                    player.isJumpUp=False
                    player.isJumpDown=True
        playerHitSlope = pygame.sprite.spritecollide(player,slopeList,False)
        if( player.isJumpDown==True) and len(playerHitSlope)==0:
            if (player.rect.y<canvasHeight-player.rect.height):
                
                player.jumpDown()

            else:
                player.rect.y=canvasHeight-player.rect.height
                player.isJumpDown=False
                player.vy=0
        if((player.isJumpDown==False and player.isJumpUp==False and 
            player.rect.bottom<canvasHeight-player.rect.height) and 
        len(playerHitSlope)==0):
            self.player.rect.y+=1
            hitplatformList = pygame.sprite.spritecollide(player,platformList,
                False)
            if(len(hitplatformList)==0 and 
                player.rect.y!=canvasHeight-player.rect.height):

                player.isJumpDown=True
            else:
                self.player.rect.y-=1
          
    def isPlayerOutOfCanvas(self,player,canvasWidth,canvasHeight):
        if player.rect.x<0:
            player.rect.x=0
        if player.rect.x>canvasWidth-player.rect.width:
            player.rect.x=canvasWidth-player.rect.width
        if player.rect.y>canvasHeight-player.rect.height:
            player.rect.y=canvasHeight-player.rect.height
            player.rect.y = canvasHeight-player.rect.height
            player.isJumpDown=False
            player.stop()
    def bulletFly(self,bulletList,enemyList,canvasWidth,platformList):
        for bullet in self.bulletList:
            if isinstance(bullet,Bullet):
                bullet.changeV()
            enemyHitList = pygame.sprite.spritecollide(bullet,self.enemyList,
                True)
            monkeyHitList = pygame.sprite.spritecollide(bullet,self.monkeyList,
                True)
            for enemy in enemyHitList:
                self.bulletList.remove(bullet)
            for enemy in monkeyHitList:
                self.bulletList.remove(bullet)
            platformHitList = pygame.sprite.spritecollide(bullet,platformList,
                False)
            for platform in platformHitList:
                self.bulletList.remove(bullet)
            if bullet.rect.x>self.canvasWidth:
                self.bulletList.remove(bullet)
    
    def addBullet(self,player,bulletList,facingRight,facingLeft):
        bullet = Bullet(facingRight,facingLeft)
        if(facingRight):
            bullet.rect.x = player.rect.x+player.rect.width
        if(facingLeft):
            bullet.rect.x = player.rect.x
        bullet.rect.y = player.rect.y+player.rect.height/3
        bulletList.add(bullet)
    def updatesAndDraws(self,canvas,bulletList,enemyList,platformList,
        playerList,fruitList,gameover,timerSecond,slopeList,rockList,
        monkeyList):
        
        if not gameover and not self.isPause:
            bulletList.update()
            
            for enemy in enemyList :
                if isinstance(enemy,Enemy) or isinstance(enemy,Torch):
                    enemy.update(self.timerSecond)
                else:
                    enemy.update()
            platformList.update()
            playerList.update(platformList,enemyList,slopeList,self.toTheEnd)
            slopeList.update()
            for player in playerList:
                rockList.update(player)
                monkeyList.update(player)
            if self.frog.isJumpDown or self.frog.isJumpUp:
                self.frogList.update(platformList,self.ground7)
        if self.win and self.playerWife.rect.x>self.player.rect.right:
            self.playerWifeList.update()
            
        slopeList.draw(canvas)
        bulletList.draw(canvas)
        enemyList.draw(canvas)
        platformList.draw(canvas)
        fruitList.draw(canvas)
        playerList.draw(canvas)
        rockList.draw(canvas)
        monkeyList.draw(canvas)

        
        if self.getFlag:
            self.bloodBarList.draw(canvas)
            self.frogList.draw(canvas)
            if not self.goToResult:
                self.drawSnow(self.canvas,self.snowList,self.canvasWidth,
                    self.canvasHeight)
        if self.win:
            self.playerWifeList.draw(canvas)

    def changeWalkingImageRight(self):
        self.facingRight=True
        self.facingLeft=False
        image1 = pygame.image.load("walkRight1.png").convert()
        image1.set_colorkey(black)
        image1 = pygame.transform.scale(image1,(40,60))
        image2 = pygame.image.load("walkRight2.png").convert()
        image2.set_colorkey(black)
        image2 = pygame.transform.scale(image2,(40,60))
        image3 = pygame.image.load("playerAngel.png").convert()
        image3.set_colorkey(black)
        image3 = pygame.transform.scale(image3,(40,41))
        self.imageDie = image3
        self.imageFlag+=1
        if self.imageFlag%10<5:
            self.player.image = image1
        else:
            self.player.image = image2
    def changeToJumpRight(self):
        self.facingRight=True
        self.facingLeft=False
        image = pygame.image.load("jumpRight.png").convert()
        image.set_colorkey(black)
        image = pygame.transform.scale(image,(40,60))
        self.player.image = image
    def changeToJumpLeft(self):
        self.facingRight=False
        self.facingLeft=True
        image = pygame.image.load("jumpRight.png").convert()
        
        image.set_colorkey(black)
        image = pygame.transform.flip(image,1,0)
        image = pygame.transform.scale(image,(40,60))
        self.player.image = image
        
    def changeWalkingImageLeft(self):
        self.facingRight=False
        self.facingLeft=True
        image1 = pygame.image.load("walkRight1.png").convert()
        image1 = pygame.transform.scale(image1,(40,60))
        image1.set_colorkey(black)
        image1 = pygame.transform.flip(image1,1,0)
        

        image2 = pygame.image.load("walkRight2.png").convert()
        image2 = pygame.transform.scale(image2,(40,60))
        image2.set_colorkey(black)
        image2 = pygame.transform.flip(image2,1,0)
        
        self.imageFlag+=1
        
        if self.imageFlag%10<5:
            self.player.image = image1
        else:
            self.player.image = image2
    def subInit1(self):
        self.goToResult = False
        self.bloodBarLength = 320
        self.canvasWidth = 1000
        self.canvasHeight = 600
        self.groundWidth = 350
        self.groundHeight = 70
        self.bgIsShifting = False
        self.toTheEnd = False
        self.score = 0
        self.timerSecond=0
        self.timerMin = 0
        self.timeCounter=0
        font = "font.ttf"
        self.font = pygame.font.Font(font,45)
        self.font2 = pygame.font.Font(font,60)
        self.exitGame=False
        self.win = False

        self.canvas = pygame.display.set_mode([self.canvasWidth,
            self.canvasHeight])
        pygame.display.set_caption("Little Yellow's Adventure")
    def subInit2(self):
        self.bgImage = pygame.image.load("BG.png").convert()
        self.bgImage = pygame.transform.scale(self.bgImage,(self.canvasWidth,
            self.canvasHeight))
        self.bgImage0 = pygame.image.load("bg1.png").convert()
        self.bgImage0 = pygame.transform.scale(self.bgImage0,(self.canvasWidth,
            self.canvasHeight))
        self.bgLoc = [0,0]
        self.soundBgm = pygame.mixer.Sound("bgm.wav")
        self.soundBgm.set_volume(0.01)
        self.soundShoot = pygame.mixer.Sound("shoot.wav")
        self.soundShoot.set_volume(0.05)
        self.soundJump = pygame.mixer.Sound("jump.wav")
        self.soundJump.set_volume(0.05)
        
        self.gameover = False
        self.enemyList = pygame.sprite.Group()
        self.bulletList = pygame.sprite.Group()
        self.playerList = pygame.sprite.Group()
        self.playerWifeList = pygame.sprite.Group()
        self.platformList = pygame.sprite.Group()
        self.allButPlayer = pygame.sprite.Group()
        self.fruitList = pygame.sprite.Group()
        self.slopeList = pygame.sprite.Group()
        self.snailList = pygame.sprite.Group()
        self.frogList = pygame.sprite.Group()
        self.snowList = pygame.sprite.Group()
        self.bloodBarList = pygame.sprite.Group()
        self.snowList = self.getFallingSnow(self.canvasWidth,self.canvasHeight)
        self.bloodBar = BloodBar(self.bloodBarLength)
        self.bloodBar.rect.y = 150
        self.bloodBar.rect.right=self.canvasWidth
        self.bloodBarList.add(self.bloodBar)
        self.bloodBar2 = BloodBar(self.bloodBarLength)
        self.bloodBar2.rect.y = 100
        self.bloodBar2.rect.right=self.canvasWidth
        self.bloodBarList.add(self.bloodBar2)
    def drawSnow(self,canvas,snowList,canvasWidth,canvasHeight):
        for i in xrange(50):
            pygame.draw.circle(self.canvas,white,self.snowList[i],2)
            self.snowList[i][1]+=1
            if(self.snowList[i][1]>self.canvasHeight):
                self.snowList[i][1]=0
                self.snowList[i][0]=random.randrange(self.canvasWidth)
    def getFallingSnow(self,canvasWidth,canvasHeight):
        snowList = []
        for i in xrange(50):
            x = random.randrange(canvasWidth)
            y =random.randrange(canvasHeight)
            snowList.append([x,y])
        return snowList
    def subInit3(self):
        self.bgShift = 0
        self.bgLength = 4000
        self.bgShiftA = 0.1
        self.bgShiftV = 0
        
        self.imageFlag=0
        self.facingRight = True
        self.facingLeft = False

        self.getGreenKey = False
        self.getRedKey = False
        self.getYellowKey = False
        self.gameStart = False
        self.showBeforeStart = True
        self.goToInstr1 = False
        self.goToInstr2 =False
        self.buttonImageList = self.getButtonImages()
    def subInit4(self):
        self.player = Player(self.gameover)
        self.player.rect.x = 300
        self.player.rect.y = self.canvasHeight-self.player.rect.height-100
        self.playerList.add(self.player)
        self.playerWife = PlayerWife()
        self.playerWife.rect.x = self.canvasWidth
        self.playerWife.rect.bottom = self.canvasHeight-self.groundHeight
        self.playerWifeList.add(self.playerWife)

        self.octopusList = pygame.sprite.Group()
        self.rockList = pygame.sprite.Group()
        self.monkeyList = pygame.sprite.Group()
        self.arrange(self.canvasWidth,self.canvasHeight,self.groundWidth,
            self.groundHeight,self.player)
        self.enemyList=self.getEnemyList(self.canvasWidth,self.canvasHeight,
            self.player,self.platformList,self.octopusList,self.snailList)
        self.getFlag = False
        self.letterCount = 0
        self.isPause = False
        self.path = "highScore.txt"
        self.isFreeMode=False
        self.switchToBossMode = False
        self.goToResult=False

        if (not os.path.exists(self.path)):
            os.makedirs(self.path)
        if (os.path.exists(self.path)):
            self.highScoreString = self.readFile(self.path)
            self.oldHighScoreString = self.highScoreString
        
    def getButtonImages(self):
        bullenImageList = []
        image1 = pygame.image.load("up.png").convert()
        image1 = pygame.transform.scale(image1,(50,50))
        image1.set_colorkey(black)

        image2 = pygame.image.load("right.png").convert()
        image2 = pygame.transform.scale(image2,(50,50))
        image2.set_colorkey(white)

        image3 = pygame.image.load("left.png").convert()
        image3 = pygame.transform.scale(image3,(50,50))
        image3.set_colorkey(white)

        image4 = pygame.image.load("s.png").convert()
        image4 = pygame.transform.scale(image4,(50,50))
        image4.set_colorkey(white)
        image5 = pygame.image.load("i.png").convert()
        image5 = pygame.transform.scale(image5,(50,50))
        image5.set_colorkey(white)
        image6 = pygame.image.load("space.png").convert()
        image6 = pygame.transform.scale(image6,(114,40))
        image6.set_colorkey(white)
        image7 = pygame.image.load("r.png").convert()
        image7 = pygame.transform.scale(image7,(50,50))
        image7.set_colorkey(white)
        image8 = pygame.image.load("r_purple.png").convert()
        image8 = pygame.transform.scale(image8,(50,50))
        image8.set_colorkey(white)

        image9 = pygame.image.load("pause.png").convert()
        image9 = pygame.transform.scale(image9,(50,50))
        image9.set_colorkey(white)
        image10 = pygame.image.load("continue.png").convert()
        image10 = pygame.transform.scale(image10,(50,50))
        image10.set_colorkey(white)
        image11 = pygame.image.load("f.png").convert()
        image11 = pygame.transform.scale(image11,(50,50))
        image11.set_colorkey(white)
        buttonImageList = [image1,image2,image3,image4,image5,image6,image7,\
        image8,image9,image10,image11]
        return buttonImageList
    def showBeforeStartFunc(self):
        textString0 = "Little Yellow's Adventure" 
        text = self.font2.render(textString0, True, blue)
        self.canvas.blit(text, [self.canvasWidth/2-300,self.canvasHeight/2-200])
        
        textString = "Classic Mode" 
        text = self.font2.render(textString, True, blue)
        self.canvas.blit(text, [self.canvasWidth/2-100,self.canvasHeight/2-100])
        

        try:
            if self.startButton.collidepoint(pygame.mouse.get_pos()):
                self.startButton=self.canvas.blit(pygame.transform.scale(
                    self.buttonImageList[3],(70,70)),[self.canvasWidth/2-210,
                    self.canvasHeight/2-110])
            else:
                self.startButton=self.canvas.blit(self.buttonImageList[3],
                    [self.canvasWidth/2-200,self.canvasHeight/2-100])
        except:
            self.startButton=self.canvas.blit(self.buttonImageList[3],
                [self.canvasWidth/2-200,self.canvasHeight/2-100])
        textString2 = "Instructions"
        text2 = self.font2.render(textString2, True, blue)
        self.canvas.blit(text2, [self.canvasWidth/2-100,
            self.canvasHeight/2+100])
        try:
            if self.instrButton.collidepoint(pygame.mouse.get_pos()):
                self.instrButton=self.canvas.blit(pygame.transform.scale(
                    self.buttonImageList[4],(70,70)),[self.canvasWidth/2-210,
                    self.canvasHeight/2+90])
            else:
                self.instrButton=self.canvas.blit(self.buttonImageList[4],
                    [self.canvasWidth/2-200,self.canvasHeight/2+100])
        except:
            self.instrButton=self.canvas.blit(self.buttonImageList[4],
                    [self.canvasWidth/2-200,self.canvasHeight/2+100])

        textString3 = "Free Mode"
        text3 = self.font2.render(textString3, True, blue)
        self.canvas.blit(text3, [self.canvasWidth/2-100,
            self.canvasHeight/2])
        try:
            if self.freeModeButton.collidepoint(pygame.mouse.get_pos()):
                self.freeModeButton=self.canvas.blit(pygame.transform.scale(
                    self.buttonImageList[10],(70,70)),[self.canvasWidth/2-210,
                    self.canvasHeight/2-10])
            else:
                self.freeModeButton=self.canvas.blit(self.buttonImageList[10],
                    [self.canvasWidth/2-200,self.canvasHeight/2])
        except:
            self.freeModeButton=self.canvas.blit(self.buttonImageList[10],
                    [self.canvasWidth/2-200,self.canvasHeight/2])
        
    def goToInstrFunc(self):
        textString3 = "Jump" 
        text3 = self.font2.render(textString3, True, blue)
        self.canvas.blit(text3, [200,self.canvasHeight/2-270])
        self.canvas.blit(self.buttonImageList[0],[150,self.canvasHeight/2-270])
        textString4 = "Walk to right"
        text4 = self.font2.render(textString4, True, blue)
        self.canvas.blit(text4, [200,self.canvasHeight/2-170])
        self.canvas.blit(self.buttonImageList[1],[150,self.canvasHeight/2-170])
        textString5 = "Walk to left"
        text5 = self.font2.render(textString5, True, blue)
        self.canvas.blit(text5, [200,self.canvasHeight/2-70])
        self.canvas.blit(self.buttonImageList[2],[150,self.canvasHeight/2-70])
        textString6 = "Fire"
        text6 = self.font2.render(textString6, True, blue)
        self.canvas.blit(text6, [self.canvasWidth/2+150,
            self.canvasHeight/2-270])
        self.canvas.blit(self.buttonImageList[5],[self.canvasWidth/2+33,
            self.canvasHeight/2-270])
        textString7 = "Start Now"
        text7 = self.font2.render(textString7, True, blue)
        self.canvas.blit(text7, [self.canvasWidth/2-150,self.canvasHeight/2+70])
        try:
            if self.startButton2.collidepoint(pygame.mouse.get_pos()):
                self.startButton2=self.canvas.blit(pygame.transform.scale(
                    self.buttonImageList[3],(70,70)),[self.canvasWidth/2+90,
            self.canvasHeight/2+60])
            else:
                self.startButton2=self.canvas.blit(self.buttonImageList[3],
                    [self.canvasWidth/2+100,self.canvasHeight/2+70])
        except:
            self.startButton2=self.canvas.blit(self.buttonImageList[3],
                    [self.canvasWidth/2+100,self.canvasHeight/2+70])

        textString8 = "Restart"
        text8 = self.font2.render(textString8, True, blue)
        self.canvas.blit(text8, 
            [self.canvasWidth/2+150,self.canvasHeight/2-170])
        self.canvas.blit(self.buttonImageList[6],[self.canvasWidth/2+100,
            self.canvasHeight/2-170])
    def goToInstrFunc1(self):
        
        textString = "little Yellow's wife"
        text = self.font2.render(textString, True, blue)
        self.canvas.blit(text, [150,100])
        textString2 = "is kidnapped by a frog."
        text2 = self.font2.render(textString2, True, blue)
        self.canvas.blit(text2, [150,150])
        textString3 = "If he wins,"
        text3 = self.font2.render(textString3, True, blue)
        self.canvas.blit(text3, [400,250])
        textString4 = "He gets wife back."
        text4 = self.font2.render(textString4, True, blue)
        self.canvas.blit(text4, [400,300])
        try:
            if self.continueButton.collidepoint(pygame.mouse.get_pos()):
                self.continueButton=self.canvas.blit(pygame.transform.scale(
                    self.buttonImageList[1],(70,70)),[400-10,400-10])
            else:
                self.continueButton=self.canvas.blit(self.buttonImageList[1],
                    [400,400])
        except:
            self.continueButton=self.canvas.blit(self.buttonImageList[1],
                    [400,400])
        image = pygame.image.load("walkRight2.png").convert()
        image.set_colorkey(black)
        image = pygame.transform.scale(image,(40,60))
        self.canvas.blit(image,[50,50])
        image2 = pygame.image.load("wifeWalk2.png").convert()
        image2.set_colorkey(black)
        image2 = pygame.transform.scale(image2,(40,60))
        image2 = pygame.transform.flip(image2,True,False)
        self.canvas.blit(image2,[90,50])
        image3 = pygame.image.load("frog.png").convert()
        image3.set_colorkey(black)
        image3 = pygame.transform.scale(image3,(58,39))
        self.canvas.blit(image3,[self.canvasWidth-330,150])
    def beforeStart(self):
        self.canvas.blit(self.bgImage0,self.bgLoc)
        if self.showBeforeStart:
            self.showBeforeStartFunc()
        if self.goToInstr1:
            self.goToInstrFunc1()
        if self.goToInstr2:
            self.goToInstrFunc()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exitGame = True
            if (event.type == pygame. MOUSEBUTTONDOWN and event.button==1):
                if (self.startButton.collidepoint(pygame.mouse.get_pos())):
                    self.gameStart=True
                    self.showBeforeStart = False
                if (self.freeModeButton.collidepoint(pygame.mouse.get_pos())):
                    self.gameStart=True
                    self.showBeforeStart = False
                    self.isFreeMode=True
                if (self.instrButton.collidepoint(pygame.mouse.get_pos())):
                    self.goToInstr1 = True
                    self.showBeforeStart=False
                if (self.goToInstr1):

                    try:
                        if(self.continueButton.collidepoint(
                            pygame.mouse.get_pos())):
                
                            self.goToInstr2 = True
                            self.goToInstr1 = False
                    except:
                        pass

                if (self.goToInstr2):
                    try:
                        if(self.startButton2.collidepoint(
                            pygame.mouse.get_pos())):
                    
                            self.gameStart=True
                            self.showBeforeStart = False
                    except:
                        pass
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_s and self.showBeforeStart:
                    
                    self.gameStart=True
                    self.showBeforeStart = False
                if event.key == pygame.K_i:
                    self.goToInstr1 = True
                    self.showBeforeStart=False
                if event.key == pygame.K_RIGHT:
                    if self.goToInstr1:
                        self.goToInstr2 = True
                        self.goToInstr1 = False
                if self.goToInstr2 and event.key == pygame.K_s:
                    self.gameStart=True
                    self.showBeforeStart = False

        
        
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self,platform):
        super(Enemy,self).__init__()
        self.platform = platform
        image = pygame.image.load("slimeWalk1.png").convert()
        image = pygame.transform.scale(image,(57,30))
        image.set_colorkey(black)
        image2 = pygame.image.load("slimeWalk2.png").convert()
        image2 = pygame.transform.scale(image2,(57,30))
        image2.set_colorkey(white)
        self.oldImage2 = image2
        self.image=image
        self.oldImage = self.image
        self.rect = self.image.get_rect()
        self.vx = -1
        
    def update(self,timerSecond):
        self.rect.x+=self.vx
        if self.vx>0 and self.rect.x>self.platform.rect.right-self.rect.width:
            self.vx*=-1
        if self.vx<0 and self.rect.x<self.platform.rect.left:
            self.vx*=-1 
        if self.vx>0:
            if timerSecond%2==0:
                self.image = pygame.transform.flip(self.oldImage,1,0)
            else:
                self.image = pygame.transform.flip(self.oldImage2,1,0)
        if self.vx<0:
            if timerSecond%2==0:
                self.image = pygame.transform.flip(self.oldImage,0,0)
            else:
                self.image = pygame.transform.flip(self.oldImage2,0,0)
class Octopus(pygame.sprite.Sprite):
    def __init__(self,canvasWidth,canvasHeight):
        super(Octopus,self).__init__()
        self.canvasHeight=canvasHeight
        self.canvasWidth=canvasWidth
        image = pygame.image.load("octopus.png").convert()
        image = pygame.transform.scale(image,(63,65))
        image.set_colorkey(white)
        self.image=image
        self.rect = self.image.get_rect()
        self.vy = 3
    def update(self):
        if self.vy>0 and self.vy<4:
            self.vy+=0.2
        if (self.rect.bottom>= self.canvasHeight/6 and
         self.rect.bottom<= self.canvasHeight):
            self.rect.y-=self.vy
        else:
            self.vy*=-1
            self.rect.y-=self.vy
class Monkey(pygame.sprite.Sprite):
    def __init__(self,ground):
        super(Monkey,self).__init__()
        self.image1 = pygame.image.load("monkeyWalkRight1.png").convert()
        self.image1 = pygame.transform.scale(self.image1,(36,59))
        self.image1 = pygame.transform.flip(self.image1,1,0)
        self.image1.set_colorkey(black)
        self.image2 = pygame.image.load("monkeyWalkRight2.png").convert()
        self.image2 = pygame.transform.scale(self.image2,(36,59))
        self.image2 = pygame.transform.flip(self.image2,1,0)
        self.image2.set_colorkey(black)
        
        self.image=self.image1
        self.rect = self.image.get_rect()
        self.ground = ground
        self.rect.right = ground.rect.right
        self.rect.bottom = self.ground.rect.top
        self.vx = -3
        self.vy = 5
    def update(self,player):
        if self.rect.x-player.rect.x<self.ground.rect.width:
            self.rect.y+=1
            monkeyHitGround= pygame.sprite.collide_rect(self,self.ground)
            if monkeyHitGround:
                self.rect.x+=self.vx
                self.rect.y-=1
                if self.rect.x%30>15:
                    self.image = self.image1
                else:
                    self.image = self.image2
            else:
                self.rect.y-=1
                if self.rect.bottom<self.ground.rect.bottom:
                    self.rect.y+=self.vy
class Torch(pygame.sprite.Sprite):
    def __init__(self,player):
        super(Torch,self).__init__()
        image = pygame.image.load("torch.png").convert()
        image = pygame.transform.scale(image,(35,20))
        image.set_colorkey(white)
        self.oldImage = image
        self.image = image
        self.rect = self.image.get_rect()
        self.player = player
    def update(self,timerSecond):
        pass
class EnemyBackForth(pygame.sprite.Sprite):
    def __init__(self,leftPillar,rightPillar,player,gameover,bgIsShifting):
        super(EnemyBackForth,self).__init__()
        self.leftPillar = leftPillar
        self.rightPillar = rightPillar
        image = pygame.image.load("snailWalk1.png").convert()
        image = pygame.transform.scale(image,(40,26))
        image.set_colorkey(black)
        shellImage = pygame.image.load("snailShell.png").convert()
        shellImage = pygame.transform.scale(shellImage,(40,26))
        shellImage.set_colorkey(black)
        self.image=image
        self.shellImage = shellImage
        self.oldImage = self.image
        self.rect = self.image.get_rect()
        self.vx = -2
        self.player = player
        self.beShell = False
        self.gameover=gameover
        self.bgIsShifting=bgIsShifting
    def update(self):
        if not self.beShell:
            self.rect.x+=self.vx
            if self.vx>0 and self.rect.right>self.rightPillar.rect.left:
                self.vx*=-1
            if self.vx<0 and self.rect.x<self.leftPillar.rect.right:
                self.vx*=-1                
            if self.vx>0:
                self.image = pygame.transform.flip(self.oldImage,1,0)
            if self.vx<0:
                self.image = pygame.transform.flip(self.oldImage,0,0)
        self.rect.top-=1
        hit = pygame.sprite.collide_rect(self,self.player)
        if hit and self.player.isJumpDown:
            self.beShell=True
            self.image = self.shellImage
            self.player.rect.bottom = self.rect.top
            self.gameover=False
            self.player.isJumpDown=False
            self.vx=0
        self.rect.top+=1
        return
        if not self.beShell:
            self.rect.left-=1

            hit = pygame.sprite.collide_rect(self,self.player)
            if hit:
                self.rect.left+=1
                self.player.rect.right = self.rect.left
                self.player.isWalking=False
                self.bgIsShifting=False
                self.vx=0
                return
            else:
                self.rect.left+=1
            self.rect.right+=1
            hit = pygame.sprite.collide_rect(self,self.player)
            if hit:
                self.player.rect.left = self.rect.right
                self.player.isWalking=False
                self.bgIsShifting=False
                self.rect.right-=1
                self.vx=0
                return
            else:
                self.rect.right-=1
        if self.beShell:

            self.rect.left-=1

            hit = pygame.sprite.collide_rect(self,self.player)
            if hit:
                self.rect.x+=self.vx
                if self.vx>0 and self.rect.right>self.rightPillar.rect.left:
                    self.vx*=-1
                    
                if self.vx<0 and self.rect.x<self.leftPillar.rect.right:
                    self.vx*=-1 
                self.rect.left+=1
                

            self.rect.right+=1
            hit = pygame.sprite.collide_rect(self,self.player)
            if hit:
                self.rect.x+=self.vx
                if self.vx>0 and self.rect.right>self.rightPillar.rect.left:
                    self.vx*=-1
                    
                if self.vx<0 and self.rect.x<self.leftPillar.rect.right:
                    self.vx*=-1 
                self.rect.right-=1  
class PlayerWife(pygame.sprite.Sprite):
    def __init__(self):
        super(PlayerWife,self).__init__()
        image1 = pygame.image.load("wifeWalk1.png").convert()
        image1.set_colorkey(black)
        image1 = pygame.transform.scale(image1,(40,60))
        self.image1 =pygame.transform.flip(image1,True,False)
        image2 = pygame.image.load("wifeWalk2.png").convert()
        image2.set_colorkey(black)
        image2 = pygame.transform.scale(image2,(40,60))
        self.image2 =pygame.transform.flip(image2,True,False)
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.vx = 0
        self.ax = 0.1
    def walk(self):
        if self.vx>=0 and self.vx<4:
            self.vx+=self.ax
    def update(self):
        self.walk()

        self.rect.x-=self.vx
        if self.rect.x%10>5:
            self.image=self.image1
        else:
            self.image=self.image2

class Player(pygame.sprite.Sprite):
    def __init__(self,gameover):
        super(Player,self).__init__()

        self.gameover=gameover
        image = pygame.image.load("walkRight2.png").convert()
        image.set_colorkey(black)
        image = pygame.transform.scale(image,(40,60))
        self.image = image
        self.rect = self.image.get_rect()
        self.vx = 0
        self.vy = 0
        self.isJumpUp = False
        self.isJumpDown = False
        self.vy0 = 30
        self.ay = 3
        self.vx = 0
        self.ax = 0.1
        self.isWalking = False
        self.goToBgShift=False

    def walk(self):
        if self.vx>=0 and self.vx<4:
            self.vx+=self.ax
        elif self.vx<0 and self.vx>-4:
            self.vx-=self.ax
        
    def jumpUp(self):
        if self.vy==0:
            self.vy=-self.vy0
        else:
            self.vy+=self.ay
    def jumpDown(self):
        self.vy+=2   
    def stop(self):
        self.vx=0
        self.vy=0
    def update(self,platformList,enemyList,slopeList,toTheEnd):
        if not self.gameover:
            canvasWidth = 1000
            if self.isWalking or toTheEnd:
                self.walk()
            if (self.rect.x>canvasWidth/2 and self.vx>0) and not toTheEnd:
                self.goToBgShift = True
                self.isWalking=False
                self.vx=0
            self.rect.x+=self.vx
            playerHitEnemy = pygame.sprite.spritecollide(self,enemyList,False)
            if(len(playerHitEnemy)>0):
                for enemy in playerHitEnemy:
                    if self.vx>0:
                        self.rect.x = enemy.rect.left-self.rect.width
                    if self.vx<0:
                        self.rect.x = enemy.rect.right
                    playerHitEnemy=[]
                    self.vx=0
                    self.isWalking=False
                    self.goToBgShift=False

            playerHitplatform = pygame.sprite.spritecollide(self,platformList,
                False)
            if(len(playerHitplatform)>0):
                for platform in playerHitplatform:
                    if self.vx>0:
                        self.rect.x = platform.rect.left-self.rect.width
                    if self.vx<0:
                        self.rect.x = platform.rect.right
                    playerHitplatform=[]
                    self.vx=0
                    self.isWalking=False
            playerHitSlope = pygame.sprite.spritecollide(self,slopeList,False)
            if len(playerHitSlope)>0 and self.isJumpUp==False:
                self.isJumpDown=False
                for slope1 in slopeList:
                    if self.rect.right<slope1.rect.left+slope1.rect.width/3:
                        
                        self.rect.bottom = \
                        slope1.rect.bottom-slope1.rect.height/3
                    if (self.rect.right>=slope1.rect.left+slope1.rect.width/3 
                        and 
                    self.rect.right<slope1.rect.left+slope1.rect.width*2/3):
                        self.rect.bottom =slope1.rect.bottom-\
                        (self.rect.right-slope1.rect.left-slope1.rect.width/3+
                            slope1.rect.height/3)
                    if self.rect.right>slope1.rect.left+slope1.rect.width*2/3:
                        self.rect.bottom = slope1.rect.top
                self.vy=0
                return 
            self.rect.y+=self.vy
            playerHitplatform = pygame.sprite.spritecollide(self,platformList,
                False)
            playerHitEnemy = pygame.sprite.spritecollide(self,enemyList,False)
            if(len(playerHitEnemy)>0):
                for enemy in playerHitEnemy:
                    if self.vy>0:
                       
                        self.rect.bottom = enemy.rect.top
                        self.vy = 0
                        self.isJumpDown=False
                    playerHitplatform=[]         
            if(len(playerHitplatform)>0):
                for platform in playerHitplatform:
                    if self.vy>0:
                        self.rect.bottom = platform.rect.top
                        self.vy = 0
                        self.isJumpDown=False
                    if self.vy<0:
                        self.rect.top = platform.rect.bottom
                        self.isJumpUp=False
                        self.isJumpDown=True
                        self.vy=0
                    playerHitplatform=[]
class BloodBar(pygame.sprite.Sprite):
    def __init__(self,width):
        super(BloodBar,self).__init__()
        self.image = pygame.Surface([width,20])
        self.image.fill(red)
        self.rect = self.image.get_rect()
class Frog(pygame.sprite.Sprite):
    def __init__(self):
        super(Frog,self).__init__()
        self.image1 = pygame.image.load("frog.png").convert()
        self.image1.set_colorkey(black)
        self.image1 = pygame.transform.scale(self.image1,(58,39))
        self.image2 = pygame.transform.flip(self.image1,True,False)
        self.image3 = pygame.image.load("frog_leap.png").convert()
        self.image3.set_colorkey(black)
        self.image3 = pygame.transform.scale(self.image3,(61,54))
        self.image4 = pygame.transform.flip(self.image3,True,False)
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.vx = 15
        self.vy0 = 30
        self.ay = 3
        self.vy = 0
        self.isJumpDown=False
        self.isJumpUp=False
    def jumpUp(self):
        if self.vy==0:
            self.vy=-self.vy0
        else:
            self.vy+=self.ay
    def jumpDown(self):
        self.vy+=2   
    def update(self,platformList,ground7):
        self.rect.y+=self.vy
        canvasHeight=600
        groundHeight = 70
        if self.vx>0 and self.rect.bottom!=canvasHeight-groundHeight:
            self.image = self.image3
        if self.vx<0 and self.rect.bottom!=canvasHeight-groundHeight:
            self.image = self.image4
        if self.vx>0 and self.rect.x<0:
            self.vx*=-1
        if self.vx<0 and self.rect.x>1000-self.rect.width:
            self.vx*=-1
        if self.isJumpUp:
            self.rect.x-=self.vx
        if(self.isJumpUp==True):
            if (self.vy<=0):
                self.jumpUp()
                if (self.vy>=0):
                    self.isJumpUp=False
                    self.isJumpDown=True
        if self.isJumpDown==True:
            if (self.rect.bottom<canvasHeight-groundHeight):
                self.jumpDown()
            else:
                self.vy=0
                self.rect.bottom=canvasHeight-groundHeight
                self.isJumpDown=False
                self.isJumpUp = False
                if self.vx>0:
                    self.image = self.image1
                else:
                    self.image = self.image2
class Bullet(pygame.sprite.Sprite):
    def __init__(self,facingRight,facingLeft):
        super(Bullet,self).__init__()
        if (facingRight):
            self.image = pygame.image.load("bulletRight.png").convert()
            self.image.set_colorkey(black)
            self.v = 20
        if(facingLeft):
            self.v = -20
            self.image = pygame.image.load("bulletLeft.png").convert()
            self.image.set_colorkey(black)
        self.a = 0.2
        self.rect = self.image.get_rect()
    def changeV(self):
        if self.v>5:
            self.v-=self.a
        if self.v<-5:
            self.v+=self.a
    def update(self):
        self.rect.x+=self.v
class VerticalBullet(pygame.sprite.Sprite):
    def __init__(self):
        super(VerticalBullet,self).__init__()
        self.image = pygame.image.load("bulletDown.png").convert()
        self.image.set_colorkey(black)
        self.v = 20
        self.a = 0.2
        self.rect = self.image.get_rect()
    def update(self):
        if self.v>5:
            self.v-=self.a
        self.rect.y+=self.v     
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super(Platform,self).__init__()
        self.image = pygame.image.load("Tiles.png").convert()
        self.image = pygame.transform.scale(self.image,(350/2,35))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
    def update(self):
        pass
class PlatformWithTorch(pygame.sprite.Sprite):
    def __init__(self):
        super(PlatformWithTorch,self).__init__()
        self.image = pygame.image.load("Tiles.png").convert()
        self.image = pygame.transform.scale(self.image,(350/2,35))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
    def update(self):
        pass
class Pillar(pygame.sprite.Sprite):
    def __init__(self):
        super(Pillar,self).__init__()
        self.image = pygame.image.load("pillar.png").convert()
        self.image = pygame.transform.scale(self.image,(60,120))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
    def update(self):
        pass
class Slope(pygame.sprite.Sprite):
    def __init__(self):
        super(Slope,self).__init__()
        self.image = pygame.image.load("slope.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(420,210))
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
    def update(self):
        pass
class Rock(pygame.sprite.Sprite):
    def __init__(self,slope,canvasHeight):
        super(Rock,self).__init__()
        self.image = pygame.image.load("rock.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(25,25))
        self.image.set_colorkey(white)
        self.oldImage = self.image
        self.rect = self.image.get_rect()
        self.rect.right = slope.rect.x+slope.rect.width*2/3+self.rect.width/6
        self.rect.bottom = slope.rect.top
        self.slope = slope
        self.canvasHeight=canvasHeight
        self.vy=1
    def update(self,player):
        if player.rect.right>self.slope.rect.left:
            if self.rect.x%12==0:
                self.image = pygame.transform.rotate(self.oldImage,-90)
            if self.rect.x%12==3:
                self.image = pygame.transform.rotate(self.oldImage,-180)
            if self.rect.x%12==6:
                self.image = pygame.transform.rotate(self.oldImage,-270)
            if self.rect.x%12==9:
                self.image = self.oldImage

            if self.rect.right<self.slope.rect.left:
                if self.rect.bottom<=self.canvasHeight:
                    self.vy+=0.5
                    self.rect.y+=self.vy
            else:
                self.rect.x-=0.001
            
            if self.rect.right < self.slope.rect.left+self.slope.rect.width/3:
                return
            else:
                if self.rect.bottom<=self.canvasHeight:
                    self.rect.y+=1
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super(Ground,self).__init__()
        self.image = pygame.image.load("ground.png").convert()
        self.image = pygame.transform.scale(self.image,(350,70))
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
class LongGround(pygame.sprite.Sprite):
    def __init__(self):
        super(LongGround,self).__init__()
        self.image = pygame.image.load("longGround.png").convert()
        self.image = pygame.transform.scale(self.image,(700,76))
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
class FloatingPlatform(pygame.sprite.Sprite):
    def __init__(self,leftBoundary,rightBoundary,player):
        super(FloatingPlatform,self).__init__()
        self.image = pygame.image.load("Tiles.png").convert()
        self.image = pygame.transform.scale(self.image,(170,35))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.leftBoundary = leftBoundary
        self.rightBoundary = rightBoundary
        self.vx = 2
        self.player=player
    def update(self):
        self.rect.x += self.vx
        if self.vx>0 and self.rect.x>self.rightBoundary:
            self.vx*=-1
        if self.vx<0 and self.rect.x<self.leftBoundary:
            self.vx*=-1
        self.rect.y-=1
        hitPlayer = pygame.sprite.collide_rect(self,self.player)
        if hitPlayer:
            self.player.rect.x +=self.vx
        self.rect.y+=1
class Cherry(pygame.sprite.Sprite):
    def __init__(self):
        super(Cherry,self).__init__()
        banana = pygame.image.load("banana.png").convert()
        banana = pygame.transform.scale(banana,(50,40))
        banana.set_colorkey(white)
        grapes = pygame.image.load("grapes.png").convert()
        grapes = pygame.transform.scale(grapes,(30,50))
        grapes.set_colorkey(black)
        watermelon = pygame.image.load("watermelon.png").convert()
        watermelon = pygame.transform.scale(watermelon,(50,39))
        watermelon.set_colorkey(white)
        pear = pygame.image.load("pear.png").convert()
        pear = pygame.transform.scale(pear,(30,46))
        pear.set_colorkey(black)
        strawberry = pygame.image.load("strawberry.png").convert()
        strawberry = pygame.transform.scale(strawberry,(35,35))
        strawberry.set_colorkey(white)
        cherry = pygame.image.load("cherry.png").convert()
        cherry = pygame.transform.scale(cherry,(30,34))
        cherry.set_colorkey(black)
        fruitImageList=[banana,grapes,watermelon,pear,strawberry,cherry]
        random.shuffle(fruitImageList)
        self.image = fruitImageList[random.randrange(0,len(fruitImageList)-1)]
        self.rect = self.image.get_rect()
    def update(self):
        pass
class GreenKey(pygame.sprite.Sprite):
    def __init__(self):
        super(GreenKey,self).__init__()
        self.image = pygame.image.load("greenKey.png").convert()
        self.image = pygame.transform.scale(self.image,(22,20))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
    def update():
        pass
class RedKey(pygame.sprite.Sprite):
    def __init__(self):
        super(RedKey,self).__init__()
        self.image = pygame.image.load("redKey.png").convert()
        self.image = pygame.transform.scale(self.image,(22,20))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
    def update():
        pass
class YellowKey(pygame.sprite.Sprite):
    def __init__(self):
        super(YellowKey,self).__init__()
        self.image = pygame.image.load("greenKey.png").convert()
        self.image = pygame.transform.scale(self.image,(22,20))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
    def update():
        pass
class BlueKey(pygame.sprite.Sprite):
    def __init__(self):
        super(BlueKey,self).__init__()
        self.image = pygame.image.load("blueKey.png").convert()
        self.image = pygame.transform.scale(self.image,(22,20))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
    def update():
        pass
class Flag(pygame.sprite.Sprite):
    def __init__(self):
        super(Flag,self).__init__()
        self.image = pygame.image.load("flag.png").convert()
        self.image = pygame.transform.scale(self.image,(20,20))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
    def update():
        pass
littleYellowsAdventure = LittleYellowsAdventure()
littleYellowsAdventure.init()
littleYellowsAdventure.run()


