# on lost focus activate timer, on gain kill timer
# or add to previous window
# choose color

import Tkinter
import string
import threading


class Notification:

    N_BLUE = ("white", "#000022", "blue")
    N_GREEN = ("white", "#002200", "green")

    class LifeThread(threading.Thread):
        def __init__(
                self,
                parent,
                title,
                data,
                colors,
                size_heading,
                size_text
        ):
            threading.Thread.__init__(self)
            self.end = False
            self.parent = parent
            self.title = title
            self.data = data
            self.colors = colors
            self.size_heading = size_heading
            self.size_text = size_text
            self.daemon = True
            self.start()

        def __del__(self):
            self.end = True

        def run(self):
            self._notify()

        def _notify(self):
            self.root = Tkinter.Tk()
            self.root.withdraw()

            def click(arg):
                self.window.withdraw()

            self.window = Tkinter.Toplevel(
                relief=Tkinter.FLAT,
                highlightthickness=1
            )
            self.window.overrideredirect(1)
            self.window.geometry("-10+10")
            self.window.bind("<Button-1>", click)

            self.label = Tkinter.Label(
                self.window,
                relief=Tkinter.FLAT,
                borderwidth=5
            )
            self.label.bind("<Button-1>", click)
            self.label.pack()

            self.text = Tkinter.Text(
                self.window,
                cursor="arrow",
                relief=Tkinter.FLAT,
                borderwidth=5,
                highlightthickness=0,
                highlightbackground=self.colors[1]
            )
            self.text.bind("<Button-1>", click)
            self.text.pack()

            self.change_notification(self.title, self.data, self.colors, self.size_heading, self.size_text)

            self.root.mainloop()
            self.end = True

        def change_notification(self, title, data, colors, size_heading, size_text):
            self.title = title
            self.data = data
            if colors:
                self.colors = colors
            else:
                self.colors = self.parent.N_BLUE

            self.size_heading = size_heading
            self.size_text = size_text

            self.label['text'] = self.title
            self.label['fg'] = self.colors[0]
            self.label['bg'] = self.colors[1]
            self.label.config(font=(None, self.size_heading, 'bold'))

            self.text['fg'] = self.colors[0]
            self.text['bg'] = self.colors[1]
            dataarray = self.data.split("\n")
            dataarray = [s[:100] for s in dataarray if string.strip(s)]
            data_width = max([len(s) for s in dataarray])
            data_height = len(dataarray)
            self.text.config(state=Tkinter.NORMAL)
            self.text.delete(1.0, Tkinter.END)
            self.text.insert(Tkinter.END, "\n".join(dataarray))
            self.text.config(state=Tkinter.DISABLED)
            self.text['width'] = data_width
            self.text['height'] = data_height
            self.text.config(font=(None, self.size_text))

            self.window['bg'] = self.colors[1]
            self.window['highlightbackground'] = self.colors[2]
            self.window['highlightcolor'] = self.colors[2]

            self.window.deiconify()

    def is_alive(self):
        return hasattr(self, "life") and self.life and not self.life.end

    def notify(self, title, data, colors=None, size_heading=9, size_text=8):
        if self.is_alive():
            self.life.change_notification(
                title,
                data,
                colors,
                size_heading,
                size_text
            )
        else:
            self.life = Notification.LifeThread(
                self,
                title,
                data,
                colors,
                size_heading,
                size_text
            )

    def show(self):
        self.life.window.deiconify()

    def hide(self):
        self.life.window.withdraw()
