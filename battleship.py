from dataclasses import dataclass, field
from enum import Enum

@dataclass(frozen=True)
class Coordinate:
    x: str
    y: int

class ShipType(Enum):
    PLANE_CARRIER = 5
    BATTLESHIP = 4
    CRUISER = 3
    SUBMARINE = 3
    DESTROYER = 2

class Direction(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

class Board:
    def __init__(self):
        self.board_coordinates = self.generate_coordinatee_board()
        self.ship_locations = {}

    def generate_coordinatee_board(self):
        x = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        board = []
        for integer in y:
            row = []
            for letter in x:
                row.append(Coordinate(letter, integer))
            board.append(row)
        return board
    
    def print_board(self):
        print("    A  B  C  D  E  F  G  H  I  J")
        row_number = 1
        for row in self.board_coordinates:
            if row_number < 10:
                print(f"{row_number}  ", end="")
            else:
                print(f"{row_number} ", end="")
            for coordinate in row:
                try:
                    for ship in self.ship_locations:
                        if coordinate in self.ship_locations[ship]:
                            print(f"[{ship.name[0]}]", end="")
                            ship_found = True
                            break
                        else:
                            ship_found = False
                    if not ship_found:
                        print("[ ]", end="")
                except Exception as e:
                    print(e)
            print("\n")
            row_number += 1

    def add_ship(self, ship_type: ShipType, direction: Direction, start_coordinate: str) -> None:
        ship_length = ship_type.value
        x = start_coordinate[0]
        y = int(start_coordinate[1])
        if direction == Direction.HORIZONTAL:
            ship_coordinates = []
            for i in range(ship_length):
                x_integer = self.get_x_integer_from_letter(x)
                x_integer += i
                x_letter = self.get_letter_from_x_integer(x_integer)
                ship_coordinates.append(Coordinate(x_letter, y))
            self.ship_locations[ship_type] = ship_coordinates
        else:
            ship_coordinates = []
            for i in range(ship_length):
                ship_coordinates.append(Coordinate(x, y + i))
            self.ship_locations[ship_type] = ship_coordinates
    
    def get_x_integer_from_letter(self, letter: str) -> int:
        if letter == "A":
            return 1
        elif letter == "B":
            return 2
        elif letter == "C":
            return 3
        elif letter == "D":
            return 4
        elif letter == "E":
            return 5
        elif letter == "F":
            return 6
        elif letter == "G":
            return 7
        elif letter == "H":
            return 8
        elif letter == "I":
            return 9
        elif letter == "J":
            return 10
        else:
            print("Invalid letter")
            return 0
    
    def get_letter_from_x_integer(self, x: int) -> str:
        if x == 1:
            return "A"
        elif x == 2:
            return "B"
        elif x == 3:
            return "C"
        elif x == 4:
            return "D"
        elif x == 5:
            return "E"
        elif x == 6:
            return "F"
        elif x == 7:
            return "G"
        elif x == 8:
            return "H"
        elif x == 9:
            return "I"
        elif x == 10:
            return "J"
        else:
            print("Invalid integer")
            return "Z"

def main():
    board = Board()
    board.add_ship(ShipType.PLANE_CARRIER, Direction.HORIZONTAL, "A1")
    board.add_ship(ShipType.BATTLESHIP, Direction.VERTICAL, "B2")
    board.add_ship(ShipType.CRUISER, Direction.HORIZONTAL, "D4")
    print(board.print_board())

if __name__ == "__main__":
    main()
    