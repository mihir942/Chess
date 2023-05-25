import pygame
import os

# Function to load image resources
def loadImage(name):
    working_dir = os.path.dirname(__file__)
    return pygame.image.load(working_dir + "/images/" + name)

# Function to load font resources
def loadFont(name,size):
    working_dir = os.path.dirname(__file__)
    full_path = working_dir + "/font/" + name
    return pygame.font.Font(full_path,size)

def loadStockfish():
    working_dir = os.path.dirname(__file__)
    full_path = working_dir + "/stockfish/" + "stockfish.exe"
    return full_path

# Function to generate square-coordinate dictionary. 
## { a1: (50,750), b2: (150,650), ...}
def setSquareCoordDictionary(positions,SCREEN_WIDTH) -> tuple:

    SMALL = SCREEN_WIDTH // 16
    BIG = SCREEN_WIDTH - SMALL
    x_coord = list(range(SMALL,BIG+SMALL,SMALL*2))
    y_coord = list(reversed(x_coord))
    coordinates = [(x,y) for x in x_coord for y in y_coord]
    white_dict = dict(zip(positions,coordinates))
    black_dict = dict(zip(list(reversed(positions)),coordinates))
    return (white_dict,black_dict,SMALL)

# Function to set true board dictionary
## {a1: wR, a2: wP, a3: wB, ...}
def setTrueBoardDictionary() -> dict:
    return {
            'a8': 'bR','b8': 'bN','c8': 'bB','d8': 'bQ','e8': 'bK','f8': 'bB','g8': 'bN','h8': 'bR',
            'a7': 'bP','b7': 'bP','c7': 'bP','d7': 'bP','e7': 'bP','f7': 'bP','g7': 'bP','h7': 'bP',
            'a6': '','b6': '','c6': '','d6': '','e6': '','f6': '','g6': '','h6': '',
            'a5': '','b5': '','c5': '','d5': '','e5': '','f5': '','g5': '','h5': '',
            'a4': '','b4': '','c4': '','d4': '','e4': '','f4': '','g4': '','h4': '',
            'a3': '','b3': '','c3': '','d3': '','e3': '','f3': '','g3': '','h3': '',
            'a2': 'wP','b2': 'wP','c2': 'wP','d2': 'wP','e2': 'wP','f2': 'wP','g2': 'wP','h2': 'wP',
            'a1': 'wR','b1': 'wN','c1': 'wB','d1': 'wQ','e1': 'wK','f1': 'wB','g1': 'wN','h1': 'wR'
        }

