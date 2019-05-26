import pygame

class Brick:
    def __init__(self,x,y,speed):  
        self.x = x  
        self.y = y
        self.sprite = pygame.image.load('resources/brick.png')
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.speed = speed
        self.collide = False
        print('New brick added')
