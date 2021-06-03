import sys
import string
import copy
from termcolor import colored
from math import floor, ceil
import graphics
import random
from os import system, name

def quit_function(text):
    if text.lower() == "quit":
        sys.exit(0)

def board_setup():
    input_succesful = True
    while input_succesful:
        board_size = input("Please select the board size. The maximum size is 10 and the minimum is 5.\n ")
        quit_function(board_size)
        if board_size.isdigit() and int(board_size) in range(5, 11):
            return int(board_size)
        else:
            print("Invalid input! (must be between 5-10)" )

def coordinates(board_size, alphabet):
    valid_coordinates = {}
    for i in range(board_size):
        for number in range(board_size):
            valid_coordinates[alphabet[i] + str(number + 1)] = i , number
    return valid_coordinates        

def init_board(board_size):
    return [list("-" * board_size) for i in range(board_size)]

def print_board(board, board_size, alphabet):
    # print(f"Your move: {active_player}")
    first_row = map(str, [*range(1, board_size + 1)])
    print("\n")
    print(f"  {' '.join(first_row)}")
    for i in range(len(board)):
        print(f"{alphabet[i]} {' '.join(board[i])}")
    print("\n")

def is_occupied(direction, hidden_board, row, column, ships_to_place):
    try:
        if direction == "h":
            for element in range(len(ships_to_place[0])):
                if hidden_board[row][column] != "X":
                    column +=1
                else:
                    return True
            return False
        elif direction == "v":
            for element in range(len(ships_to_place[0])):
                if hidden_board[row][column] != "X":
                    row +=1
                else:
                    return True
            return False
    except:
        return True

def ships_placement(valid_coordinates, board, ships_to_place, hidden_board, player):
    while True:
        ship = input(f"Please select the coordinates of your {ships_to_place[0]} ship: ")
        quit_function(ship)
        if ship.upper() in valid_coordinates.keys():
            row, column = valid_coordinates[ship.upper()]
            direction = ships_placement_direction(player)
            occupied = is_occupied(direction, hidden_board, row, column, ships_to_place)
            if occupied == False:
                row, column = valid_coordinates[ship.upper()]
                return row, column, direction
            else:
                print("Ships are too close!")        
        else:
            print("Invalid input!")

def ships_placement_direction(player):
    valid_input = True
    while valid_input:
        ship_direction = input(f"{player}: Please select the direction of the ship. Vertical - V or Horizontal - H: ")
        quit_function(ship_direction)
        if ship_direction.lower() == "h" or ship_direction.lower() == "v":
            direction = ship_direction.lower()
            return direction 
        else:
            print("Invalid input!")

def mark_placement(row, column, direction, ships_to_place, board, hidden_board):
    marked_ships = []
    hidden_row = copy.deepcopy(row)
    hidden_column = copy.deepcopy(column)
    for element in range(len(ships_to_place[0])):
        board[row][column] = "X"
        marked_ships.append((row, column))
        hidden_board[row][column]= "X"
        if direction == "h":
            column += 1
        elif direction == "v":
            row +=1
    for element in range(len(ships_to_place[0])):
        if hidden_row + 1 < len(hidden_board):
            hidden_board[hidden_row+1][hidden_column] = "X"
        if hidden_row - 1 >= 0:
            hidden_board[hidden_row-1][hidden_column] = "X"
        if hidden_column + 1 < len(hidden_board):
            hidden_board[hidden_row][hidden_column+1] = "X"
        if hidden_column - 1 >= 0:
            hidden_board[hidden_row][hidden_column-1] = "X"
    ships_to_place.pop(0)
    return marked_ships
    
def number_of_ships(board_size):
    if board_size == 5:
        ships_to_place = ["X", "X", "XX", "XXX"]
    elif board_size == 6:
        ships_to_place = ["X", "X", "XX", "XX", "XXX"]
    elif board_size == 7:
        ships_to_place = ["X", "X", "XX", "XX", "XXX", "XXX"]
    elif board_size == 8:
        ships_to_place = ["X", "X", "XX", "XX", "XXX", "XXX", "XXXX"]
    elif board_size == 9:
        ships_to_place = ["X", "X", "XX", "XX", "XX" "XXX", "XXX" "XXXX"]
    else:
        ships_to_place = ["XX", "XX", "XX", "XX", "XXX" "XXX", "XXX", "XXXX", "XXXXX"]
    hits_to_win = 0
    for element in ships_to_place:
        hits_to_win += len(element)
    return ships_to_place, hits_to_win
    
