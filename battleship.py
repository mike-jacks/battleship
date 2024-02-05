from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple
import os
from time import sleep

@dataclass(frozen=True)
class Coordinate:
    x: str
    y: int
     
class TextColor(Enum):
    RED = "\033[91m"
    WHITE = "\033[97m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    DEFAULT = "\033[0m"
class ShipType(Enum):
    PLANE_CARRIER = {'plane_carrier':5}
    BATTLESHIP = {'battleship':4}
    CRUISER =  {'cruiser':3}
    SUBMARINE = {'submarine':3}
    DESTROYER = {'destroyer':2}
    NULL = {'null':0}

class Direction(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

class Player:
    def __init__(self, name: str):
        self.name = name
        self.board = Board()
        self.opponent_board = Board()
        self.ships_alive: list[ShipType] = [ShipType.PLANE_CARRIER, ShipType.BATTLESHIP, ShipType.CRUISER, ShipType.SUBMARINE, ShipType.DESTROYER]
        self.ships_placed: list[ShipType] = []
        self.ships_destroyed: list[ShipType] = []
    
    def place_ship(self, ship_type: ShipType, direction: Direction, start_coordinate: str) -> None:
        if ship_type in self.ships_placed:
            print(f"{ship_type.name.capitalize()} is already placed")
            return
        self.ships_placed.append(ship_type)
        self.board.add_ship(ship_type, direction, start_coordinate)
    
    def get_attack_coordinate_input(self) -> str:
        coordinate = input(f"{self.name}, enter the coordinate to attack: ").upper()
        return coordinate

    def attack(self, coordinate_str: str, opponent: 'Player'):
        try:
            x = coordinate_str[0]
            y = int(coordinate_str[1:])
        except ValueError:
            print("Invalid input")
            sleep(2)
            return
        coordinate = Coordinate(x, y)
        if coordinate in opponent.board.hit_locations or coordinate in opponent.board.miss_locations:
            print("You have already attacked this location")
            sleep(2)
            return
        opponent_is_hit, ship = opponent.board.is_hit(coordinate, opponent.ships_alive)
        if opponent_is_hit:
            if opponent.board.is_ship_destroyed(ship):
                opponent.ships_alive.remove(ship)
                opponent.ships_destroyed.append(ship)
                print(f"{ship.name.capitalize()} has been destroyed")
                sleep(2)
            return
        if opponent.board.is_miss(Coordinate(x, y)):
            return

    def is_winner(self, opponent: 'Player') -> bool:
        if len(opponent.ships_destroyed) == 5:
            return True
        return False
class Board:
    def __init__(self):
        self.board_coordinates = self.generate_coordinatee_board()
        self.ship_locations = {}
        self.hit_locations = []
        self.miss_locations = []
        

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
    
    def print_board(self, player: Player, opponent: Player) -> None:
        clear_screen()
        print(f"\n{player.name}'s board:                      {opponent.name}'s board: ")
        print(f"    A  B  C  D  E  F  G  H  I  J          A  B  C  D  E  F  G  H  I  J")
        row_number = 1
        is_not_empty_space = False
        for row in self.board_coordinates:
            if row_number < 10:
                print(f" {row_number} ", end="")
            else:
                print(f"{row_number} ", end="")
            for coordinate in row:
                try:
                    for ship in self.ship_locations:
                        if coordinate in self.hit_locations:
                            print(f"[{TextColor.RED.value}*{TextColor.DEFAULT.value}]", end="")
                            is_not_empty_space = True
                            break
                        if coordinate in self.miss_locations:
                            print(f"[{TextColor.BLUE.value}-{TextColor.DEFAULT.value}]", end="")
                            is_not_empty_space = True
                            break
                        if coordinate in self.ship_locations[ship]:
                            print(f"[{TextColor.GREEN.value}{ship.name[0]}{TextColor.DEFAULT.value}]", end="")
                            is_not_empty_space = True
                            break
                        else:
                            is_not_empty_space = False
                    if not is_not_empty_space:
                        print("[ ]", end="")
                except Exception as e:
                    print(e)
            if row_number < 10:
                print(f"      {row_number}", end=" ")
            else:
                print(f"     {row_number}", end=" ")
            for coordinate in opponent.board.board_coordinates[row_number - 1]:
                try:
                    for ship in opponent.board.ship_locations:
                        if coordinate in opponent.board.hit_locations:
                            print(f"[{TextColor.RED.value}*{TextColor.DEFAULT.value}]", end="")
                            is_not_empty_space = True
                            break
                        if coordinate in opponent.board.miss_locations:
                            print(f"[{TextColor.BLUE.value}-{TextColor.DEFAULT.value}]", end="")
                            is_not_empty_space = True
                            break
                        else:
                            is_not_empty_space = False
                    if not is_not_empty_space:
                        print("[ ]", end="")
                except Exception as e:
                    print(e)
            print("\n")
            row_number += 1

    def add_ship(self, ship_type: ShipType, direction: Direction, start_coordinate: str) -> None:
        ship_length = ship_type.value[ship_type.name.lower()]
        x = start_coordinate[0]
        y = int(start_coordinate[1:])
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
    
    def is_hit(self, coordinate: Coordinate, ships: list[ShipType]) -> Tuple[bool, ShipType]:
        for ship in ships:
            if coordinate in self.ship_locations[ship]:
                self.ship_locations[ship].remove(coordinate)
                self.hit_locations.append(coordinate)
                print(f"{ship.name.capitalize()} has been hit")
                sleep(2)
                return (True, ship)
        return (False, ShipType.NULL)
    
    def is_miss(self, coordinate: Coordinate) -> bool:
        if coordinate not in self.ship_locations:
            self.miss_locations.append(coordinate)
            print("Miss")
            sleep(2)
            return True
        return False
    
    def is_ship_destroyed(self, ship: ShipType) -> bool:
        if len(self.ship_locations[ship]) == 0:
            return True
        return False
        

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    


def place_ships(player: Player, opponent: Player):
    while len(player.ships_placed) < 5:
        for ship in player.ships_alive:
            coordinate = "A1"
            direction = Direction.HORIZONTAL
            while True:
                if ship in player.ships_placed:
                    break
                try:
                    coordinate_answer = input(f"{player.name}, where would you like to place your {ship.name.capitalize()}? Please give coordinates: ").upper()
                    coordinate_input = Coordinate(coordinate_answer[0],int(coordinate_answer[1:]))
                    if coordinate_input in [coordinate for row in player.board.board_coordinates for coordinate in row]:
                        coordinate = coordinate_answer
                        break
                    else:
                        print("Invalid coordinates")
                        continue
                except ValueError:
                    print("Invalid input")
                    continue
            while True:
                try:
                    direction_answer = input(f"Would you like to place your {ship.name.capitalize()} ship horizontally or vertically?: ").upper()
                    if direction_answer == "H" or direction_answer == "HORIZONTAL" or direction_answer == "HORIZONTALLY":
                        direction = Direction.HORIZONTAL
                        break
                    elif direction_answer == "V" or direction_answer == "VERTICAL" or direction_answer == "VERTICALLY":
                        direction = Direction.VERTICAL
                        break
                    else:
                        print("Invalid direction")
                        continue
                except ValueError:
                    print("Invalid input")
                    continue
            player.place_ship(ship, direction, coordinate)
            player.board.print_board(player, opponent)

def main():
    player1 = Player("Player1")
    player2 = Player("Player2")
    print("Welcome to Battle Ship!")
    Board().print_board(player1, player2)
    place_ships(player1, player2)
    place_ships(player2, player1)
    
    game_in_progress = True
    while game_in_progress:
        player1.board.print_board(player1, player2)
        player1.attack(player1.get_attack_coordinate_input(), player2)
        if player1.is_winner(player2):
            print(f"{player1.name} wins!")
            break
        player2.board.print_board(player2, player1)
        player2.attack(player2.get_attack_coordinate_input(), player1)
        if player2.is_winner(player1):
            print(f"{player2.name} wins!")
            break
    
if __name__ == "__main__":
    main()
    