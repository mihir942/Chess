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