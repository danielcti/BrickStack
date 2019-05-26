import pygame

class Hand:
    def __init__(self,x,y,speed):
        self.left_sprite = pygame.image.load('resources/left_hand.png')
        self.right_sprite = pygame.image.load('resources/right_hand.png')
        self.width = self.left_sprite.get_width()
        self.height = self.left_sprite.get_height()
        self.x = x
        self.y = y
        self.speed = speed
        self.side = 'left'
        self.contactPoint = y
        print('Hand added!')
