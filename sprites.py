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
        self.highlight = False

    def update(self,event_list):

        if self.highlight:
            self.image.fill((235, 210, 52))
        else:
            self.image.fill((0,0,0,0))

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    print(self.piece)
                    if self.piece: self.highlight = not self.highlight