import sys
import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.picture import Picture  # used for displaying images
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types/shapes


# MAIN FUNCTION OF THE PROGRAM
# -------------------------------------------------------------------------------
# Main function where this program starts execution
def start():
    # set the dimensions of the game grid
    grid_h, grid_w = 20, 17
    # set the size of the drawing canvas
    canvas_h, canvas_w = 40 * grid_h, 40 * grid_w
    stddraw.setCanvasSize(canvas_w, canvas_h)
    # set the scale of the coordinate system
    stddraw.setXscale(-0.5, grid_w - 0.5)
    stddraw.setYscale(-0.5, grid_h - 0.5)

    # set the dimension values stored and used in the Tetromino class
    Tetromino.grid_height = 20
    Tetromino.grid_width = 12

    # create the game grid
    grid = GameGrid(20, 12)
    # create the first tetromino to enter the game grid
    # by using the create_tetromino function defined below
    current_tetromino = create_tetromino(grid_h, grid_w)
    grid.current_tetromino = current_tetromino

    next_tetromino = create_tetromino(grid_h, grid_w)
    grid.next_tetromino = next_tetromino

    # display a simple menu before opening the game
    # by using the display_game_menu function defined below
    grid.level = display_game_menu(grid_h, grid_w)

    # the main game loop (keyboard interaction for moving the tetromino)
    while True:
        # check user interactions via the keyboard
        if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
            key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
            # if the left arrow key has been pressed
            if key_typed == "left":
                # move the active tetromino left by one
                current_tetromino.move(key_typed, grid)
                # if the right arrow key has been pressed
            elif key_typed == "right":
                # move the active tetromino right by one
                current_tetromino.move(key_typed, grid)
            # if the down arrow key has been pressed
            elif key_typed == "down":
                # move the active tetromino down by one
                # (soft drop: causes the tetromino to fall down faster)
                current_tetromino.move(key_typed, grid)
            elif key_typed == "space":
                current_tetromino.move(key_typed, grid)
            elif key_typed == "escape":
                pause(grid_h, grid_w)

            # clear the queue of the pressed keys for a smoother interaction
            stddraw.clearKeysTyped()

        # move the active tetromino down by one at each iteration (auto fall)
        success = current_tetromino.move("down", grid)

        # place the active tetromino on the grid when it cannot go down anymore
        if not success:
            # get the tile matrix of the tetromino without empty rows and columns
            # and the position of the bottom left cell in this matrix
            tiles, pos = grid.current_tetromino.get_min_bounded_tile_matrix(True)
            # update the game grid by locking the tiles of the landed tetromino
            game_over = grid.update_grid(tiles, pos)
            # end the main game loop if the game is over
            if game_over:
                grid.gameOver()
            # create the next tetromino to enter the game grid
            # by using the create_tetromino function defined below

            current_tetromino = next_tetromino
            next_tetromino = create_tetromino(grid_h, grid_w)
            grid.next_tetromino = next_tetromino
            grid.current_tetromino = current_tetromino
        # display the game grid and the current tetromino

        grid.merge()
        grid.clearRows()
        grid.display()
        grid.drop_isolated()
        grid.drop_isolated_twins()


# Function for creating random shaped tetrominoes to enter the game grid
def create_tetromino(grid_height, grid_width):
    # type (shape) of the tetromino is determined randomly
    tetromino_types = ['I', 'O', 'Z', 'L', 'J', 'S', 'T']
    random_index = random.randint(0, len(tetromino_types) - 1)
    random_type = tetromino_types[random_index]
    # create and return the tetromino
    tetromino = Tetromino(random_type)

    return tetromino