def shooting_phase(shooting_board, board, valid_coordinates, player):
    print(f"Hello {player}! Your turn! ")
    while True:
        shot = input("Please choose the coordinates of your shot: ")
        quit_function(shot)
        if shot.upper() in valid_coordinates:
            row, col = valid_coordinates[shot.upper()]
            if board[row][col] == "X" :
                shooting_board[row][col] = colored("H", 'blue')
                print("Nice, you hit the ship! ")
                break
            else:
                shooting_board[row][col] = colored("M", 'red')
                print("You missed! ")   
                break     
        else:
            print("Please select valid coordinates.")

def has_won(shooting_board, hits_to_win):
    sum_of_hits = 0
    for element in shooting_board:
       sum_of_hits += element.count(colored("S", 'yellow'))
    return sum_of_hits == hits_to_win

def player_generator():
    player_name_1 = input("Player 1: Please input your name: ")
    quit_function(player_name_1)
    player_name_2 = input("Player 2: Please input your name: ")
    quit_function(player_name_2)
    return player_name_1, player_name_2


def switch(active_player, player_1, player_2):
    if active_player == player_1:
        return player_2
    elif active_player == player_2:
        return player_1


def sunken_check(marked_ships, board):
   for element in marked_ships:
        counter = 0
        for i in element:
            row, column = i
            if board[row][column] == colored("H", 'blue'):
                counter += 1
        if counter == len(element):
            for i in element:
                row, column = i
                board[row][column] = colored("S", 'yellow')
            print("You've sunk a ship!")


def is_tie(counter):
    return False if counter > 0 else True


def planing_phase(ships_to_place, player_board, board_size, alphabet, player, valid_coordinates, hidden_board):
    print("\n" + f"Planing phase for {player} has begun! {player} please place your ships! ")
    print_board(player_board, board_size, alphabet)
    marked_ships = []
    while len(ships_to_place) > 0:
        row, column, direction = ships_placement(valid_coordinates, player_board, ships_to_place, hidden_board, player)
        marked_ship = mark_placement(row, column, direction, ships_to_place, player_board, hidden_board)
        marked_ships.append(marked_ship)
        clear()
        print_board(player_board, board_size, alphabet)
    print(f"Planing phase for {player} has ended! ")
    return marked_ships

def player_generator_ai():
    player_name_1 = input("Player 1: Please input your name: ")
    quit_function(player_name_1)
    player_name_2 = "AI-George"
    return player_name_1, player_name_2

def planing_phase_ai(ships_to_place, player_board, board_size, alphabet, player, valid_coordinates, hidden_board):
    print("\n" + f"Planing phase for {player} has begun! {player} please place your ships! ")
    print_board(player_board, board_size, alphabet)
    marked_ships = []
    while len(ships_to_place) > 0:
        row, column, direction = ships_placement_ai(valid_coordinates, player_board, ships_to_place, hidden_board, player)
        marked_ship = mark_placement(row, column, direction, ships_to_place, player_board, hidden_board)
        marked_ships.append(marked_ship)
        clear()
        print_board(player_board, board_size, alphabet)
    print(f"Planing phase for {player} has ended! ")
    return marked_ships

def ships_placement_ai(valid_coordinates, board, ships_to_place, hidden_board, player):
    while True:
        ship = random.choice(list(valid_coordinates.keys()))
        row, column = valid_coordinates[ship]
        direction = random.choice(["h", "v"])
        occupied = is_occupied(direction, hidden_board, row, column, ships_to_place)
        if occupied == False:
            row, column = valid_coordinates[ship]
            return row, column, direction
        else:
            continue   

def shooting_phase_ai(shooting_board, board, valid_coordinates, player):
    print(f"Hello {player}! Your turn! ")
    while True:
        list_of_valid_coordinates = list(valid_coordinates.keys())
        shot = random.choice(list_of_valid_coordinates)
        list_of_valid_coordinates.remove(shot)

        row, col = valid_coordinates[shot]
        if board[row][col] == "X" :
            shooting_board[row][col] = colored("H", 'blue')
            print("Nice, AI-George hit the ship! ")
            break
        else:
            shooting_board[row][col] = colored("M", 'red')
            print("AI-George missed! ")   
            break     

