import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button

from stockfish import Stockfish
sf = Stockfish("C:/Users/mihir/Downloads/stockfish_15.1/stockfish.exe",depth=18,parameters={"Threads": 2, "Minimum Thinking Time": 30})

from sys import exit
from buttons import *
from helper import *
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

# background image
board_surf = loadImage('board.png').convert()
board_surf = pygame.transform.rotozoom(board_surf,0,1)
board_rect = board_surf.get_rect()
board_rect.center=(SCR_WIDTH//2,SCR_HEIGHT//2)  

# loading up all chess piece images
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

# relating piece to image
piece_image_dict = {
    'wR': white_rook,'wN': white_knight,'wB': white_bishop,'wQ': white_queen,'wK': white_king,'wP': white_pawn,
    'bR': black_rook,'bN': black_knight,'bB': black_bishop,'bQ': black_queen,'bK': black_king,'bP': black_pawn }

# initialising true board dictionary
## {a1: wR, a2: wP, a3: wB, ...}
true_board_dict = setTrueBoardDictionary()

# initialising castling dictionary
castling_dict = {
    "e1g1":("h1","f1","wR"),
    "e1c1":("a1","d1","wR"),
    "e8g8":("h8","f8","bR"),
    "e8c8":("a8","d8","bR"), 
}

# Setup - Variables
lettering = ['a','b','c','d','e','f','g','h']
numbering = ['1','2','3','4','5','6','7','8']
positions = [letter+number for letter in lettering for number in numbering]
white_dict,black_dict,STEP = setSquareCoordDictionary(positions,SCR_WIDTH)

# Menu Mode
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

# Active Mode
def ACTIVE_MODE(colour,difficulty):

    # stockfish parameters
    elo = int(difficulty / 100 * 3000)
    sf.set_elo_rating(elo) 

    # move variables
    source_sprite = None
    dest_sprite = None
    
    # instantiating square-coordinate dictionary based on colour
    ## { a1: (50,750), b2: (150,650), ...}
    sq_coord_dict = white_dict if colour=='WHITE' else black_dict

    # creating list of Square Sprites
    square_group = pygame.sprite.Group()    

    # list of squares (a1,a2,a3,...,h6,h7,h8)
    squares = list(sq_coord_dict.keys())

    # making a square sprite for each square (a1,a2,a3)
    for square in squares:

        # (50,100)  
        coord = sq_coord_dict[square]
        
        # bQ (black Queen)
        piece = true_board_dict[square]

        # instantiate instance of Square
        sq_sprite = Square(square,coord,piece,STEP)
        
        # add instance to list of Square Sprites
        square_group.add(sq_sprite)    

    def displayPiecesBasedOnTrueBoard():

        for square in squares:

            # getting piece, based on square
            piece = true_board_dict[square]
            
            # getting coordinate, based on square
            coord = sq_coord_dict[square]
            
            # getting image, based on piece
            image = piece_image_dict.get(piece)
                
            if piece:
                if (source_sprite) and (piece == source_sprite.piece) and (square == source_sprite.square): 
                    SCREEN.blit(image,image.get_rect(center=pygame.mouse.get_pos()))
                else:
                    SCREEN.blit(image,image.get_rect(center=coord))

    def doMoveIfValid(move):
        print(f"Move: {move}")
        
        if sf.is_move_correct(move):

            moving_piece = source_sprite.piece

            true_board_dict[move[0:2]] = ""
            true_board_dict[move[2:4]] = moving_piece

            source_sprite.piece = ""
            dest_sprite.piece = moving_piece

            # check for castling
            if move in list(castling_dict.keys()):
                rook_source_square = castling_dict[move][0]
                rook_dest_square = castling_dict[move][1]
                rook_colour = castling_dict[move][2]

                true_board_dict[rook_source_square] = ""
                true_board_dict[rook_dest_square] = rook_colour

                for sq_sprite in square_group:
                    if sq_sprite.square == rook_source_square: sq_sprite.piece = ""
                    if sq_sprite.square == rook_dest_square: sq_sprite.piece = rook_colour
            
            sf.make_moves_from_current_position([move])
            print(sf.get_board_visual())

    # Main Loop
    while True: 
        
        # check for events
        event_list = pygame.event.get()
        for event in event_list:

            # QUIT event
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # MOUSE CLICK event
            if event.type == pygame.MOUSEBUTTONDOWN:
                for sq_sprite in square_group:
                    if sq_sprite.rect.collidepoint(event.pos):

                        # set source sprite once mouse clicked down
                        source_sprite = sq_sprite
                        print(f"Piece: {sq_sprite.piece} | Square: {sq_sprite.square}")

            # MOUSE UNCLICK event
            if event.type == pygame.MOUSEBUTTONUP:
                for sq_sprite in square_group:
                    if sq_sprite.rect.collidepoint(event.pos) and source_sprite:
                            
                        # put the move together
                        move = source_sprite.square + sq_sprite.square
                            
                        # update destination sprite
                        dest_sprite = sq_sprite
                            
                        # perform move, if valid
                        doMoveIfValid(move)
                            
                        # reset move variables
                        source_sprite = None
                        dest_sprite = None

        # display chess board
        SCREEN.blit(board_surf,board_rect)

        # draw invisible squares
        square_group.draw(SCREEN)
      
        # based on true board dictionary, set the images of all pieces
        displayPiecesBasedOnTrueBoard()

        # update the whole screen every frame
        pygame.display.update()

        # set frame rate = 60 FPS
        CLOCK.tick_busy_loop(60)

# Initial Start
MENU_MODE()