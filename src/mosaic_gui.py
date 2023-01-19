from tkinter import *
from tkinter import ttk


class MosaicGUI:
    def __init__(
        self, root: Tk, base_image_path: str = "../assets/daemon.png", listener=None
    ):
        root.title("Play mosaic!")
        self.listener = listener
        self.base_image_path = base_image_path

        # Create main frame
        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Create input buttons
        self.cols = IntVar(value=2)
        cols_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.cols)
        cols_entry.grid(column=2, row=1, sticky=(W, E))
        cols_label = ttk.Label(self.mainframe, text="Columns")
        cols_label.grid(column=1, row=1, sticky=(W, E))

        self.rows = IntVar(value=2)
        rows_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.rows)
        rows_entry.grid(column=2, row=2, sticky=(W, E))
        rows_label = ttk.Label(self.mainframe, text="Rows")
        rows_label.grid(column=1, row=2, sticky=(W, E))

        # Create shuffle elements
        shuffle_button = ttk.Button(
            self.mainframe, text="Shuffle", command=self.shuffle
        )
        shuffle_button.grid(column=1, row=3)

        self.base_image = PhotoImage(file=base_image_path)
        self.canvas = Canvas(
            self.mainframe,
            width=500,
            height=500,
        )
        self.canvas.grid(column=1, row=4)
        self.canvas.create_image(0, 0, anchor=NW, image=self.base_image)
        self.canvas.image = self.base_image

        # Conveniency
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        cols_entry.focus()
        root.bind("<Return>", self.shuffle)

    def get_rows(self):
        return self.rows.get()

    def get_cols(self):
        return self.cols.get()

    def shuffle(self, *args):
        if self.listener is not None:
            self.listener.shuffle()

    def set_image(self, filepath):
        self.base_image = PhotoImage(file=filepath)
        new_im = self.canvas.create_image(0, 0, anchor=NW, image=self.base_image)
        self.canvas.image = self.base_image


if __name__ == "__main__":
    root = Tk()
    gui = MosaicGUI(root)
    root.mainloop()
