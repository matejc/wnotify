from Tkinter import *
import string

# on lost focus activate timer, on gain kill timer
# or add to previous window


def notifysend(title, data):

    foreground = "white"
    background = "#000022"
    border_color = "blue"

    root = Tk()
    root.withdraw()

    def click(arg):
        root.destroy()

    window = Toplevel(bg=background, relief=FLAT, highlightcolor=border_color, highlightbackground=border_color, highlightthickness=1)
    window.overrideredirect(1)
    window.geometry("-10+10")
    window.bind("<Button-1>", click)

    dataarray = data.split("\n")
    dataarray = [s for s in dataarray if string.strip(s)]
    data_width = max([len(s) for s in dataarray])
    data_height = len(dataarray)

    label = Label(
        window,
        text=title,
        bg=background,
        fg=foreground,
        relief=FLAT,
        borderwidth=5
    )
    label.config(font=(None, 12, 'bold'))
    label.bind("<Button-1>", click)
    label.pack()

    text = Text(
        window,
        width=data_width,
        height=data_height,
        cursor="arrow",
        bg=background,
        fg=foreground,
        relief=FLAT,
        borderwidth=5
    )
    text.config(font=(None, 10))
    text.bind("<Button-1>", click)
    text.insert(INSERT, "\n".join(dataarray))
    text.config(state=DISABLED)
    text.config(highlightbackground=background)
    text.pack()

    #root.geometry("{0}x{1}-10+10".format(500, 300))
    #root.geometry("{0}x{1}-10+10".format(500, 300))
    #root.wm_attributes("-topmost", 1)
    root.mainloop()

notifysend("WeeChat", "nek text nek\n        \n\ntext\n nek text\nloooooooooooooooooooooooooooooooooooooong teeeeeeeeeeext")
