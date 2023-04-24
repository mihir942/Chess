import pygame
import os
from sys import exit

# Functions to load resources
def loadImage(name):
    working_dir = os.path.dirname(__file__)
    return pygame.image.load(working_dir + "/images/" + name)

def loadFont(name,size):
    working_dir = os.path.dirname(__file__)
    full_path = working_dir + "/font/" + name
    return pygame.font.Font(full_path,size)

# Setup - Admin
pygame.init()
pygame.display.set_caption("Chess")
SCR_WIDTH = 800
SCR_HEIGHT = 800
screen = pygame.display.set_mode((SCR_WIDTH,SCR_HEIGHT))
clock = pygame.time.Clock()

# Main Loop
while True:    

    # check for events
    for event in pygame.event.get():

        # QUIT event
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # update the whole screen every frame
    pygame.display.update()

    # set frame rate = 60 FPS
    clock.tick_busy_loop(60)
