from dataclasses import dataclass, field

@dataclass
class Coordinate:
    x: str
    y: int

class Board:
    def __init__(self):
        pass

    def generate_board(self):
        x = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        y = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        board = []
        for integer in y:
            row = []
            for letter in x:
                row.append(Coordinate(letter, integer))
            board.append(row)
        return board

    def add_ship(self, coordinate: Coordinate):
        pass

def main():
    board = Board()
    print(board.generate_board())

if __name__ == "__main__":
    main()
    