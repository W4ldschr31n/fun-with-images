from random import randint
import time
from tkinter import Tk
from src.mosaic_gui import MosaicGUI
from src.mosaic_image import Mosaic
import sys
from PIL import Image


class Listener:
    def __init__(self, image_path):
        self.gui: MosaicGUI = None
        self.mosaic: Mosaic = None
        self.image_path = image_path
        self.current_region_clicked = None

    def set_gui(self, gui):
        self.gui = gui

    def set_mosaic(self, mosaic):
        self.mosaic = mosaic

    def display_mosaic_output(self):
        self.mosaic.save_assembled()
        self.gui.set_image("./out/mosaic.png")

    def shuffle(self):
        with Image.open(self.image_path) as im:
            self.mosaic.init_from_image(
                im,
                self.gui.get_rows(),
                self.gui.get_cols(),
            )
            self.mosaic.shuffle_regions()
            self.display_mosaic_output()

    def click_on_image(self, row, col):
        new_pos = (row, col)
        if self.current_region_clicked is None:
            self.gui.highlight_region(row, col)
            self.current_region_clicked = new_pos
        else:
            if self.current_region_clicked == new_pos:
                self.gui.unlight_region(row, col)
            else:
                self.gui.swap_regions(self.current_region_clicked, new_pos)
                self.mosaic.swap_regions_from_pos(self.current_region_clicked, new_pos)
                self.display_mosaic_output()
                self.check_is_win()

            self.current_region_clicked = None

    def check_is_win(self):
        if self.mosaic.check_is_win():
            self.gui.display_victory()
            return True

        return False

    def autoplay(self):
        # FIXME image doesnt update, maybe fork ?
        rows = self.gui.get_rows() - 1
        cols = self.gui.get_cols() - 1
        while not self.check_is_win():
            next_click_row = randint(0, rows)
            next_click_col = randint(0, cols)
            self.click_on_image(next_click_row, next_click_col)
            time.sleep(1)


# Create application
image_path = sys.argv[1]

listener = Listener(image_path)
root = Tk()

gui = MosaicGUI(root, image_path, listener)
listener.set_gui(gui)

mosaic = Mosaic(out_path="./out")
listener.set_mosaic(mosaic)

# Start running
root.mainloop()
