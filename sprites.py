import pygame
from helper import *

class Square(pygame.sprite.Sprite):
    def __init__(self,square,coord,piece,STEP):
        super().__init__()

        self.square = square
        self.coord = coord
        self.piece = piece

        self.image = pygame.Surface((STEP*2,STEP*2),pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=coord)

