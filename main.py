import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button

import os
from sys import exit
from helper import *
from buttons import *

# Setup - Admin
pygame.init()
pygame.display.set_caption("chess")
SCR_WIDTH = 800
SCR_HEIGHT = 800
SCREEN = pygame.display.set_mode((SCR_WIDTH,SCR_HEIGHT))
CLOCK = pygame.time.Clock()
gilroyregular30 = loadFont('gilroy_regular.ttf',30)
gilroyregular40 = loadFont('gilroy_regular.ttf',40)
gilroyblack80 = loadFont('gilroy_black.ttf',80)
gilroybold40 = loadFont('gilroy_bold.ttf',40)
gilroybold30 = loadFont('gilroy_bold.ttf',30)

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
    button = Button(SCREEN,325,650,150,70,
                    text="PLAY",
                    textHAlign='centre',
                    textVAlign='centre',
                    fontSize=60,
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
        textbox.setText(f"Difficulty: {slider.getValue()}")

        # widgets 
        pygame_widgets.update(event_list)

        # update the whole screen every frame
        pygame.display.update()

        # set frame rate = 60 FPS
        CLOCK.tick_busy_loop(60)

def ACTIVE_MODE(colour,difficulty):

    board = loadImage('board.png').convert_alpha()
    board = pygame.transform.rotozoom(board,0,1)
    board_rect = board.get_rect()
    board_rect.center=(SCR_WIDTH//2,SCR_HEIGHT//2)

    # Main Loop
    while True:    

        # check for events
        for event in pygame.event.get():

            # QUIT event
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # display chess board
        SCREEN.blit(board,board_rect)

        # update the whole screen every frame
        pygame.display.update()

        # set frame rate = 60 FPS
        CLOCK.tick_busy_loop(60)

# Initial Start
MENU_MODE()