def pause(grid_height, grid_width):
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
    img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
    # image is represented using the Picture class
    image_to_display = Picture(img_file)
    # display the image
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    # dimensions of the start game button
    easy_button_w, easy_button_h = grid_width - 11, 1.5
    normal_button_w, normal_button_h = grid_width - 11, 1.5
    # coordinates of the bottom left corner of the start game button
    easy_button_blc_x, easy_button_blc_y = img_center_x - easy_button_w / 2, 6
    normal_button_blc_x, normal_button_blc_y = img_center_x - normal_button_w / 2, 4

    # display the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(easy_button_blc_x, easy_button_blc_y, easy_button_w, easy_button_h)
    stddraw.filledRectangle(normal_button_blc_x, normal_button_blc_y, normal_button_w, normal_button_h)
    # display the text on the start game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)
    text_to_display = "The Game is Paused"
    stddraw.text(img_center_x, 9, text_to_display)

    stddraw.setPenColor(Color(255, 0, 0))
    easy = "Continue"
    stddraw.text(img_center_x, 6.7, easy)
    normal = "Restart"
    stddraw.text(img_center_x, 4.7, normal)
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
                    break
                elif normal_button_blc_y <= mouse_y <= normal_button_blc_y + normal_button_h:
                    os.execl(sys.executable, sys.executable, *sys.argv)


def display_options(grid_height, grid_width, grid=None):
    # colors used for the menu
    background_color = Color(42, 69, 99)
    # clear the background canvas to background_color
    stddraw.clear(background_color)
    # get the directory in which this python code file is placed
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # path of the image file
    img_file = current_dir + "/images/Options.png"
    # center coordinates to display the image
    img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 10
    # image is represented using the Picture class
    image_to_display = Picture(img_file)
    # display the image
    stddraw.picture(image_to_display, img_center_x, img_center_y)

    while True:
        stddraw.show(50)
        # check user interactions via the keyboard
        if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
            key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
            # if the left arrow key has been pressed
            if key_typed == "escape":
                display_game_menu(grid_height, grid_width)
                break
        stddraw.clearKeysTyped()


# Function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width, grid=None):
    # colors used for the menu
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
    img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
    # image is represented using the Picture class
    image_to_display = Picture(img_file)
    # display the image
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    # dimensions of the start game button
    easy_button_w, easy_button_h = grid_width - 11, 1.5
    normal_button_w, normal_button_h = grid_width - 11, 1.5
    hard_button_w, hard_button_h = grid_width - 11, 1.5
    settings_w, settings_h = grid_width - 9, 1.5
    # coordinates of the bottom left corner of the start game button
    easy_button_blc_x, easy_button_blc_y = img_center_x - easy_button_w / 2, 6
    normal_button_blc_x, normal_button_blc_y = img_center_x - normal_button_w / 2, 4
    hard_button_blc_x, hard_button_blc_y = img_center_x - hard_button_w / 2, 2
    settings_blc_x, settings_blc_y = img_center_x - settings_w / 2, 0
    # display the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(easy_button_blc_x, easy_button_blc_y, easy_button_w, easy_button_h)
    stddraw.filledRectangle(normal_button_blc_x, normal_button_blc_y, normal_button_w, normal_button_h)
    stddraw.filledRectangle(hard_button_blc_x, hard_button_blc_y, hard_button_w, hard_button_h)
    stddraw.filledRectangle(settings_blc_x, settings_blc_y, settings_w, settings_h)
    # display the text on the start game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)
    text_to_display = "Choose a Level for Start the Game"
    stddraw.text(img_center_x, 9, text_to_display)

    stddraw.setPenColor(Color(255, 0, 0))
    easy = "EASY"
    stddraw.text(img_center_x, 6.7, easy)
    normal = "NORMAL"
    stddraw.text(img_center_x, 4.7, normal)
    hard = "HARD"
    stddraw.text(img_center_x, 2.7, hard)
    settings = "HOW TO PLAY"
    stddraw.text(img_center_x, 0.7, settings)
    # menu interaction loop
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
                    return 250
                elif normal_button_blc_y <= mouse_y <= normal_button_blc_y + normal_button_h:
                    return 150
                elif hard_button_blc_y <= mouse_y <= hard_button_blc_y + hard_button_h:
                    return 50
                elif settings_blc_y <= mouse_y <= settings_blc_y + settings_h:
                    display_options(grid_height, grid_width)


# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
    start()
