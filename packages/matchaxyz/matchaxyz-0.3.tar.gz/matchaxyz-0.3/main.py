# matcha_game.py

import random

def create_board(size):
    """
    Create a board with randomized symbols.

    Args:
    - size: Size of the board (number of pairs)

    Returns:
    - board: A list representing the game board
    """
    symbols = [chr(i) for i in range(65, 65+size)] * 2
    random.shuffle(symbols)
    board = [symbols[i:i+size] for i in range(0, size*2, size)]
    return board

def display_board(board, revealed):
    """
    Display the game board.

    Args:
    - board: The game board
    - revealed: A list representing which symbols are revealed
    """
    for i in range(len(board)):
        row = ""
        for j in range(len(board[i])):
            if revealed[i][j]:
                row += board[i][j] + " "
            else:
                row += "X "
        print(row)

def check_match(board, revealed, row1, col1, row2, col2):
    """
    Check if the symbols at the given coordinates match.

    Args:
    - board: The game board
    - revealed: A list representing which symbols are revealed
    - row1, col1: Coordinates of the first symbol
    - row2, col2: Coordinates of the second symbol

    Returns:
    - True if the symbols match, False otherwise
    """
    return board[row1][col1] == board[row2][col2]

def main():
    size = 4  # Change this to adjust the size of the game board
    board = create_board(size)
    revealed = [[False] * size for _ in range(size)]

    while True:
        display_board(board, revealed)
        print("Enter coordinates of two symbols to reveal (e.g., '0 1 1 2'): ")
        row1, col1, row2, col2 = map(int, input().split())

        if row1 < 0 or row1 >= size or col1 < 0 or col1 >= size \
                or row2 < 0 or row2 >= size or col2 < 0 or col2 >= size:
            print("Invalid coordinates. Please try again.")
            continue

        if revealed[row1][col1] or revealed[row2][col2]:
            print("Those symbols are already revealed. Please choose again.")
            continue

        revealed[row1][col1] = True
        revealed[row2][col2] = True
        display_board(board, revealed)

        if check_match(board, revealed, row1, col1, row2, col2):
            print("Congratulations! You found a match!")
        else:
            print("Sorry, those symbols do not match.")

if __name__ == "__main__":
    main()
