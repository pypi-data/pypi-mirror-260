# Import the required libraries
import threading
import tkthread
tkthread.patch()

from time import sleep
from tkinter import *  # pylint: disable=unused-wildcard-import, wildcard-import


class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)


class WindowHelper:
    def __init__(self):
        # Create an instance of tkinter frame or window
        self.win = Tk()

        # Set the size of the window
        self.win.geometry("700x350")

        # Remove the Title bar of the window
        self.win.overrideredirect(True)

        self.win.lift()
        self.win.attributes("-topmost", True)
        self.win.focus_force()

        self.x_offset, self.y_offset = 0, 0

        self.win.bind("<B1-Motion>", self.move_window)
        self.win.bind("<Button-1>", self.store_window)

        self.canvas = ResizingCanvas(self.win ,width=700, height=350, bg="black", highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=YES)

        self.img = PhotoImage(width=700, height=350)
        self.canvas.create_image((700, 350), image=self.img, state="normal")


    def setPixel(self, x, y, *, rgb: tuple | None = None, hexstr: str | None = None):
        if rgb is not None and hexstr is not None:
            raise ValueError("Only one of rgb or hexstr can be specified")
        if rgb is None and hexstr is None:
            raise ValueError("One of rgb or hexstr must be specified")

        if rgb is not None:
            hexstr = "#%02x%02x%02x" % rgb
        self.img.put(hexstr, (x, y))


    def store_window(self, e):
        self.x_offset = e.x
        self.y_offset = e.y


    @property
    def window_size(self):
        return tuple(map(int, self.win.winfo_geometry().split("+")[0].split("x")))

    def move_mouse_button(self, e):
        y_size = int(self.win.winfo_geometry().split("+")[0].split("x")[1])
        x_size = int(self.win.winfo_geometry().split("+")[0].split("x")[0])
        y1 = self.win.winfo_pointery()-self.win.winfo_rooty()
        x1 = self.win.winfo_pointerx()-self.win.winfo_rootx()

        if y1 >= y_size - (y_size * 0.2) and x1 >= x_size - (x_size * 0.2):
            x1 = self.win.winfo_pointerx()
            y1 = self.win.winfo_pointery()
            x0 = self.win.winfo_rootx()
            y0 = self.win.winfo_rooty()

            x_size = max((x1-x0), 200)
            y_size = max((y1-y0), 100)


            self.win.geometry("%sx%s" % (x_size,y_size))


    def move_window(self, e):
        y1 = self.win.winfo_pointery()-self.win.winfo_rooty()
        y_size = int(self.win.winfo_geometry().split("+")[0].split("x")[1])

        if self.y_offset <= (y_size * 0.2):
            x1, y1 = self.win.winfo_pointerxy()

            xSet = max(x1-self.x_offset, 200)
            ySet = max(y1-self.y_offset, 100)

            self.win.geometry("+%s+%s" % (xSet,ySet))
        self.move_mouse_button(e)

    def start(self):
        self.win.mainloop()


