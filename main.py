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
    move_mode = "UP"
    move_piece = ""
    move_piece_image = None
    move_square_source = ""
    move_square_dest = ""
    move_square_sprite_source = None
    move_square_sprite_dest = None

    # instantiating square-coordinate dictionary based on colour
    ## { a1: (50,750), b2: (150,650), ...}
    sq_coord_dict = white_dict if colour=='WHITE' else black_dict

    # creating list of Square Sprites
    square_group = pygame.sprite.Group()    

    # list of squares (a1,a2,a3,...,h6,h7,h8)
    keys = list(sq_coord_dict.keys())

    # making a square sprite for each square (a1,a2,a3)
    for square in keys:

        # (50,100)  
        coord = sq_coord_dict[square]
        
        # bQ (black Queen)
        piece = true_board_dict[square]
        
        # piece image (white_rook)
        # if piece_image is None, so be it. 
        piece_image = piece_image_dict.get(piece)

        # instantiate instance of Square
        sq_sprite = Square(square,coord,piece,piece_image,STEP)
        
        # add instance to list of Square Sprites
        square_group.add(sq_sprite)    

    def displayPiecesBasedOnTrueBoard():

        for square in keys:

            # getting piece, based on square
            piece = true_board_dict[square]
            
            # getting coordinate, based on square
            coord = sq_coord_dict[square]
            
            # getting image, based on piece
            image = piece_image_dict.get(piece)
                
            # if there is a piece (meaning image != None) then display it
            if piece: 
                
                # manually checks every piece to see whether it's being clicked on

                # clicked on => then blit the image at the mouse position
                if (piece == move_piece) and (square == move_square_source) and (move_mode == "DOWN"):
                    SCREEN.blit(image,image.get_rect(center=pygame.mouse.get_pos()))
                
                # not clicked on => blit the image at its coordinates, as found from true board
                else:        
                    SCREEN.blit(image,image.get_rect(center=coord))

    # if user's colour is black, computer makes the first move 
    if colour == 'BLACK':
        computer_move = sf.get_best_move_time(200)
        sf.make_moves_from_current_position([computer_move])
        source = computer_move[0:2]
        dest = computer_move[2:4]
        piece_to_move = true_board_dict[source]
        true_board_dict[source] = ""
        true_board_dict[dest] = piece_to_move
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

        # display chess board
        SCREEN.blit(board_surf,board_rect)

        # draw invisible squares
        square_group.draw(SCREEN)
        
        # check for moves
        for sq_sprite in square_group:
            
            # check if the square is clicked on AND has a piece attached to it
            clicked = sq_sprite.check_clicked(event_list)
            
            if sq_sprite.piece and clicked:

                # set the "move" variables    
                move_mode = "DOWN"
                move_piece = clicked[0]
                move_piece_image = clicked[1]
                move_square_source = clicked[2]
                move_square_sprite_source = sq_sprite

            # which square the mouse has been unclicked on? (to make the move)
            unclicked = sq_sprite.check_unclicked(event_list)
            
            if unclicked and move_mode == "DOWN":
                    
                move_mode = "UP"
                move_square_dest = unclicked[2]
                move_square_sprite_dest = sq_sprite
                move = move_square_source+move_square_dest
                
                # if move is valid
                if sf.is_move_correct(move):
                        
                    # play move

                    # set true board dictionary to new values. source to empty. dest to the piece moved
                    true_board_dict[move_square_source] = ""
                    true_board_dict[move_square_dest] = move_piece

                    # update the display with the true board ** NOTE the dual call of pygame.display.update()
                    displayPiecesBasedOnTrueBoard()
                    pygame.display.update()

                    # resetting the "move" variables
                    move_square_sprite_source.piece = ""
                    move_square_sprite_source.piece_image = None

                    move_square_sprite_dest.piece = move_piece
                    move_square_sprite_dest.piece_image = move_piece_image
                        
                    sf.make_moves_from_current_position([move])
                        
                    print("Move:",move)
                    print(sf.get_board_visual())
                   
                        
                    # if, after the player moved, it's checkmate or stalemate, end the game, go to MENU
                    eval = sf.get_evaluation()
                    eval_type = eval["type"]
                    if (eval_type == "mate") or len(sf.get_top_moves()) == 0:
                        print("Checkmate/Stalemate")
                        MENU_MODE()
                    
                    # if all is good (no mates), play computer move
                    else:

                        # play computer move
                        computer_move = sf.get_best_move_time(200)
                        sf.make_moves_from_current_position([computer_move])
                        source = computer_move[0:2]
                        dest = computer_move[2:4]
                        piece_to_move = true_board_dict[source]
                        true_board_dict[source] = ""
                        true_board_dict[dest] = piece_to_move
                        print(sf.get_board_visual())

                move_piece = ""
                move_piece_image = None
                move_square_source = ""
                move_square_dest = ""
                move_square_sprite_source = None
                move_square_sprite_dest = None

        # based on true board dictionary, set the images of all pieces
        displayPiecesBasedOnTrueBoard()

        # update the whole screen every frame
        pygame.display.update()

        # set frame rate = 60 FPS
        CLOCK.tick_busy_loop(60)

# Initial Start
MENU_MODE()