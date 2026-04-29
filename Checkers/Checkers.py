from tkinter import *

class Checkers(Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Checkers")
        self.minsize(500, 500)

        top = Frame(self)
        top.pack(side="top")

        Button(top, text="Reset", font=("Aril", 15)).grid(row=0, column=1)

if __name__ == "__main__":
    app = Checkers()
    app.mainloop()