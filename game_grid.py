import os
import sys
import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color  # used for coloring the game grid
from lib.picture import Picture
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing


# Class used for modelling the game grid
class GameGrid:
    # Constructor for creating the game grid based on the given arguments
    def __init__(self, grid_h, grid_w):
        self.filled_rows = []
        self.score = 0
        # set the dimensions of the game grid as the given arguments
        self.level = None
        self.next_tetromino = None
        self.grid_height = grid_h
        self.grid_width = grid_w
        # create a tile matrix to store the tiles landed onto the game grid
        self.tile_matrix = np.full((grid_h, grid_w), None)
        # create the tetromino that is currently being moved on the game grid
        self.current_tetromino = None
        # the game_over flag shows whether the game is over or not
        self.game_over = False
        # set the color used for the empty grid cells
        self.empty_cell_color = Color(42, 69, 99)
        # set the colors used for the grid lines and the grid boundaries
        self.line_color = Color(0, 100, 200)
        self.boundary_color = Color(0, 100, 200)
        # thickness values used for the grid lines and the boundaries
        self.line_thickness = 0.002
        self.box_thickness = 10 * self.line_thickness

    # Method used for displaying the game grid
    def display(self):
        # clear the background to empty_cell_color
        stddraw.clear(self.empty_cell_color)
        # draw the game grid
        self.draw_grid()
        # draw the current/active tetromino if it is not None (the case when the
        # game grid is updated)
        if self.current_tetromino is not None:
            self.current_tetromino.Draw()

        if self.current_tetromino is not None:
            self.next_tetromino.preview()


        # draw a box around the game grid
        self.draw_boundaries()
        # show the resulting drawing with a pause duration = 250 ms

        score = "SCORE:"
        total_score = str(self.score)
        next = "NEXT:"
        stddraw.setPenColor(Color(255, 255, 255))
        stddraw.setFontSize(18)
        stddraw.boldText(13, 18, score)
        stddraw.boldText(13, 17, total_score)
        stddraw.boldText(13, 6, next)

        if self.level is not None:
            stddraw.show(self.level)

    def preview(self):
        if self.next_tetromino is not None:
            self.next_tetromino.preview()

    # Method for drawing the cells and the lines of the game grid
    def draw_grid(self):
        # for each cell of the game grid
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                # draw the tile if the grid cell is occupied by a tile
                if self.tile_matrix[row][col] is not None:
                    self.tile_matrix[row][col].draw(Point(col, row))
        # draw the inner lines of the grid
        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)
        # x and y ranges for the game grid
        start_x, end_x = -0.5, self.grid_width - 0.5
        start_y, end_y = -0.5, self.grid_height - 0.5
        for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
            stddraw.line(x, start_y, x, end_y)
        for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
            stddraw.line(start_x, y, end_x, y)
        stddraw.setPenRadius()  # reset the pen radius to its default value

        # Method for drawing the boundaries around the game grid

    def draw_boundaries(self):
        # draw a bounding box around the game grid as a rectangle
        stddraw.setPenColor(self.boundary_color)  # using boundary_color
        # set the pen radius as box_thickness (half of this thickness is visible
        # for the bounding box as its lines lie on the boundaries of the canvas)
        stddraw.setPenRadius(self.box_thickness)
        # the coordinates of the bottom left corner of the game grid
        pos_x, pos_y = -0.5, -0.5
        stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # Method used for checking whether the grid cell with given row and column
    # indexes is occupied by a tile or empty
    def is_occupied(self, row, col):
        # considering newly entered tetrominoes to the game grid that may have
        # tiles with position.y >= grid_height
        if not self.is_inside(row, col):
            return False
        # the cell is occupied by a tile if it is not None
        return self.tile_matrix[row][col] is not None

    # Method used for checking whether the cell with given row and column indexes
    # is inside the game grid or not
    def is_inside(self, row, col):
        if row < 0 or row >= self.grid_height:
            return False
        if col < 0 or col >= self.grid_width:
            return False
        return True

    def clearRows(self):
        filled_rows = self.checkRows()
        col_ = len(self.tile_matrix[0])
        if len(filled_rows) != 0:
            for row in filled_rows:
                for col in range(col_):
                    self.score = self.score + self.tile_matrix[row][col].number
                    self.tile_matrix[row][col] = None
        else:
            pass

    def checkRows(self):
        row_ = len(self.tile_matrix)
        col_ = len(self.tile_matrix[0])
        filled_rows = []
        for row in range(row_):
            count = 0
            for col in range(col_):
                if self.tile_matrix[row][col] is not None:
                    count = count + 1
                else:
                    break

            if count == col_:
                filled_rows.append(row)
        return filled_rows

    def drop_isolated(self):
        row_ = len(self.tile_matrix) - 1
        col_ = len(self.tile_matrix[0]) - 1
        for row in range(row_):
            row += 1
            for col in range(col_):
                if self.tile_matrix[row][col] is not None:
                    if self.tile_matrix[row][col - 1] is None:  # left
                        if self.tile_matrix[row][col + 1] is None:  # right
                            if self.tile_matrix[row - 1][col] is None:  # bottom
                                while self.tile_matrix[row - 1][col] is None:
                                    self.tile_matrix[row - 1][col] = self.tile_matrix[row][col]
                                    self.tile_matrix[row][col] = None

    def drop_isolated_twins(self):
        row_ = len(self.tile_matrix)-2
        col_ = len(self.tile_matrix[0])-1
        for row in range(row_):
            row += 1
            for col in range(col_):
                if self.tile_matrix[row][col] is not None and self.tile_matrix[row][col+1] is not None:
                    if self.tile_matrix[row][col - 1] is None: #left
                        if self.tile_matrix[row][col + 2] is None: #right
                            if self.tile_matrix[row - 1][col] is None and self.tile_matrix[row-1][col+1] is None: #bottom
                                while self.tile_matrix[row - 1][col] is None and self.tile_matrix[row - 1][col+1] is None:
                                    self.tile_matrix[row - 1][col] = self.tile_matrix[row][col]
                                    self.tile_matrix[row - 1][col + 1] = self.tile_matrix[row][col + 1]
                                    self.tile_matrix[row][col] = None
                                    self.tile_matrix[row][col + 1] = None

    def merge(self):
        row_ = len(self.tile_matrix) - 1
        col_ = len(self.tile_matrix[0])
        for row in range(row_):
            for col in range(col_):
                if self.tile_matrix[row][col] is not None and self.tile_matrix[row - 1][col] is not None:
                    if self.tile_matrix[row][col].number == self.tile_matrix[row - 1][col].number:
                        self.tile_matrix[row - 1][col].number = 2 * self.tile_matrix[row][col].number
                        self.score = self.score + self.tile_matrix[row - 1][col].number
                        self.color(row - 1, col)
                        self.tile_matrix[row][col] = None
                        self.tile_matrix[row][col] = self.tile_matrix[row + 1][col]
                        self.tile_matrix[row + 1][col] = None

    def color(self, row, col):
        if self.tile_matrix[row][col].number == 4:
            self.tile_matrix[row][col].background_color = Color(238, 217, 177)
        elif self.tile_matrix[row][col].number == 8:
            self.tile_matrix[row][col].background_color = Color(242, 177, 121)
        elif self.tile_matrix[row][col].number == 16:
            self.tile_matrix[row][col].background_color = Color(245, 149, 99)
        elif self.tile_matrix[row][col].number == 32:
            self.tile_matrix[row][col].background_color = Color(246, 124, 95)
        elif self.tile_matrix[row][col].number == 64:
            self.tile_matrix[row][col].background_color = Color(246, 94, 59)
        elif self.tile_matrix[row][col].number == 128:
            self.tile_matrix[row][col].background_color = Color(237, 207, 114)
        elif self.tile_matrix[row][col].number == 256:
            self.tile_matrix[row][col].background_color = Color(237, 204, 97)
        elif self.tile_matrix[row][col].number == 512:
            self.tile_matrix[row][col].background_color = Color(237, 200, 80)
        elif self.tile_matrix[row][col].number == 1024:
            self.tile_matrix[row][col].background_color = Color(237, 197, 63)
        elif self.tile_matrix[row][col].number == 2048:
            self.tile_matrix[row][col].background_color = Color(237, 194, 46)

    # Method that locks the tiles of the landed tetromino on the game grid while
    # checking if the game is over due to having tiles above the topmost grid row.
    # The method returns True when the game is over and False otherwise.
    def update_grid(self, tiles_to_lock, blc_position):
        # necessary for the display method to stop displaying the tetromino
        self.current_tetromino = None
        # lock the tiles of the current tetromino (tiles_to_lock) on the game grid
        n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
        for col in range(n_cols):
            for row in range(n_rows):
                # place each tile onto the game grid
                if tiles_to_lock[row][col] is not None:
                    # compute the position of the tile on the game grid
                    pos = Point()
                    pos.x = blc_position.x + col
                    pos.y = blc_position.y + (n_rows - 1) - row
                    if self.is_inside(pos.y, pos.x):
                        self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
                    # the game is over if any placed tile is above the game grid
                    else:
                        self.game_over = True
        # return the game_over flag
        return self.game_over

    def gameOver(self):
        stddraw.clearKeysTyped()
        background_color = Color(42, 69, 99)
        button_color = Color(25, 255, 228)
        text_color = Color(0, 255, 17)
        # clear the background canvas to background_color
        stddraw.clear(background_color)
        # get the directory in which this python code file is placed
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # path of the image file
        img_file = current_dir + "/images/menu_image.png"
        # center coordinates to display the image
        img_center_x, img_center_y = 16 / 2, self.grid_height - 7
        # image is represented using the Picture class
        image_to_display = Picture(img_file)
        # display the image
        stddraw.picture(image_to_display, img_center_x, img_center_y)
        # dimensions of the start game button
        easy_button_w, easy_button_h = 6, 1.5
        normal_button_w, normal_button_h = 6, 1.5
        # coordinates of the bottom left corner of the start game button
        easy_button_blc_x, easy_button_blc_y = img_center_x - easy_button_w / 2, 5
        normal_button_blc_x, normal_button_blc_y = img_center_x - normal_button_w / 2, 3

        # display the start game button as a filled rectangle
        stddraw.setPenColor(button_color)
        stddraw.filledRectangle(easy_button_blc_x, easy_button_blc_y, easy_button_w, easy_button_h)
        stddraw.filledRectangle(normal_button_blc_x, normal_button_blc_y, normal_button_w, normal_button_h)
        # display the text on the start game button
        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(25)
        stddraw.setPenColor(text_color)
        text_to_display = "The Game is Over"
        stddraw.text(img_center_x, 9, text_to_display)

        total_score = "Total Score is: " + str(self.score)
        stddraw.text(img_center_x, 8, total_score)

        stddraw.setPenColor(Color(255, 0, 0))
        easy = "Restart"
        stddraw.text(img_center_x, 5.7, easy)
        normal = "Quit"
        stddraw.text(img_center_x, 3.7, normal)
        while True:
            # display the menu and wait for a short time (50 ms)
            stddraw.show(50)
            # check if the mouse has been left-clicked on the button
            if stddraw.mousePressed():
                # get the x and y coordinates of the location at which the mouse has
                # most recently been left-clicked
                mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
                # check if these coordinates are inside the button
                if easy_button_blc_x <= mouse_x <= easy_button_blc_x + easy_button_w:
                    if easy_button_blc_y <= mouse_y <= easy_button_blc_y + easy_button_h:
                        os.execl(sys.executable, sys.executable, *sys.argv)
                    elif normal_button_blc_y <= mouse_y <= normal_button_blc_y + normal_button_h:
                        sys.exit()
