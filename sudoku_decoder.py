import math

class SudokuDecoder:
    def __init__(self, file_name, game_size = 9):
        self.games = []
        self.game_size = game_size
        self.read_file_data(file_name)

    def read_file_data(self, file_name):
        file = open(file_name, "r")
        self.games = []

        # read every clause until we get 0, then go to the next line
        for line in file:
            current_game = []
            for char_position, char in enumerate(line):
                if char == '.':
                    continue
                
                row_position = math.floor(char_position / self.game_size) + 1
                column_position = (char_position % self.game_size) + 1
                new_rule = f'{row_position}{column_position}{char}'
                current_game.append(new_rule)
            
            self.games.append(current_game)

    def get_games(self):
        return self.games
                    
                    