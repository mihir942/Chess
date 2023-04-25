import pygame

class Square(pygame.sprite.Sprite):
    def __init__(self,position,coord,step):
        super().__init__()

        self.position = position
        self.coord = coord

        self.image = pygame.Surface((step*2,step*2),pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=coord)
    
    def update(self,event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    print(self.position)