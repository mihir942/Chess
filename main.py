import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button

from stockfish import Stockfish
SF = Stockfish("C:/Users/mihir/Downloads/stockfish_15.1/stockfish.exe",depth=18,parameters={"Hash":64,"Threads": 8, "Minimum Thinking Time": 30})
import chess

from random import randint
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
def ACTIVE_MODE(player_colour,difficulty):

    # game state variable, has 3 values: "ongoing","mate","promotion"
    game_state = "ongoing"

    # setting difficulty of stockfish
    elo = int(difficulty / 100 * 2000)
    SF.set_elo_rating(elo) 

    # reset stockfish to initial position
    SF.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    
    # initialising true board dictionary
    ## {a1: wR, a2: wP, a3: wB, ...}
    true_board_dict = setTrueBoardDictionary()

    # move variables
    source_sprite = None
    dest_sprite = None
    turn = "WHITE"
    highlight_sprite_1 = None
    highlight_sprite_2 = None

    # instantiating square-coordinate dictionary based on colour
    ## { a1: (50,750), b2: (150,650), ...}
    sq_coord_dict = white_dict if player_colour=='WHITE' else black_dict

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

    def unhighlightAllSprites():
        for sq_sprite in square_group:
            sq_sprite.image.fill((0,0,0,0))

    # based on true board dictionary, show the piece images on screen at the right positions
    def displayPiecesBasedOnTrueBoard():

        for square in squares:

            # getting piece, based on square
            piece = true_board_dict[square]
            
            # getting coordinate, based on square
            coord = sq_coord_dict[square]
            
            # getting image, based on piece
            image = piece_image_dict.get(piece)
            
            # if there is a piece on the square
            if piece:

                # if source sprite exists, AND the piece + square match source sprite's, 
                # aka it's being dragged upon by the mouse
                # make it follow mouse position 
                if source_sprite and (piece == source_sprite.piece) and (square == source_sprite.square): 
                    SCREEN.blit(image,image.get_rect(center=pygame.mouse.get_pos()))
                    
                # otherwise, make piece appear at coordinates as specified by dictionary
                else:
                    try:
                        SCREEN.blit(image,image.get_rect(center=coord))
                    except AttributeError as err:
                            print(f"DEBUG,{piece},{image},{square}")

    # This function checks for "Castling".
    # Updates the rook movement based on hardcoded values in castling_dict
    # Why? The move alone only updates the king's values. 
    def castlingRookUpdate(move,piece):

        # if move is one of 4 legal castling moves...
        if move in list(castling_dict.keys()) and (piece == "wK" or piece == "bK"):

            # getting rook's movement info from castling_dict
            rook_source_square = castling_dict[move][0]
            rook_dest_square = castling_dict[move][1]
            rook_colour = castling_dict[move][2]

            # updating rook movement in true board
            true_board_dict[rook_source_square] = ""
            true_board_dict[rook_dest_square] = rook_colour

            # updating rook movement amongst the sprites
            for sq_sprite in square_group:
                 if sq_sprite.square == rook_source_square: sq_sprite.piece = ""
                 if sq_sprite.square == rook_dest_square: sq_sprite.piece = rook_colour  

    # This function checks for "En Passant".
    # Updates the captured pawn square on true board, and its related sprite
    # Why? "En Passant" is a special move, for which the pawn taken is horizontally beside the pawn taking. 
    def enPassantUpdate(move,piece):

        # checking if move is en passant
        if (SF.will_move_be_a_capture(move) == Stockfish.Capture.EN_PASSANT):
            
            # e5f6 => source_square is e5, dest_square is f6
            source_square = move[0:2]
            dest_square = move[2:4]
            
            # if piece is white, then the square of the captured pawn is like so: e5f6 => f5 (numerically one lower)
            if piece[0] == "w":
                square_number = int(dest_square[1]) - 1
            
            # if piece is black, then the square of the captured pawn is like so: c4d3 => d4 (numerically one higher)
            else:
                square_number = int(dest_square[1]) + 1
            
            # calculating the square of the captured pawn
            pawn_captured_square = dest_square[0] + str(square_number)
            
            # updating the square value on true board 
            true_board_dict[pawn_captured_square] = ""
            
            # updating the sprite attached to this square
            for sq_sprite in square_group:
                if (sq_sprite.square == pawn_captured_square): sq_sprite.piece = ""  

    # check for checkmates / stalemates after every move. 
    def checkForMates():
        board = chess.Board(SF.get_fen_position())

        if board.is_checkmate() or board.is_stalemate():
            return board.outcome()
        else:
            return False

    # perform the player's move
    def doMoveIfValid(move,promotion_piece):
        nonlocal turn
        nonlocal game_state
        nonlocal highlight_sprite_1, highlight_sprite_2

        # if not promoting (which is most moves)
        if not promotion_piece: 
            
            # if it's a valid move
            if SF.is_move_correct(move):

                # what piece to move?
                moving_piece = source_sprite.piece

                # update piece movement in true board
                true_board_dict[move[0:2]] = ""
                true_board_dict[move[2:4]] = moving_piece

                # update piece movement amongst the sprites
                source_sprite.piece = ""
                dest_sprite.piece = moving_piece

                # highlight sprites to indicate most recent move
                unhighlightAllSprites()
                source_sprite.image.fill((255, 244, 143))
                dest_sprite.image.fill((255, 244, 143))

                # update castling rook movements (if any)
                castlingRookUpdate(move,moving_piece)
                    
                # updating en passant move (if any)
                enPassantUpdate(move,moving_piece)

                # make the move on stockfish
                SF.make_moves_from_current_position([move])
                print(SF.get_board_visual())

                # check for checkmate/stalemate
                if checkForMates():
                    game_state = "mate"

                # change turns
                turn = "WHITE" if turn == "BLACK" else "BLACK"
            
        # if promoting
        else:
            
            # if promotion piece is wR, stockfish suffix becomes 'r'. bQ becomes 'q'
            stockfish_suffix = promotion_piece[1].lower()

            # if move is correct
            if SF.is_move_correct(move+stockfish_suffix):

                # update promotion piece movement in true board
                true_board_dict[move[0:2]] = ""
                true_board_dict[move[2:4]] = promotion_piece

                # update promotion piece movement amongst the sprites
                source_sprite.piece = ""
                dest_sprite.piece = promotion_piece

                # highlight sprites to indicate most recent move
                unhighlightAllSprites()
                source_sprite.image.fill((255, 244, 143))
                dest_sprite.image.fill((255, 244, 143))

                # make the move on stockfish (first translate the move)
                SF.make_moves_from_current_position([move+stockfish_suffix])
                print(SF.get_board_visual())
                
                # check for checkmate/stalemate
                if checkForMates():
                    game_state = "mate"

                # change turns
                turn = "WHITE" if turn == "BLACK" else "BLACK"

                # game state: changes from "promotion" to "ongoing"
                game_state = "ongoing"

    # Main Loop
    while True: 
        
        # if computer's turn, do computer's move
        if (turn != player_colour):

            # gets computer move within "x" ms, where "x" is chosen randomly from 700-1000
            computer_move = SF.get_best_move_time(randint(1500,2000))
            
            # "e2e4" -> source_square becomes e2, dest_square becomes e4
            source_square = computer_move[0:2]
            dest_square = computer_move[2:4]

            # finding out which piece to move based on what squares the computer said
            piece_to_move = true_board_dict[source_square]

            # updating the sprites about the pieces attached to them 
            # AND highlight the source,dest sprites to indicate most recent piece movement
            unhighlightAllSprites()
            for sq_sprite in square_group:
                if sq_sprite.square == source_square: 
                    sq_sprite.piece = ""
                    sq_sprite.image.fill((255, 244, 143))
                if sq_sprite.square == dest_square: 
                    sq_sprite.piece = piece_to_move
                    sq_sprite.image.fill((255, 244, 143))


            # if it's a promotion move. e.g. e7e8q (where the length is 5, since the suffix q is present)
            # then update the true board in this unique way
            if len(computer_move) > 4:
                
                promotion_piece = turn[0].lower() + computer_move[-1].upper()

                # updating the promotion move in true board
                true_board_dict[source_square] = ""
                true_board_dict[dest_square] = promotion_piece

            # not a promotion move? update true board the normal way, check for castling/enPassant updates
            else:

                # updating the move in true board
                true_board_dict[source_square] = ""
                true_board_dict[dest_square] = piece_to_move

                # update castling rook movements (if any)
                castlingRookUpdate(computer_move,piece_to_move)
                
                # updating en passant move (if any)
                enPassantUpdate(computer_move,piece_to_move)

            # make the move on our stockfish instance
            SF.make_moves_from_current_position([computer_move])
            print(f"Computer move: {computer_move}")
            print(SF.get_board_visual())

            # check for checkmate/stalemate
            if checkForMates():
                game_state = "mate"

            # change turns
            turn = "WHITE" if turn == "BLACK" else "BLACK"

        # check for events
        for event in pygame.event.get():

            # QUIT event
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # MOUSE CLICK event, when the game is ongoing
            if game_state == "ongoing":

                # check for player input only on THEIR TURN
                if (turn == player_colour):

                    # MOUSE CLICK event (event.button -> 1 represents left mouse click)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                        # check all sprites to see if mouse pos inside its rect
                        for sq_sprite in square_group:

                            # is the mouse position, at the time of click, within this square sprite?
                            if sq_sprite.rect.collidepoint(event.pos):

                                # set source sprite once mouse clicked down
                                source_sprite = sq_sprite

                    # MOUSE UNCLICK event (event.button -> 1 represents left mouse click)
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:

                        # check all sprites to see if mouse pos inside its rect
                        for sq_sprite in square_group:

                            # is the mouse position, at the time of unclick, within this square sprite? AND there was a source sprite?
                            if sq_sprite.rect.collidepoint(event.pos) and source_sprite:
                                        
                                # put the move together
                                move = source_sprite.square + sq_sprite.square
                                        
                                # update destination sprite
                                dest_sprite = sq_sprite
                                                                
                                # Is the move a promotion move? If so, change game state, check for promotion input
                                # the below 2 are just temp variables helping to check for promotion
                                source_number = int(source_sprite.square[1])
                                dest_number = int(sq_sprite.square[1])
                                if (source_number == 7 and dest_number == 8 and source_sprite.piece == 'wP') or (source_number == 2 and dest_number == 1 and source_sprite.piece == 'bP'):
                                    game_state = "promotion"

                                # A normal move, you say? Proceed as per normal - perform move
                                else:
                                    # perform move, if valid
                                    doMoveIfValid(move,None)

                                    # reset move variables
                                    source_sprite = None
                                    dest_sprite = None

            # SPACE event to go to menu screen, when the game is checkmated/stalemated            
            elif game_state == "mate":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
                    MENU_MODE()

            # R,N,B,Q events to promote to rook, knight, bishop or queen, when a pawn is being promoted in game
            elif game_state == "promotion":

                # if ANY key pressed when in promotion mode
                if event.type == pygame.KEYDOWN:
                    
                    # getting move -> for determining move variable later on
                    move = source_sprite.square + dest_sprite.square

                    # getting colour of piece moved -> for determining promotion_piece variable later on
                    colour = source_sprite.piece[0]

                    # r pressed = rook
                    if event.key == pygame.K_r:
                        
                        # setting promotion piece -> e.g. wR, bR
                        promotion_piece = colour + 'R'

                        # perform promotion move, if valid
                        doMoveIfValid(move,promotion_piece)
                        
                        # reset move variables
                        source_sprite = None
                        dest_sprite = None
                   
                    # b pressed = bishop
                    elif event.key == pygame.K_b:
                        
                        # setting promotion piece -> e.g. wB, bB
                        promotion_piece = colour + 'B'

                        # perform promotion move, if valid
                        doMoveIfValid(move,promotion_piece)

                        # reset move variables
                        source_sprite = None
                        dest_sprite = None
                    
                    # n pressed = knight
                    elif event.key == pygame.K_n:
                        
                        # setting promotion piece -> e.g. wN, bN
                        promotion_piece = colour + 'N'

                        # perform promotion move, if valid
                        doMoveIfValid(move,promotion_piece)

                        # reset move variables
                        source_sprite = None
                        dest_sprite = None
                    
                    # q pressed = queen
                    elif event.key == pygame.K_q:
                                                
                        # setting promotion piece -> e.g. wQ, bQ
                        promotion_piece = colour + 'Q'

                        # perform promotion move, if valid
                        doMoveIfValid(move,promotion_piece)

                        # reset move variables
                        source_sprite = None
                        dest_sprite = None
                    
        # display chess board
        SCREEN.blit(board_surf,board_rect)

        # draw invisible squares
        square_group.draw(SCREEN)
      
        # based on true board dictionary, set the images of all pieces
        displayPiecesBasedOnTrueBoard()

        # When the game state is in "mate" (checkmate/stalemate),
        # display mate message, option to restart
        if game_state == "mate":
            
            # get outcome
            outcome = checkForMates()
            
            # if checkmate, then tell user it's checkmate, along with which colour won
            if outcome.termination == chess.Termination.CHECKMATE:
                colour = "White" if outcome.winner else "Black"
                msg_text = f"Checkmate! {colour} won."

            # if stalemate, then tell user it's stalemate
            elif outcome.termination == chess.Termination.STALEMATE:
                msg_text = f"Stalemate!"

            # show the message, whatever it is, on the screen    
            msg_surf = gilroyregular30.render(f"{msg_text} Press SPACE to go to main menu",True,'red','grey')
            msg_rect = msg_surf.get_rect(center=(400,400))
            SCREEN.blit(msg_surf,msg_rect)

        # When the game state is in "promotion",
        # display promotion message, options (R=Rook,N=Knight,B=Bishop,Q=Queen)
        elif game_state == "promotion":
            
            # show the message on the screen
            msg_surf = gilroyregular30.render("Promotion! Press r=rook, b=bishop, n=knight, q=queen.",True,'red','grey')
            msg_rect = msg_surf.get_rect(center=(400,400))
            SCREEN.blit(msg_surf,msg_rect)

        # update the whole screen every frame
        pygame.display.update()

        # set frame rate = 60 FPS
        CLOCK.tick_busy_loop(60)

# Initial Start
MENU_MODE()