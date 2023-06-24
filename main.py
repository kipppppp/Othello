
# Author: Kyle Gonzales
# GitHub username: kipppppp

import os       # Only used to clear screen for Windows terminal
import random   # Used for AI move generation


class Othello:
    """Represents a game of Othello. Includes a 8x8 board and current dict of players. This class utilizes objects
    of the player class to create a player dictionary which takes the form {Symbol: Player object}"""
    def __init__(self):
        self._player_dict = {}
        self._header = "    1 2 3 4 5 6 7 8  "
        self._board = [['  -', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                        ['|', '+', '+', '+', '+', '+', '+', '+', '+', '|'],
                        ['|', '+', '+', '+', '+', '+', '+', '+', '+', '|'],
                        ['|', '+', '+', '+', '+', '+', '+', '+', '+', '|'],
                        ['|', '+', '+', '+', 'O', 'X', '+', '+', '+', '|'],
                        ['|', '+', '+', '+', 'X', 'O', '+', '+', '+', '|'],
                        ['|', '+', '+', '+', '+', '+', '+', '+', '+', '|'],
                        ['|', '+', '+', '+', '+', '+', '+', '+', '+', '|'],
                        ['|', '+', '+', '+', '+', '+', '+', '+', '+', '|'],
                        ['  -', '-', '-', '-', '-', '-', '-', '-', '-', '-']]

    def print_board(self):
        """Prints the current board, including player tokens"""
        row_counter = 0
        print(self._header)
        for row in self._board:
            if 0 < row_counter <= 8:
                print(str(row_counter) + ' ', end='')
            for col in row:
                print(col + ' ', end='')
            row_counter += 1
            print('')

    def add_player(self, name, symbol, flag=False):
        """Creates a player object and adds it to the player dictionary"""
        self._player_dict[symbol.upper()] = Player(name, symbol.upper(), flag)

    def get_player(self, symbol):
        """Returns a player object given a symbol"""
        return self._player_dict[symbol.upper()]

    def make_move(self, player_object, row_col):
        """Uses a player object and coordinates (as tuple) to place the appropriate token"""
        self._board[row_col[0]][row_col[1]] = player_object.get_symbol()

    def check_game_over(self):
        """Updates both player object's list of available moves. If no moves exist, the game is over"""
        self.get_player_positions('X')
        self.find_valid_moves('X')

        self.get_player_positions('O')
        self.find_valid_moves('O')

        if not self._player_dict['X'].get_moves_list() and not self._player_dict['O'].get_moves_list():
            os.system('cls')
            print("Game over! Total points below")
            self.print_board()
            p1 = self._player_dict['X']
            p2 = self._player_dict['O']
            print("X:", p1.get_points())
            print("O:", p2.get_points())

            if p1.get_points() == p2.get_points():
                print("Tie game!")
            elif p1.get_points() > p2.get_points():
                print(p1.get_name(), "(" + p1.get_symbol() + ") is the winner!")
            else:
                print(p2.get_name(), "(" + p2.get_symbol() + ") is the winner!")
            print('')
            print("Thanks for playing (:")
            exit()

    def get_player_positions(self, symbol):
        """Updates a player object's list of current token locations"""
        position_list = []
        row_counter = 0
        sym = symbol.upper()
        for row in self._board:
            col_counter = 0
            for col in row:
                if col == sym:
                    position_list.append((row_counter, col_counter))    # Store tile position
                col_counter += 1
            row_counter += 1

        self._player_dict[symbol.upper()].set_token_locations_and_points(position_list)     # Update player object list

    def find_valid_moves(self, symbol):
        """Updates a player object's valid move list"""
        player_object = self._player_dict[symbol.upper()]
        token_positions = player_object.get_token_locations()
        valid_moves_list = []

        if symbol.upper() == 'X':
            opp_symbol = 'O'
        else:
            opp_symbol = 'X'

        for pos in token_positions:
            # Vertical axis
            valid_moves_list.append(self.check_vertical_axis_up(pos, symbol, opp_symbol))
            valid_moves_list.append(self.check_vertical_axis_down(pos, symbol, opp_symbol))

            # Horizontal axis
            valid_moves_list.append(self.check_horizontal_axis_left(pos, symbol, opp_symbol))
            valid_moves_list.append(self.check_horizontal_axis_right(pos, symbol, opp_symbol))

            # Diagonal axis 1
            valid_moves_list.append(self.check_diagonal_axis_up_left(pos, symbol, opp_symbol))
            valid_moves_list.append(self.check_diagonal_axis_down_right(pos, symbol, opp_symbol))

            # Diagonal axis 2
            valid_moves_list.append(self.check_diagonal_axis_down_left(pos, symbol, opp_symbol))
            valid_moves_list.append(self.check_diagonal_axis_up_right(pos, symbol, opp_symbol))

        # Use set conversion to remove duplicate coordinates
        valid_moves_list = set(valid_moves_list)
        # Filter out None value if present
        valid_moves_list = list(filter(lambda item: item is not None, valid_moves_list))
        valid_moves_list.sort()

        player_object.set_moves_list(valid_moves_list)  # Update player object list of available moves

    def flip_tiles(self, symbol, pos):
        """Flips all appropriate tiles when a move is made"""
        if symbol.upper() == 'X':
            opp_symbol = 'O'
        else:
            opp_symbol = 'X'

        # Vertical axis
        self.check_vertical_axis_up(pos, symbol, opp_symbol, True)
        self.check_vertical_axis_down(pos, symbol, opp_symbol, True)

        # Horizontal axis
        self.check_horizontal_axis_left(pos, symbol, opp_symbol, True)
        self.check_horizontal_axis_right(pos, symbol, opp_symbol, True)

        # Diagonal axis 1
        self.check_diagonal_axis_up_left(pos, symbol, opp_symbol, True)
        self.check_diagonal_axis_down_right(pos, symbol, opp_symbol, True)

        # Diagonal axis 2
        self.check_diagonal_axis_down_left(pos, symbol, opp_symbol, True)
        self.check_diagonal_axis_up_right(pos, symbol, opp_symbol, True)

        for symbol in self._player_dict:
            self.get_player_positions(symbol)

    def check_vertical_axis_up(self, pos, symbol, opp_symbol, flip=False):
        """Checks for valid move upward. Returns tuple"""
        row = pos[0] - 1
        col = pos[1]
        while self._board[row][col] == opp_symbol:
            row -= 1
            if self._board[row][col] == '+' and not flip:
                return row, col
            if self._board[row][col] == symbol and flip:
                row += 1
                while self._board[row][col] == opp_symbol:
                    self._board[row][col] = symbol
                    row += 1

    def check_vertical_axis_down(self, pos, symbol, opp_symbol, flip=False):
        """Checks for valid move downward. Returns tuple"""
        row = pos[0] + 1
        col = pos[1]
        while self._board[row][col] == opp_symbol:
            row += 1
            if self._board[row][col] == '+' and not flip:
                return row, col
            if self._board[row][col] == symbol and flip:
                row -= 1
                while self._board[row][col] == opp_symbol:
                    self._board[row][col] = symbol
                    row -= 1

    def check_horizontal_axis_left(self, pos, symbol, opp_symbol, flip=False):
        """Checks for valid move left. Returns tuple"""
        row = pos[0]
        col = pos[1] - 1
        while self._board[row][col] == opp_symbol:
            col -= 1
            if self._board[row][col] == '+' and not flip:
                return row, col
            if self._board[row][col] == symbol and flip:
                col += 1
                while self._board[row][col] == opp_symbol:
                    self._board[row][col] = symbol
                    col += 1

    def check_horizontal_axis_right(self, pos, symbol, opp_symbol, flip=False):
        """Checks for valid move right. Returns tuple"""
        row = pos[0]
        col = pos[1] + 1
        while self._board[row][col] == opp_symbol:
            col += 1
            if self._board[row][col] == '+' and not flip:
                return row, col
            if self._board[row][col] == symbol and flip:
                col -= 1
                while self._board[row][col] == opp_symbol:
                    self._board[row][col] = symbol
                    col -= 1

    def check_diagonal_axis_up_left(self, pos, symbol, opp_symbol, flip=False):
        """Checks for valid move up-left. Returns tuple"""
        row = pos[0] - 1
        col = pos[1] - 1
        while self._board[row][col] == opp_symbol:
            row -= 1
            col -= 1
            if self._board[row][col] == '+' and not flip:
                return row, col
            if self._board[row][col] == symbol and flip:
                row += 1
                col += 1
                while self._board[row][col] == opp_symbol:
                    self._board[row][col] = symbol
                    row += 1
                    col += 1

    def check_diagonal_axis_down_right(self, pos, symbol, opp_symbol, flip=False):
        """Checks for valid move down-right. Returns tuple"""
        row = pos[0] + 1
        col = pos[1] + 1
        while self._board[row][col] == opp_symbol:
            row += 1
            col += 1
            if self._board[row][col] == '+' and not flip:
                return row, col
            if self._board[row][col] == symbol and flip:
                row -= 1
                col -= 1
                while self._board[row][col] == opp_symbol:
                    self._board[row][col] = symbol
                    row -= 1
                    col -= 1

    def check_diagonal_axis_down_left(self, pos, symbol, opp_symbol, flip=False):
        """Checks for valid move down-left. Returns tuple"""
        row = pos[0] + 1
        col = pos[1] - 1
        while self._board[row][col] == opp_symbol:
            row += 1
            col -= 1
            if self._board[row][col] == '+' and not flip:
                return row, col
            if self._board[row][col] == symbol and flip:
                row -= 1
                col += 1
                while self._board[row][col] == opp_symbol:
                    self._board[row][col] = symbol
                    row -= 1
                    col += 1

    def check_diagonal_axis_up_right(self, pos, symbol, opp_symbol, flip=False):
        """Checks for valid move up-right. Returns tuple"""
        row = pos[0] - 1
        col = pos[1] + 1
        while self._board[row][col] == opp_symbol:
            row -= 1
            col += 1
            if self._board[row][col] == '+' and not flip:
                return row, col
            if self._board[row][col] == symbol and flip:
                row += 1
                col -= 1
                while self._board[row][col] == opp_symbol:
                    self._board[row][col] = symbol
                    row += 1
                    col -= 1


class Player:
    """Represents a player with a name and symbol (X or O). This class is used to store player information"""
    def __init__(self, name, symbol, flag=False):
        self._name = name
        self._symbol = symbol.upper()
        self._token_locations = []
        self._moves_list = []
        self._points = 0
        self._ai_flag = flag

    def get_name(self):
        """Return player name as string"""
        return self._name

    def get_symbol(self):
        """Return player symbol as string"""
        return self._symbol

    def get_moves_list(self):
        """Return player moves as list of tuples"""
        return self._moves_list

    def get_points(self):
        """Return player points as int"""
        return self._points

    def get_token_locations(self):
        """Returns token coordinates as list"""
        return self._token_locations

    def set_token_locations_and_points(self, token_locations_list):
        """Updates list of player token locations and updates point value"""
        self._token_locations = token_locations_list
        self._points = len(self._token_locations)

    def set_moves_list(self, list_of_moves):
        """Updates list of available moves"""
        self._moves_list = list_of_moves

    def get_ai_status(self):
        """Returns boolean value of ai_flag"""
        return self._ai_flag


def player_initialization():
    """Determines number of players and initializes player objects via user input"""
    player1_name = input("Player 1(X), please enter your name: ")
    if player1_name == '0':
        game_board.add_player("AI", 'X', True)
    else:
        game_board.add_player(player1_name, 'X')

    player2_name = input("Player 2(O), please enter your name: ")
    if player2_name == '0':
        game_board.add_player("AI", 'O', True)
    else:
        game_board.add_player(player2_name, 'O')


def change_players(symbol):
    """Alternates current player"""
    if symbol == 'X':
        return 'O'
    else:
        return 'X'


# Introduction
print("Welcome to Othello with Kyle!")
print("This version supports 2 players, 1 player vs AI, or AI vs. AI.\nEnter 0 as player name to assign AI. Enter exit to quit")
print("X always moves first. Good luck!")

# Initialize game board and players
game_board = Othello()
player_initialization()

os.system('cls')

# Gameplay loop
current_player = 'X'
while True:
    # Check game end condition and update board state for both players
    game_board.check_game_over()

    # If the current player has no available moves their turn is forfeited
    if not game_board.get_player(current_player).get_moves_list():
        # Change players
        print(game_board.get_player(current_player).get_name(), "had no valid moves. Their turn is forfeited.")
        current_player = change_players(current_player)

    # Announce current player, show score, and display the current game board
    print(game_board.get_player(current_player).get_name(), "(" + game_board.get_player(current_player).get_symbol() + "), it's your turn.")
    print("X:", game_board.get_player('X').get_points())
    print("O:", game_board.get_player('O').get_points())
    game_board.print_board()

    # Get available moves list for current player
    moves = game_board.get_player(current_player).get_moves_list()

    # AI move generation
    if game_board.get_player(current_player).get_ai_status():
        ai_move = random.choice(moves)
        game_board.make_move(game_board.get_player(current_player), ai_move)
        game_board.flip_tiles(current_player, ai_move)
        print("AI placed a token at:", ai_move)
        print('')

        # Change players
        current_player = change_players(current_player)
        continue

    # Move validation loop
    valid_move = False
    while not valid_move:
        raw_move = input("Enter move as row,column (? to see a list of moves): ")
        if raw_move.lower() == "exit":
            print("Thanks for playing!")
            exit()
        elif raw_move == '?':
            print(moves)
            continue
        elif len(raw_move) != 3 or raw_move[1] != ',':
            print("Invalid input format. Please enter a valid move.")
            continue
        else:
            desired_row = int(raw_move[0])
            desired_col = int(raw_move[2])
            desired_move = desired_row, desired_col

            # Check if desired move is available
            if desired_move in moves:
                valid_move = True
            else:
                print("Invalid move. Please enter a valid move.")
                continue

        # Make valid move
        if valid_move:
            game_board.make_move(game_board.get_player(current_player), desired_move)
            game_board.flip_tiles(current_player, desired_move)

    # Change players
    current_player = change_players(current_player)

    os.system('cls')
