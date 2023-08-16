from game import TeekoPlayer
import random
def main():
    ai_c = 0
    opponent_c = 0
    for i in range(100):
        print('Hello, this is Samaritan')
        ai = TeekoPlayer()
        piece_count = 0
        turn = 0

        # drop phase
        while piece_count < 8 and ai.game_value(ai.board) == 0:

            # get the player or AI's move
            if ai.my_piece == ai.pieces[turn]:
                ai.print_board()
                move = ai.make_move(ai.board)
                ai.place_piece(move, ai.my_piece)
                print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
            else:
                move_made = False
                ai.print_board()
                print(ai.opp + "'s turn")

                move = []
                (row, col) = (random.randint(0, 4), random.randint(0, 4))
                while not ai.board[row][col] == ' ':
                    (row, col) = (random.randint(0, 4), random.randint(0, 4))

                # ensure the destination (row,col) tuple is at the beginning of the move list
                move.insert(0, (row, col))
                ai.opponent_move(move)
                move_made = True


            # update the game variables
            piece_count += 1
            turn += 1
            turn %= 2

        # move phase - can't have a winner until all 8 pieces are on the board
        while ai.game_value(ai.board) == 0:

            # get the player or AI's move
            if ai.my_piece == ai.pieces[turn]:
                ai.print_board()
                move = ai.make_move(ai.board)
                ai.place_piece(move, ai.my_piece)
                print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
                print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
            else:
                move_made = False
                ai.print_board()
                print(ai.opp + "'s turn")
                while not move_made:
                    move = []

                    (row, col) = (random.randint(0, 4), random.randint(0, 4))
                    while not ai.board[row][col] == ai.opp:
                        (row, col) = (random.randint(0, 4), random.randint(0, 4))

                    succ = ai.succ(ai.board, ai.opp)
                    for i in range(len(succ)):
                        if succ[i][row][col] == ' ':
                            if row - 1 >= 0 and succ[i][row - 1][col] == ai.opp and ai.board[row - 1][col] == ' ':
                                move.append((row - 1, col))
                                break
                            elif row + 1 <= 4 and succ[i][row + 1][col] == ai.opp and ai.board[row + 1][col] == ' ':
                                move.append((row + 1, col))
                                break
                            elif col - 1 >= 0 and succ[i][row][col - 1] == ai.opp and ai.board[row][col - 1] == ' ':
                                move.append((row, col - 1))
                                break
                            elif col + 1 <= 4 and succ[i][row][col + 1] == ai.opp and ai.board[row][col + 1] == ' ':
                                move.append((row, col + 1))
                                break
                            elif row - 1 >= 0 and col - 1 >= 0 and succ[i][row - 1][col - 1] == ai.opp and \
                                    ai.board[row - 1][col - 1] == ' ':
                                move.append((row - 1, col - 1))
                                break
                            elif row + 1 <= 4 and col - 1 >= 0 and succ[i][row + 1][col - 1] == ai.opp and \
                                    ai.board[row + 1][col - 1] == ' ':
                                move.append((row + 1, col - 1))
                                break
                            elif row - 1 >= 0 and col + 1 <= 4 and succ[i][row - 1][col + 1] == ai.opp and \
                                    ai.board[row - 1][col + 1] == ' ':
                                move.append((row - 1, col + 1))
                                break
                            elif row + 1 <= 4 and col + 1 <= 4 and succ[i][row + 1][col + 1] == ai.opp and \
                                    ai.board[row + 1][col + 1] == ' ':
                                move.append((row + 1, col + 1))
                                break

                    move.append((row, col))
                    ai.opponent_move(move)
                    move_made = True

            # update the game variables
            turn += 1
            turn %= 2

        ai.print_board()
        if ai.game_value(ai.board) == 1:
            print("AI wins! Game over.")
            ai_c+=1
        else:
            print("You win! Game over.")


    print(f'Percentage of AI wins: {(ai_c/(ai_c + opponent_c) * 100)}%')



if __name__ == "__main__":

    main()