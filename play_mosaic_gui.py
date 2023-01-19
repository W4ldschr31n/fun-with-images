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

    def set_gui(self, gui):
        self.gui = gui

    def set_mosaic(self, mosaic):
        self.mosaic = mosaic

    def shuffle(self):
        with Image.open(self.image_path) as im:
            self.mosaic.init_from_image(
                im,
                self.gui.get_rows(),
                self.gui.get_cols(),
            )
            self.mosaic.shuffle_regions()
            self.mosaic.save_assembled()
        self.gui.set_image("./out/mosaic.png")


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
