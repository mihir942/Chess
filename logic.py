from stockfish import Stockfish
sf = Stockfish("C:/Users/mihir/Downloads/stockfish_15.1/stockfish.exe",depth=18,parameters={"Threads": 2, "Minimum Thinking Time": 30})


sf.set_fen_position("8/8/8/8/8/1Q6/2K5/k7 b - - 0 1")
print(sf.get_top_moves())

# print(sf.get_evaluation())

# print(sf.get_board_visual())

# sf.set_elo_rating(2500)


# while True:
#     x = input("your move? ")
#     if sf.is_move_correct(x):
#         sf.make_moves_from_current_position([x])
#         print(sf.get_what_is_on_square("d1"))
#         print(sf.get_board_visual())
#     else:
#         print("move invalid")
#         continue    

#     best_move = sf.get_best_move()
#     print(best_move)
#     sf.make_moves_from_current_position([best_move])
#     print(sf.get_board_visual())
    
#     print("Evaluation:",sf.get_evaluation())