import pygame
import os

# Functions to load resources
def loadImage(name):
    working_dir = os.path.dirname(__file__)
    return pygame.image.load(working_dir + "/images/" + name)

def loadFont(name,size):
    working_dir = os.path.dirname(__file__)
    full_path = working_dir + "/font/" + name
    return pygame.font.Font(full_path,size)

# Function to generate and map coordinates
def setCoordinates(positions,SCREEN_WIDTH):

    SMALL = SCREEN_WIDTH // 16
    BIG = SCREEN_WIDTH - SMALL
    x_coord = list(range(SMALL,BIG+SMALL,SMALL*2))
    y_coord = list(reversed(x_coord))
    coordinates = [(x,y) for x in x_coord for y in y_coord]

    white_dict = dict(zip(positions,coordinates))
    black_dict = dict(zip(list(reversed(positions)),coordinates))

    return (white_dict,black_dict,SMALL)