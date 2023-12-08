#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 08:21:19 2023

@author: kenxn
"""
import simpleGE

import pygame

import random



class Player(simpleGE.SuperSprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("stillplayer.png")
        self.setSize(30,30)
        self.moveSpeed = 7
        self.setAngle(90)
        self.x = 320
        self.y = 400
        
            
        
    def checkEvents(self):
        super().checkEvents()
        """ press b key for a stream of bullets """
       
    
    
        if self.scene.isKeyPressed(pygame.K_LEFT):
            self.turnBy(8)
        if self.scene.isKeyPressed(pygame.K_RIGHT):
            self.turnBy(-8)
        if self.scene.isKeyPressed(pygame.K_UP):
            self.forward(7)
        if self.scene.isKeyPressed(pygame.K_DOWN):
            self.forward(-5)
    
    
    
class Bullet(simpleGE.SuperSprite):
    def __init__(self, scene, parent):
        super().__init__(scene)
        self.parent = parent
        self.imageMaster = pygame.Surface((3, 3))
        self.imageMaster.fill(pygame.Color("white"))
        self.setBoundAction(self.HIDE)
        self.hide()
        
    def fire(self):
        self.show()
        self.setPosition(self.parent.rect.center)
        self.setMoveAngle(self.parent.rotation)
        self.setSpeed(20)

    

class Grass(simpleGE.BasicSprite):
    """ falls from top of screen at random speed
       when reset appears at new speed and position
       at top of screen """
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("grass.png")
        self.x = 320
        self.y = 240
        
        
        

        
        
class Zombie(simpleGE.BasicSprite):
    """ falls from top of screen at random speed
       when reset appears at new speed and position
       at top of screen """
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("zombie.png")
        self.setSize(30, 30)
        self.bulletsound = simpleGE.Sound("zombieshot.wav")
        self.reset()

    def reset(self):
        newX = random.randint(0, 640) 
        self.x = newX
        self.y = 7
        self.dy = random.randint(3,7)

    def checkEvents(self):
            if self.collidesWith(self.scene.player):
                self.stop()
                self.reset()
  
            if self.collidesGroup(self.scene.bullets):
                self.scene.score += 100
                self.bulletsound.play()
                self.reset()

            
         
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setCaption("Arrows to control, Space for bullet, b for bullet stream")
        self.player = Player(self)
        self.NUM_BULLETS = 100
        self.currentBullet = 0       
        self.bullets = []
        
       
        for i in range(self.NUM_BULLETS):
            self.bullets.append(Bullet(self, self.player))
                        
            
        self.grass = []
        for i in range(1):
            self.grass.append(Grass(self))
            
        
        self.zombie = []
        for i in range(16):
            self.zombie.append(Zombie(self))
            
            
        self.lblScore = simpleGE.Label()
        self.lblScore.text = "Score: 0"
        self.lblScore.center = (80, 50)
        self.score = 0
        
        self.lblTime = simpleGE.Label()
        self.lblTime.text = "Time Survived: 30"
        self.lblTime.center = (500, 50)
    
        
        self.timer = simpleGE.Timer()
        
        
            
        self.sprites = [self.grass, self.player, self.zombie, self.bullets, self.lblTime, self.lblScore ]


    def doEvents(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.currentBullet += 1
                pygame.image.load("shootingplayer.png")
                if self.currentBullet >= self.NUM_BULLETS:
                    self.currentBullet = 0
                self.bullets[self.currentBullet].fire()
        
        
    def update(self):
        timeLeft = 30 - self.timer.getElapsedTime()
        if timeLeft < 0:
            self.stop()
        
            
        self.lblTime.text = f"Time Left: {timeLeft:.2f}"
        self.lblScore.text = f"Score: {self.score}"
        
def main():
    
    
    game = Game()
    game.start()
    pygame.quit()
    
    
if __name__ == "__main__":
    main() 