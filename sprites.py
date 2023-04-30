import pygame
from helper import *

class Square(pygame.sprite.Sprite):
    def __init__(self,square,coord,piece,piece_image,STEP):
        super().__init__()

        self.square = square
        self.coord = coord
        self.piece = piece
        self.piece_image = piece_image

        self.image = pygame.Surface((STEP*2,STEP*2),pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=coord)

        self.piece_image = piece_image
    
    def check_clicked(self,event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    return (self.piece,self.piece_image,self.square)
        return False

    def check_unclicked(self,event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    return (self.piece,self.piece_image,self.square)
        return False