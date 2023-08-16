import random


class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]


    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        drop_phase = True  # TODO: detect drop phase
        counter = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (self.board[i][j] != ' '):
                    counter += 1
        if (counter>=8):
            drop_phase = False

        move = []
        old = (0,0)
        new = (0,0)
        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            value, next_st = self.max_value(state, 0)
            for i in range(5):
                for j in range(5):
                    # source row and column
                    if (state[i][j] == ' ' and next_st[i][j] == self.my_piece):
                        new = (i, j)
                    # destination row and column
                    if (state[i][j] == self.my_piece and next_st[i][j] == ' '):
                        old = (i, j)
            move.append(new)
            move.append(old)
            return move

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        value, next_st = self.max_value(state, 0)
        for i in range(5):
                for j in range(5):
                    # source row and column
                    if (state[i][j] == ' ' and next_st[i][j] == self.my_piece):
                        new = (i, j)
        # ensure the destination (row,col) tuple is at the beginning of the move list
        move.insert(0, new)
        return move


    def succ(self, state):
        """ Gets all valid successors to a state

        Args:
        self: the player
        state (list of lists): the current state of the game
        drop_phase (boolean): drop phase or not

        Returns:
            list: of all legal successors

        """
        succ_states = []
        pieces = []
        oppo_pieces = []
        drop_phase = True
        for i in range(len(state)):
            for j in range(len(state[i])):
                if (state[i][j] == self.my_piece):
                    pieces.append((i, j))
                if (state[i][j] == self.opp):
                    oppo_pieces.append((i, j))
        if len(pieces) >= 4 and len(oppo_pieces) >= 4:
            drop_phase = False

        new_copy = [row[:] for row in state]
        # move to adjacent
        if not drop_phase:
            for p in pieces:
                x = p[0]
                y = p[1]
                # move vertical
                if (x-1>=0 and state[x-1][y]==' '):
                    new_copy[x-1][y] = new_copy[x][y]
                    new_copy[x][y] = ' '
                    succ_states.append(new_copy)
                    new_copy = [row[:] for row in state]
                if (x+1<5 and state[x+1][y]==' '):
                    new_copy[x+1][y] = new_copy[x][y]
                    new_copy[x][y] = ' '
                    succ_states.append(new_copy)
                    new_copy = [row[:] for row in state]
                # move horizontal
                if (y-1>=0 and state[x][y-1]==' '):
                    new_copy[x][y-1] = new_copy[x][y]
                    new_copy[x][y] = ' '
                    succ_states.append(new_copy)
                    new_copy = [row[:] for row in state]
                if (y+1<5 and state[x][y+1]==' '):
                    new_copy[x][y+1] = new_copy[x][y]
                    new_copy[x][y] = ' '
                    succ_states.append(new_copy)
                    new_copy = [row[:] for row in state]
                # move diagonal
                if (x-1>=0 and y-1>=0 and state[x-1][y-1]==' '):
                    new_copy[x-1][y-1] = new_copy[x][y]
                    new_copy[x][y] = ' '
                    succ_states.append(new_copy)
                    new_copy = [row[:] for row in state]
                if (x+1<5 and y+1<5 and state[x+1][y+1]==' '):
                    new_copy[x+1][y+1] = new_copy[x][y]
                    new_copy[x][y] = ' '
                    succ_states.append(new_copy)
                    new_copy = [row[:] for row in state]
                if (x-1>=0 and y+1<5 and state[x-1][y+1]==' '):
                    new_copy[x-1][y+1] = new_copy[x][y]
                    new_copy[x][y] = ' '
                    succ_states.append(new_copy)
                    new_copy = [row[:] for row in state]
                if (x+1<5 and y-1>=0 and state[x+1][y-1]==' '):
                    new_copy[x+1][y-1] = new_copy[x][y]
                    new_copy[x][y] = ' '
                    succ_states.append(new_copy)
                    new_copy = [row[:] for row in state]
            random.shuffle(succ_states)
            return succ_states

        # not in drop phase, so place a new piece in every open space
        # will calculate heuristic of each later
        for i in range(5):
            for j in range(5):
                if state[i][j] == ' ':
                    new_copy[i][j] = self.my_piece
                    succ_states.append(new_copy)
                    new_copy = [row[:] for row in state]

        random.shuffle(succ_states)
        return succ_states

    def heuristic_game_value_back(self, state):
        """ Evaluates a given successor based on how close it is to the terminal state

        Args:
        self: the player 
        state (list): successor to evaluate

        Returns:
            float: heuristic value

        """
        if self.game_value(state) != 0:
            return self.game_value(state)
        '''
        values = [[0,1,0,1,0],
                  [1,2,2,2,1],
                  [0,2,3,2,0],
                  [1,2,2,2,1],
                  [0,1,0,1,0]]
        
        value = [[1,2,1,2,1],
                  [2,3,3,3,2],
                  [1,3,4,3,1],
                  [2,3,3,3,2],
                  [1,2,1,2,1]]
        '''
        my_count = 0
        oppo_count = 0
        my_max = 0
        oppo_max = 0

        # check horizontal wins
        for row in range(5):
            for i in range(5):
                if state[row][i] == self.opp:
                    oppo_count += 1
                if state[row][i] == self.my_piece:
                    my_count += 1
            
            if oppo_count > 2 and my_count > 0: # if there are 2 or more opponent pieces in that row
                my_count += oppo_count*2
            if my_count > my_max:
                my_max = my_count
            my_count = 0
            if oppo_count > oppo_max:
                oppo_max = oppo_count
            oppo_count = 0  

         # check vertical wins
        for col in range(5):
            for i in range(5):
                if state[i][col] == self.opp:
                    oppo_count += 1
                if state[i][col] == self.my_piece:
                    my_count += 1
            
            if oppo_count > 2 and my_count > 0: # if there are 2 or more opponent pieces in that row
                my_count += oppo_count*2
            if my_count > my_max:
                my_max = my_count
            my_count = 0
            if oppo_count > oppo_max:
                oppo_max = oppo_count
            oppo_count = 0

        # check \ diagonal wins
        for i in range(2):
            for col in range(2):
                if state[i][col] == self.opp:
                    oppo_count += 1
                if state[i+1][col+1] == self.opp:
                    oppo_count += 1
                if state[i+2][col+2] == self.opp:
                    oppo_count += 1
                if state[i+3][col+3] == self.opp:
                    oppo_count += 1

                if state[i][col] == self.my_piece:
                    my_count += 1
                if state[i+1][col+1] == self.my_piece:
                    my_count += 1
                if state[i+2][col+2] == self.my_piece:
                    my_count += 1
                if state[i+3][col+3] == self.my_piece:
                    my_count += 1

                if oppo_count > 2 and my_count > 0: # if there are 2 or more opponent pieces in that row
                    my_count += oppo_count*2
                if my_count > my_max:
                    my_max = my_count
                my_count = 0
                if oppo_count > oppo_max:
                    oppo_max = oppo_count
                oppo_count = 0  

        # check / diagonal wins
        for i in range(2):
            for col in range(3, 5):
                if state[i][col] == self.opp:
                    oppo_count += 1
                if state[i+1][col-1] == self.opp:
                    oppo_count += 1
                if state[i+2][col-2] == self.opp:
                    oppo_count += 1
                if state[i+3][col-3] == self.opp:
                    oppo_count += 1

                if state[i][col] == self.my_piece:
                    my_count += 1
                if state[i+1][col-1] == self.my_piece:
                    my_count += 1
                if state[i+2][col-2] == self.my_piece:
                    my_count += 1
                if state[i+3][col-3] == self.my_piece:
                    my_count += 1

                if oppo_count > 2 and my_count > 0: # if there are 2 or more opponent pieces in that row
                    my_count += oppo_count*2
                if my_count > my_max:
                    my_max = my_count
                my_count = 0
                if oppo_count > oppo_max:
                    oppo_max = oppo_count
                oppo_count = 0 

        # check box wins
        for i in range(4):
            for col in range(4):
                if state[i][col] == self.opp:
                    oppo_count += 1
                if state[i][col+1] == self.opp:
                    oppo_count += 1
                if state[i+1][col] == self.opp:
                    oppo_count += 1
                if state[i+1][col+1] == self.opp:
                    oppo_count += 1

                if state[i][col] == self.my_piece:
                    my_count += 1
                if state[i][col+1] == self.my_piece:
                    my_count += 1
                if state[i+1][col] == self.my_piece:
                    my_count += 1
                if state[i+1][col+1] == self.my_piece:
                    my_count += 1
                
                if oppo_count > 2 and my_count > 0: # if there are 2 or more opponent pieces in that row
                    my_count += oppo_count*2
                if my_count > my_max:
                    my_max = my_count
                my_count = 0
                if oppo_count > oppo_max:
                    oppo_max = oppo_count
                oppo_count = 0 
        
        if (my_max == oppo_max):
            return 0 # middle value
        elif (my_max < oppo_max):
            return (-1) * (oppo_max/12)
        
        return (my_max)/12


    def heuristic_game_value(self, state):
        """ Evaluates a given successor based on how close it is to the terminal state

        Args:
        self: the player 
        state (list): successor to evaluate

        Returns:
            float: heuristic value

        """
        if self.game_value(state) != 0:
            return self.game_value(state)
        '''
        values = [[0,1,0,1,0],
                  [1,2,2,2,1],
                  [0,2,3,2,0],
                  [1,2,2,2,1],
                  [0,1,0,1,0]]
        '''
        value = [[1,2,1,2,1],
                  [2,3,3,3,2],
                  [1,3,4,3,1],
                  [2,3,3,3,2],
                  [1,2,1,2,1]]
        
        my_count = 0
        oppo_count = 0
        my_max = 0
        oppo_max = 0

        block = []

        # check horizontal wins
        for row in range(5):
            for i in range(5):
                if state[row][i] == self.opp:
                    oppo_count += value[row][i]
                if state[row][i] == self.my_piece:
                    my_count += value[row][i]
            
            if oppo_count > 3 and my_count > 0: # if there are 2 or more opponent pieces in that row
                my_count *= 3
                block.append(my_count)
            my_max = max(my_count, my_max)
            my_count = 0
            oppo_max = max(oppo_count, oppo_max)
            oppo_count = 0  

         # check vertical wins
        for col in range(5):
            for i in range(5):
                if state[i][col] == self.opp:
                    oppo_count += value[i][col]
                if state[i][col] == self.my_piece:
                    my_count += value[i][col]
            
            if oppo_count > 3 and my_count > 0: # if there are 2 or more opponent pieces in that row
                my_count *= 3
                block.append(my_count)
            imy_max = max(my_count, my_max)
            my_count = 0
            oppo_max = max(oppo_count, oppo_max)
            oppo_count = 0  

        # check \ diagonal wins
        for i in range(2):
            for col in range(2):
                if state[i][col] == self.opp:
                    oppo_count += value[i][col]
                if state[i+1][col+1] == self.opp:
                    oppo_count += value[i+1][col+1]
                if state[i+2][col+2] == self.opp:
                    oppo_count += value[i+2][col+2]
                if state[i+3][col+3] == self.opp:
                    oppo_count += value[i+3][col+3]

                if state[i][col] == self.my_piece:
                    my_count += value[i][col]
                if state[i+1][col+1] == self.my_piece:
                    my_count += value[i+1][col+1]
                if state[i+2][col+2] == self.my_piece:
                    my_count += value[i+2][col+2]
                if state[i+3][col+3] == self.my_piece:
                    my_count += value[i+3][col+3]

                if oppo_count > 3 and my_count > 0: # if there are 2 or more opponent pieces in that row
                    my_count *= 3
                    block.append(my_count)
                my_max = max(my_count, my_max)
                my_count = 0
                oppo_max = max(oppo_count, oppo_max)
                oppo_count = 0   

        # check / diagonal wins
        for i in range(2):
            for col in range(3, 5):
                if state[i][col] == self.opp:
                    oppo_count += value[i][col]
                if state[i+1][col-1] == self.opp:
                    oppo_count += value[i+1][col-1]
                if state[i+2][col-2] == self.opp:
                    oppo_count += value[i+2][col-2]
                if state[i+3][col-3] == self.opp:
                    oppo_count += value[i+3][col-3]

                if state[i][col] == self.my_piece:
                    my_count += value[i][col]
                if state[i+1][col-1] == self.my_piece:
                    my_count += value[i+1][col-1]
                if state[i+2][col-2] == self.my_piece:
                    my_count += value[i+2][col-2]
                if state[i+3][col-3] == self.my_piece:
                    my_count += value[i+3][col-3]

                if oppo_count > 3 and my_count > 0: # if there are 2 or more opponent pieces in that row
                    my_count *= 3
                    block.append(my_count)
                my_max = max(my_count, my_max)
                my_count = 0
                oppo_max = max(oppo_count, oppo_max)
                oppo_count = 0  

        # check box wins
        for i in range(4):
            for col in range(4):
                if state[i][col] == self.opp:
                    oppo_count += value[i][col]
                if state[i][col+1] == self.opp:
                    oppo_count += value[i][col+1]
                if state[i+1][col] == self.opp:
                    oppo_count += value[i+1][col]
                if state[i+1][col+1] == self.opp:
                    oppo_count += value[i+1][col+1]

                if state[i][col] == self.my_piece:
                    my_count += value[i][col]
                if state[i][col+1] == self.my_piece:
                    my_count += value[i][col+1]
                if state[i+1][col] == self.my_piece:
                    my_count += value[i+1][col]
                if state[i+1][col+1] == self.my_piece:
                    my_count += value[i+1][col+1]
                
                if oppo_count > 3 and my_count > 0: # if there are 2 or more opponent pieces in that row
                    my_count *= 3
                    block.append(my_count)
                my_max = max(my_count, my_max)
                my_count = 0
                oppo_max = max(oppo_count, oppo_max)
                oppo_count = 0  
        
        if (len(block) > 0):
            return max(block)
        if (my_max == oppo_max):
            return 0 # middle value
        elif (my_max < oppo_max):
            return (-1) * (oppo_max/100)
        
        return (my_max)/100


    def max_value(self, state, depth):
        """ recursive function to choose the max value state

        Args:
        self: the player
        state (list): current state of the board
        depth: how far into the tree the recursive function is

        Returns:
            list: the next state

        """
        # base case 
        # base case
        if self.game_value(state) != 0:
            return self.game_value(state), state

        if depth >= 3:
            return self.heuristic_game_value(state), state

        else:
            a = float('-inf')
            next_state = state
            for s in self.succ(state):
                store = self.min_value(s, depth+1)
                if a < store[0]:
                    a = store[0]
                    next_state = s

        return a, next_state


    def min_value(self, state, depth):
        """ recursive function to choose the min value state

        Args:
        self: the player
        state (list): current state of the board
        depth: how far into the tree the recursive function is

        Returns:
            list: the next state

        """
        # base case
        if self.game_value(state) != 0:
            return self.game_value(state), state

        if depth >= 3:
            return self.heuristic_game_value(state), state

        else:
            b = float('inf')
            next_state = state
            for s in self.succ(state):
                store = self.max_value(s, depth+1)
                if b > store[0]:
                    b = store[0]
                    next_state = s

        return b, next_state



    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)


    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece


    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")


    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # TODO: check \ diagonal wins
        for i in range(2):
            for col in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col+1] == state[i+2][col+2] == state[i+3][col+3]:
                    return 1 if state[i][col] == self.my_piece else -1

        # TODO: check / diagonal wins
        for i in range(2):
            for col in range(3, 5):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col-1] == state[i+2][col-2] == state[i+3][col-3]:
                    return 1 if state[i][col] == self.my_piece else -1

        # TODO: check box wins
        for i in range(4):
            for col in range(4):
                if (state[i][col] != ' ' and state[i][col] == state[i][col+1] == state[i+1][col] == state[i+1][col+1]):
                        return 1 if state[i][col] == self.my_piece else -1

        return 0  # no winner yet


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
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
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

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
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                      (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
