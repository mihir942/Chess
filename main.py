import pygame
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
gilroy_regular = loadFont('gilroy_regular.ttf',30)
gilroy_black = loadFont('gilroy_black.ttf',80)


def MENU_MODE():
    
    # background
    background = loadImage('background.jpg').convert_alpha()
    background = pygame.transform.rotozoom(background,0,0.7)
    background_rect = background.get_rect(center=(SCR_WIDTH//2,SCR_HEIGHT//2))

    # title
    title = gilroy_black.render("chess",True,'White')
    title_rect = title.get_rect(center=(SCR_WIDTH//2,SCR_HEIGHT//4))


    font50 = pygame.font.SysFont(None, 50)

    radioButtons = [
        RadioButton(50, 40, 200, 60, font50, "WHITE"),
        RadioButton(50, 120, 200, 60, font50, "BLACK"),
    ]
    for rb in radioButtons:
        rb.setRadioButtons(radioButtons)
    radioButtons[0].clicked = True

    group = pygame.sprite.Group(radioButtons)

    # Main Loop
    while True:
        
        # check for events
        event_list = pygame.event.get()
        for event in event_list:

            # QUIT event
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # display background, title        
        SCREEN.blit(background,background_rect)
        SCREEN.blit(title,title_rect)

        group.update(event_list)
        group.draw(SCREEN)

        # update the whole screen every frame
        pygame.display.update()

        # set frame rate = 60 FPS
        CLOCK.tick_busy_loop(60)

def ACTIVE_MODE(color):

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