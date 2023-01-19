import os, sys
from PIL import Image


def main():
    dest_format = "." + sys.argv[1]

    files_to_convert = sys.argv[2:]

    if not files_to_convert:
        print("No file provided !")
        return

    for filename in files_to_convert:
        print(f"---Converting {filename}---")
        basename, extension = os.path.splitext(filename)
        if extension == dest_format:
            print("\tFile already has the desired format !")
            continue
        with Image.open(filename) as im:
            new_name = f"{basename}{dest_format}"
            try:
                im.save(new_name)
                print(f"\tSaved as {new_name}")
            except OSError:
                print("\tCouldn't convert file")


if __name__ == "__main__":
    main()
    print("Exiting...")
