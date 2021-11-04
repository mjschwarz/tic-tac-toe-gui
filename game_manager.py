import sys
import time
from board import *
import pygame.locals as pgl


def launch_game(board):
    """
    Launches the game with an empty board.

    :param board: the board being played upon
    :return: none

    """

    # create board background
    board.display.fill(board.board_color)
    # draw vertical grib lines
    pg.draw.line(board.display, board.line_color, (board.width / 3, 0), (board.width / 3, board.height), 7)
    pg.draw.line(board.display, board.line_color, (board.width / 3 * 2, 0), (board.width / 3 * 2, board.height), 7)
    # draw horizontal grid lines
    pg.draw.line(board.display, board.line_color, (0, board.height / 3), (board.width, board.height / 3), 7)
    pg.draw.line(board.display, board.line_color, (0, board.height / 3 * 2), (board.width, board.height / 3 * 2), 7)
    # write message and push updates
    display_message(board)


def reset_game(board):
    """
    Resets the board state and launches a new game.

    :param board: the board being played upon
    :return: none

    """

    # wait to improve user experience
    time.sleep(1)
    # reset board state
    board.reset_board()
    # launch new game
    launch_game(board)


def play_game(board):
    """
    Manages the flow of gameplay and user actions.

    :param board: the board being played upon
    :return: none

    """

    # forever loop
    while True:
        # queue of user actions
        for event in pg.event.get():
            if event.type == pgl.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pgl.MOUSEBUTTONDOWN:
                make_move(board)
                if board.winner or board.draw:
                    reset_game(board)
        pg.display.update()
        board.Clock.tick(board.fps)


def make_move(board):
    """
    Receives user input and determines where move was made.

    :param board: the board being played upon
    :return: none

    """

    # get coordinates of mouse click
    x, y = pg.mouse.get_pos()

    # get column of move
    if x < board.width / 3:
        col = 1
    elif x < board.width / 3 * 2:
        col = 2
    elif x < board.width:
        col = 3
    else:
        col = None

    # get row of move
    if y < board.height / 3:
        row = 1
    elif y < board.height / 3 * 2:
        row = 2
    elif y < board.height:
        row = 3
    else:
        row = None

    # display move and check for game completion
    if row and col and (board.state[row - 1][col - 1] is None):
        display_move(board, row, col)
        check_win_or_draw(board)


def display_move(board, row, col):
    """
    Updates the visual display to show the user's move.

    :param board: the board being played upon
    :param row: the row of the user's move
    :param col: the column of the user's move
    :return: none

    """

    # determine which in square move was made
    # x_pos, y_pos determined by sizes of display window and images
    if row == 1:
        x_pos = 30
    elif row == 2:
        x_pos = board.width / 3 + 30
    else:  # row == 3:
        x_pos = board.width / 3 * 2 + 30

    if col == 1:
        y_pos = 30
    elif col == 2:
        y_pos = board.height / 3 + 30
    else:  # col == 3:
        y_pos = board.height / 3 * 2 + 30

    # add player marker to board state
    board.state[row - 1][col - 1] = board.cur_player
    # place 'x' or 'o' img on board
    if board.cur_player == 'x':
        board.display.blit(board.x_icon, (y_pos, x_pos))
        board.cur_player = 'o'
    else:
        board.display.blit(board.o_icon, (y_pos, x_pos))
        board.cur_player = 'x'
    # update display
    pg.display.update()


def check_win_or_draw(board):
    """
    Checks whether win or draw conditions have been met.

    :param board: the board being played upon
    :return: none
    """

    # if winner found draw a red line connecting moves

    # check rows for winner
    for row in range(0, 3):
        if (board.winner is None) and (board.state[row][0]) and \
                (board.state[row][0] == board.state[row][1] == board.state[row][2]):
            board.winner = board.state[row][0]
            pg.draw.line(board.display, (250, 0, 0), (0, (row + 1) * board.height / 3 - board.height / 6),
                         (board.width, (row + 1) * board.height / 3 - board.height / 6), 4)
            break

    # check columns for winner
    for col in range(0, 3):
        if (board.winner is None) and (board.state[0][col] is not None) \
                and (board.state[0][col] == board.state[1][col] == board.state[2][col]):
            board.winner = board.state[0][col]
            pg.draw.line(board.display, (250, 0, 0), ((col + 1) * board.width / 3 - board.width / 6, 0),
                         ((col + 1) * board.width / 3 - board.width / 6, board.height), 4)
            break

    # check diagonal bottom left to top right for winner
    if (board.winner is None) and (board.state[0][0] is not None) \
            and (board.state[0][0] == board.state[1][1] == board.state[2][2]):
        board.winner = board.state[0][0]
        pg.draw.line(board.display, (250, 70, 70), (50, 50), (350, 350), 4)

    # check diagonal top left to bottom right for winner
    elif (board.winner is None) and (board.state[0][2] is not None) \
            and (board.state[0][2] == board.state[1][1] == board.state[2][0]):
        board.winner = board.state[0][2]
        pg.draw.line(board.display, (250, 70, 70), (350, 50), (50, 350), 4)

    # check for draw
    elif (board.winner is None) and (all([all(row) for row in board.state])):
        board.draw = True

    # display winner, draw, or next turn message
    display_message(board)


def display_message(board):
    """
    Updates the message at the bottom of the display.

    :param board: the board being played upon
    :return: none

    """

    # determine which message to display
    if board.winner:
        message = board.winner.upper() + " Wins!"
    elif board.draw:
        message = "Draw!"
    else:
        message = board.cur_player.upper() + "'s Turn"

    # set font size and color for message
    text = pg.font.Font(None, 50).render(message, True, (255, 255, 255))
    # place message on board
    board.display.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(board.width / 2, 500 - 50))
    board.display.blit(text, text_rect)
    # update display
    pg.display.update()
