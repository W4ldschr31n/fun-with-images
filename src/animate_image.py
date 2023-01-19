from tkinter import *
from tkinter import ttk


def drop():
    x, y = canvas.coords(moving_image)
    drop_button.configure(state=DISABLED)
    if y < 500:
        canvas.move(moving_image, 0, 10)
        canvas.after(10, drop)
    else:
        drop_button.configure(command=lift)
        drop_button.configure(state=NORMAL)


def lift():
    x, y = canvas.coords(moving_image)
    drop_button.configure(state=DISABLED)
    if y > 0:
        canvas.move(moving_image, 0, -10)
        canvas.after(10, lift)
    else:
        drop_button.configure(command=drop)
        drop_button.configure(state=NORMAL)


root = Tk()

# Create main frame
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

drop_button = ttk.Button(mainframe, text="Drop", command=drop)
drop_button.grid(column=1, row=1)

base_image = PhotoImage(file="../out/corner_0.png")
canvas = Canvas(
    mainframe,
    width=500,
    height=500,
)
canvas.grid(column=1, row=2)
current_x = 0
current_y = 0
moving_image = canvas.create_image(current_x, current_y, anchor=NW, image=base_image)

root.mainloop()
