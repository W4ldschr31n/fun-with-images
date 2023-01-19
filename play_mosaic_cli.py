import sys
from PIL import Image
from src.mosaic_image import Mosaic


filepath = sys.argv[1]
cols, rows = 3, 3
mosaic = Mosaic(out_path="./out")
with Image.open(filepath) as im:
    mosaic.init_from_image(im, cols, rows)
mosaic.save_regions()
mosaic.shuffle_regions()
mosaic.save_assembled()
try:
    mosaic.play_from_cli()
except KeyboardInterrupt:
    print("\nGoodbye !")
