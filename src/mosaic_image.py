from random import randint, choice
from typing import List, Tuple
from PIL import Image
import logging


class Region:
    def __init__(self, im: Image, box: Tuple[int, int, int, int]):
        crop = im.crop(box)
        self._current_crop = crop
        self._original_crop = crop
        self._original_hash = hash(crop.tobytes())
        self._box = box

    def get_crop(self):
        return self._current_crop

    def get_box(self):
        return self._box

    def set_new_crop(self, crop: Image):
        self._current_crop = crop

    def check_is_ok(self):
        return self._original_hash == self.get_current_hash()

    def delete_original_crop(self):
        del self._original_crop

    def get_current_hash(self):
        return hash(self._current_crop.tobytes())

    def get_original_hash(self):
        return self._original_hash

    def get_original_crop(self):
        return self._original_crop

    def replace_from_original_crop(self, other: "Region"):
        self._current_crop = other.get_original_crop()

    def swap_with(self, other: "Region"):
        self_crop = self.get_crop()
        other_crop = other.get_crop()
        self.set_new_crop(other_crop)
        other.set_new_crop(self_crop)

    def save(self, *args, **kwargs):
        self._current_crop.save(*args, **kwargs)


class Mosaic:
    def __init__(self, out_path: str = "../out"):
        self.out_path = out_path
        self.width = None
        self.height = None
        self.cols = None
        self.rows = None
        self.col_step = None
        self.row_step = None
        self.boxes = []
        self.regions: List[Region] = []

    def init_from_image(self, im: Image, cols, rows):
        self.width = im.width
        self.height = im.height
        self.cols = max(cols, 1)
        self.rows = max(rows, 1)
        self.col_step = im.width // self.cols
        self.row_step = im.height // self.rows
        self.boxes = []
        self.regions: List[Region] = []

        self._set_boxes()
        self._set_regions(im)

    def _set_boxes(self):
        for y in range(self.cols):
            for x in range(self.rows):
                self.boxes.append(
                    (
                        x * self.col_step,
                        y * self.row_step,
                        (x + 1) * self.col_step,
                        (y + 1) * self.row_step,
                    )
                )

        return self.boxes

    def _set_regions(self, im: Image):
        for box in self.boxes:
            region = Region(im, box)
            self.regions.append(region)

    def save_regions(self):
        for index, region in enumerate(self.regions):
            region.save(f"{self.out_path}/region_{index}.png")

    def save_assembled(self):
        whole = Image.new("RGBA", (self.width, self.height))
        for region in self.regions:
            whole.paste(region.get_crop(), region.get_box())

        whole.save(f"{self.out_path}/mosaic.png")

    def shuffle_regions(self):
        total_regions = len(self.regions)
        # Cannot shuffle with less than 2 regions
        if total_regions < 2:
            return

        # Ensure total permutation to not have any already placed region
        # Random the initial swap to not have deterministic output
        first_permutation_seed = randint(1, total_regions - 1)
        remaining_spots = list(range(total_regions))
        # Make sure we don't randomly pick the seed
        remaining_spots.pop(first_permutation_seed)
        permutation_list = [first_permutation_seed]
        while len(remaining_spots) > 1:
            # Exclude current position so we have to swap every piece
            spots_to_pick_from = set(remaining_spots)
            current_position = len(permutation_list)
            spots_to_pick_from.discard(current_position)
            next_pick = choice(list(spots_to_pick_from))
            remaining_spots.remove(next_pick)
            permutation_list.append(next_pick)

        # Last region has no choice
        permutation_list.append(remaining_spots[0])
        for index, swap_to in enumerate(permutation_list):
            self.regions[index].replace_from_original_crop(self.regions[swap_to])

    def check_is_win(self):
        return all(region.check_is_ok() for region in self.regions)

    def swap_regions_from_index(self, index_1: int, index_2: int):
        check_range = range(len(self.regions))
        # Check the move is legit
        if index_1 not in check_range or index_2 not in check_range:
            raise ValueError("Position to move is out of bounds")
        self.regions[index_1].swap_with(self.regions[index_2])

    def swap_regions_from_pos(self, pos_1: Tuple[int, int], pos_2: int):
        index_1 = pos_1[0] + pos_1[1] * self.cols
        index_2 = pos_2[0] + pos_2[1] * self.cols
        self.swap_regions_from_index(index_1, index_2)

    def get_all_current_hash(self):
        return [region.get_current_hash() for region in self.regions]

    def get_all_original_hash(self):
        return [region.get_original_hash() for region in self.regions]

    def play_from_cli(self):
        logging.basicConfig(level=logging.DEBUG)
        while not self.check_is_win():
            print("------")
            logging.debug(self.get_all_original_hash())
            logging.debug(self.get_all_current_hash())
            index_1, index_2 = int(input("First index to swap : ")), int(
                input("Second index to swap : ")
            )
            self.swap_regions_from_index(index_1, index_2)
            self.save_assembled()
        print("WIN")