def battleships_HH():
    alphabet = string.ascii_uppercase
    board_size = board_setup()
    clear()
    counter = floor(board_size**2 * 0.75)*2
    valid_coordinates = coordinates(board_size, alphabet)

    player_1, player_2 = player_generator()
    
    player_1_board = init_board(board_size)
    player_1_hidden_board = init_board(board_size)
    player_1_shooting_board = init_board(board_size)
    
    player_2_board = init_board(board_size)
    player_2_hidden_board = init_board(board_size)
    player_2_shooting_board = init_board(board_size)

    player_1_ships_to_place, hits_to_win = number_of_ships(board_size)
    player_2_ships_to_place, hits_to_win = number_of_ships(board_size)
    clear()
    input(f"\n{player_1} PLACEMENT PHASE")
    marked_ships_1 = planing_phase(player_1_ships_to_place, player_1_board, board_size, alphabet, player_1, valid_coordinates, player_1_hidden_board)
    clear()
    input(f"\n{player_2} PLACEMENT PHASE")
    marked_ships_2 = planing_phase(player_2_ships_to_place, player_2_board, board_size, alphabet, player_2, valid_coordinates, player_2_hidden_board)
    clear()
    
    active_marked_ships = marked_ships_2
    active_player = player_1
    active_board = player_2_board
    active_shooting_board = player_1_shooting_board

    while has_won(active_shooting_board, hits_to_win) == False:
        clear()
        print(f"Turns left:{ceil(counter/2)}")
        print_board(active_shooting_board, board_size, alphabet)
        shooting_phase(active_shooting_board, active_board, valid_coordinates, active_player)
        sunken_check(active_marked_ships, active_shooting_board)
        if has_won(active_shooting_board, hits_to_win) == True:
            print(f'Contratulations {active_player}, you have won!')
            print_board(active_shooting_board, board_size, alphabet)
            break
        if is_tie(counter):
            print(f"No more turns, it's a draw!")
            break
        counter -= 1          
        print_board(active_shooting_board, board_size, alphabet)
        active_player = switch(active_player, player_1, player_2)
        active_board = switch(active_board, player_1_board, player_2_board)
        active_shooting_board = switch(active_shooting_board, player_1_shooting_board, player_2_shooting_board) 
        active_marked_ships = switch(active_marked_ships, marked_ships_1, marked_ships_2) 
        print(f"TURN END! Next player: {active_player}")

def battleships_AI():
    alphabet = string.ascii_uppercase
    board_size = board_setup()
    clear()
    counter = floor(board_size**2 * 0.75)*2
    valid_coordinates = coordinates(board_size, alphabet)

    player_1, player_2 = player_generator_ai()
    
    player_1_board = init_board(board_size)
    player_1_hidden_board = init_board(board_size)
    player_1_shooting_board = init_board(board_size)
    
    player_2_board = init_board(board_size)
    player_2_hidden_board = init_board(board_size)
    player_2_shooting_board = init_board(board_size)

    player_1_ships_to_place, hits_to_win = number_of_ships(board_size)
    player_2_ships_to_place, hits_to_win = number_of_ships(board_size)
    input(f"\n{player_1} PLACEMENT PHASE")
    marked_ships_1 = planing_phase(player_1_ships_to_place, player_1_board, board_size, alphabet, player_1, valid_coordinates, player_1_hidden_board)
    input(f"\n{player_2} PLACEMENT PHASE")
    marked_ships_2 = planing_phase_ai(player_2_ships_to_place, player_2_board, board_size, alphabet, player_2, valid_coordinates, player_2_hidden_board)
    
    active_marked_ships = marked_ships_2
    active_player = player_1
    active_board = player_2_board
    active_shooting_board = player_1_shooting_board

    while has_won(active_shooting_board, hits_to_win) == False:
        clear()
        print(f"Turns left:{ceil(counter/2)}")
        print_board(active_shooting_board, board_size, alphabet)
        if active_player == player_1:
            shooting_phase(active_shooting_board, active_board, valid_coordinates, active_player)
        else:
            shooting_phase_ai(active_shooting_board, active_board, valid_coordinates, active_player)
        sunken_check(active_marked_ships, active_shooting_board)
        if has_won(active_shooting_board, hits_to_win) == True:
            print(f'Contratulations {active_player}, you have won!')
            print_board(active_shooting_board, board_size, alphabet)
            break
        if is_tie(counter):
            print(f"No more turns, it's a draw!")
            break
        counter -= 1          
        print_board(active_shooting_board, board_size, alphabet)
        active_player = switch(active_player, player_1, player_2)
        active_board = switch(active_board, player_1_board, player_2_board)
        active_shooting_board = switch(active_shooting_board, player_1_shooting_board, player_2_shooting_board) 
        active_marked_ships = switch(active_marked_ships, marked_ships_1, marked_ships_2) 
        print(f"TURN END! Next player: {active_player}")

def play_again():
    while True:
        again = input("Do you want to play again? Y/N")
        if again.lower() == "y":
            return True
        elif again.lower() == "n":
            return False
        else:
            print("Invalid input!")

def main_menu():
    graphics.ascii_battleships()
    while True:
        game_mode = input("Game mode: ")
        quit_function(game_mode)
        if game_mode == "1":
            battleships_AI()
            break    
        elif game_mode == "2":
            battleships_HH()
            break                
        else:
            print("Invalid input!")

def main_function():
    clear()
    main_menu()
    if play_again() == True:
        main_menu()
    else:
        sys.exit(0)

def clear():
    if name == 'nt':
        _ = system('cls')

main_function()