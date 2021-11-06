import pygame as pg


class Board:
    """Represents a board to be played upon"""

    def __init__(self):
        """Initializes an empty board.

        Attributes
        __________
        winner: whether a winner has been found
        draw: whether a draw has been found
        cur_player: whose turn it is ('x' or 'o')
        state: current state of the board in terms of player moves
        width: width of the board (in pixels)
        height: height of the board (in pixels)
        board_color: background color of the board (given as (R,G,B))
        line_color: color of grid lines (given as (R,G,B))
        fps: frames per second of the game player
        Clock: clock object from to track time
        display: window to display gameplay on
        x_icon: image for 'x' player
        o_icon: image for 'o' player

        """

        self.winner = None
        self.draw = None
        self.cur_player = 'x'  # player 'x' always starts
        self.state = [[None] * 3, [None] * 3, [None] * 3]

        self.width = 400
        self.height = 400
        self.board_color = (255, 255, 255)  # white
        self.line_color = (0, 0, 0)  # black

        pg.init()

        self.fps = 30
        self.Clock = pg.time.Clock()
        self.display = pg.display.set_mode((self.width, self.height + 100), 0, 32)

        pg.display.set_caption("Tic Tac Toe")

        self.x_icon = pg.image.load("images/x_img.png")
        self.o_icon = pg.image.load("images/o_img.png")

    def reset_board(self):
        self.winner = None
        self.draw = None
        self.cur_player = 'x'
        self.state = [[None] * 3, [None] * 3, [None] * 3]
