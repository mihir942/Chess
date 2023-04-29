import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button

import os
from sys import exit
from helper import *
from buttons import *
from sprites import *

# Setup - Admin
pygame.init()
pygame.display.set_caption("chess")
SCR_WIDTH = 800
SCR_HEIGHT = 800
SCREEN = pygame.display.set_mode((SCR_WIDTH,SCR_HEIGHT))
CLOCK = pygame.time.Clock()
gilroyregular30 = loadFont('gilroy_regular.ttf',30)
gilroyregular40 = loadFont('gilroy_regular.ttf',40)
gilroybold30 = loadFont('gilroy_bold.ttf',30)
gilroybold40 = loadFont('gilroy_bold.ttf',40)
gilroyblack80 = loadFont('gilroy_black.ttf',80)

# Setup - Variables
lettering = ['a','b','c','d','e','f','g','h']
numbering = ['1','2','3','4','5','6','7','8']
positions = [letter+number for letter in lettering for number in numbering]
white_dict,black_dict,STEP = setSquareCoordDictionary(positions,SCR_WIDTH)

def MENU_MODE():

    def play():
        colour = ''
        if radioButtons[0].clicked: colour = 'WHITE'
        else: colour = 'BLACK'

        difficulty = slider.getValue()
        ACTIVE_MODE(colour,difficulty)

    # background
    background = loadImage('background.jpg').convert_alpha()
    background = pygame.transform.rotozoom(background,0,0.7)
    background_rect = background.get_rect(center=(SCR_WIDTH//2,SCR_HEIGHT//2))

    # title
    title = gilroyblack80.render("chess",True,'White')
    title_rect = title.get_rect(center=(SCR_WIDTH//2,SCR_HEIGHT//4))

    # radio button (white/black)
    radioButtons = [
        RadioButton(300, 300, 200, 60, gilroybold40, "white"),
        RadioButton(300, 380, 200, 60, gilroybold40, "black"),
    ]
    for rb in radioButtons: rb.setRadioButtons(radioButtons)
    radioButtons[0].clicked = True
    group = pygame.sprite.Group(radioButtons)

    # slider, textbox
    slider = Slider(SCREEN,250,570,300,30,min=1,max=100,step=1,handleColour=(127, 85, 57),curved=True,initial=50)
    textbox = TextBox(SCREEN,300,500,200,50,font=gilroyregular30,borderThickness=0,radius=0,colour=(200,200,200))
    textbox.disable()

    # play button
    button = Button(SCREEN,350,650,100,70,
                    text="play",
                    textHAlign='centre',
                    textVAlign='centre',
                    font=gilroybold40,
                    textColour=(0,0,0),
                    inactiveColour=(200,200,200),
                    hoverColour=(176, 137, 104),
                    onClick=play,
                    )

    # Main Loop
    while True:
        
        # check for events
        event_list = pygame.event.get()
        for event in event_list:

            # QUIT event
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # display background, title, radio buttons        
        SCREEN.blit(background,background_rect)
        SCREEN.blit(title,title_rect)
        group.update(event_list)
        group.draw(SCREEN)

        # display textbox
        textbox.setText(f"difficulty: {slider.getValue()}")

        # widgets 
        pygame_widgets.update(event_list)

        # update the whole screen every frame
        pygame.display.update()

        # set frame rate = 60 FPS
        CLOCK.tick_busy_loop(60)

def ACTIVE_MODE(colour,difficulty):

    # background image
    board_surf = loadImage('board.png').convert()
    board_surf = pygame.transform.rotozoom(board_surf,0,1)
    board_rect = board_surf.get_rect()
    board_rect.center=(SCR_WIDTH//2,SCR_HEIGHT//2)

    # chess pieces
    white_rook = pygame.transform.rotozoom(loadImage('white_rook.png'),0,0.2) 
    white_knight = pygame.transform.rotozoom(loadImage('white_knight.png'),0,0.2)
    white_bishop = pygame.transform.rotozoom(loadImage('white_bishop.png'),0,0.2)
    white_queen = pygame.transform.rotozoom(loadImage('white_queen.png'),0,0.2)
    white_king = pygame.transform.rotozoom(loadImage('white_king.png'),0,0.2)
    white_pawn = pygame.transform.rotozoom(loadImage('white_pawn.png'),0,0.2)

    black_rook = pygame.transform.rotozoom(loadImage('black_rook.png'),0,0.2)
    black_knight = pygame.transform.rotozoom(loadImage('black_knight.png'),0,0.2)
    black_bishop = pygame.transform.rotozoom(loadImage('black_bishop.png'),0,0.2)
    black_queen = pygame.transform.rotozoom(loadImage('black_queen.png'),0,0.2)
    black_king = pygame.transform.rotozoom(loadImage('black_king.png'),0,0.2)
    black_pawn = pygame.transform.rotozoom(loadImage('black_pawn.png'),0,0.2)        

   # initialising true board
    true_board = setTrueBoardDictionary()

    # initialising Square Sprites
    square_group = pygame.sprite.Group()
    sq_coord_dict = white_dict if colour=='WHITE' else black_dict
    for square in list(sq_coord_dict.keys()):
        coord = sq_coord_dict[square]
        piece = true_board[square]
        sq = Square(square,coord,STEP,piece)
        square_group.add(sq)    

    def displayPiecesBasedOnTrueBoard():
        for square in list(true_board.keys()):
            piece = true_board[square]
            coord = sq_coord_dict[square]
            if piece == 'wR':  SCREEN.blit(white_rook,white_rook.get_rect(center=coord))
            elif piece == 'wN': SCREEN.blit(white_knight,white_knight.get_rect(center=coord))
            elif piece == 'wB': SCREEN.blit(white_bishop,white_bishop.get_rect(center=coord))
            elif piece == 'wQ': SCREEN.blit(white_queen,white_queen.get_rect(center=coord))
            elif piece == 'wK': SCREEN.blit(white_king,white_king.get_rect(center=coord))
            elif piece == 'wP': SCREEN.blit(white_pawn,white_pawn.get_rect(center=coord))
            elif piece == 'bR':  SCREEN.blit(black_rook,black_rook.get_rect(center=coord))
            elif piece == 'bN': SCREEN.blit(black_knight,black_knight.get_rect(center=coord))
            elif piece == 'bB': SCREEN.blit(black_bishop,black_bishop.get_rect(center=coord))
            elif piece == 'bQ': SCREEN.blit(black_queen,black_queen.get_rect(center=coord))
            elif piece == 'bK': SCREEN.blit(black_king,black_king.get_rect(center=coord))
            elif piece == 'bP': SCREEN.blit(black_pawn,black_pawn.get_rect(center=coord))         

    # Main Loop
    while True: 

        # check for events
        event_list = pygame.event.get()
        for event in event_list:

            # QUIT event
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # display chess board
        SCREEN.blit(board_surf,board_rect)

        # draw invisible squares
        square_group.draw(SCREEN)
        square_group.update(event_list)

        # set initial starting pieces
        displayPiecesBasedOnTrueBoard()

        # update the whole screen every frame
        pygame.display.update()

        # set frame rate = 60 FPS
        CLOCK.tick_busy_loop(60)

# Initial Start
MENU_MODE()