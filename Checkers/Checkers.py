from tkinter import * # imports everything from libary 
from PIL import Image, ImageTk

class Checkers(Tk): # creating a class called checkers that inherets from TK
    def __init__(self): # runs when create Checkers()
        super().__init__() # calls parent tk constructor
        
        self.title("Checkers")
        self.minsize(640, 640) # stay at this size usually

        top = Frame(self) # creates containers
        top.pack(side="top") # sets that container to top

        Button(top, 
               text="Reset", 
               font=("Ariel", 15)).grid(row=0, column=1) # button to reset game, need to add command after
        
        self.pieces = set()
        self.selected_piece = None
        self.board() # this is what draws the board, without this the window is just blank
        self.image_piece()
        self.set_piece()

    def board(self): # method to make board
        rows = 8 
        columns = 8
        square_size = 80 # each square on the board is of 80 pixels

        white = "#FFFFFF" # white color
        black = "#4B4B4B" # black color for board

        self.canvas = Canvas( # creates a canvas (area to create), attached to self which is the main window
            self,
            width = columns * square_size, # the width is 8 * 860 which is 640
            height = rows * square_size # same for height
        )
        self.canvas.pack() # displays the canvas in the window

        for row in range(rows): # loops through the rows
            for column in range(columns): # loops through columns
                x1 = column * square_size
                y1 = row * square_size
                x2 = x1 + square_size
                y2 = y1 + square_size

                if (row + column) % 2 == 0: # displays the color
                    color = white
                else:
                    color = black
                
                self.canvas.create_rectangle( # draws a rectangle in the canvas and fills colors
                    x1, y1, x2, y2, 
                    fill=color, 
                    outline=color)
                
                self.canvas.bind("<Button-1>", self.move_piece)
                
    def image_piece(self):    
        
        size = 80

        red = Image.open("Checkers/Images/red.png")
        black = Image.open("Checkers/Images/black.png")

        red = red.resize((size, size))
        black = black.resize((size, size))

        self.red_piece = ImageTk.PhotoImage(red)
        self.black_piece = ImageTk.PhotoImage(black)

    def draw_piece(self, row, column, image):
        square_size = 80
        x = column * square_size + square_size // 2
        y = row *square_size + square_size // 2

        piece_id = self.canvas.create_image(x, y, image=image)

        self.pieces.add(piece_id)


    def set_piece(self): 
        for row in range(3):
            for column in range(8):
                if (row + column) % 2 == 1:
                    self.draw_piece(row, column, self.red_piece)
        for row in range(5, 8):
            for column in range(8):
                if (row + column) % 2 == 1:
                    self.draw_piece(row, column, self.black_piece)
    

    def move_piece(self, event):
        row = event.y // 80
        col = event.x // 80

        clicked = self.canvas.find_closest(event.x, event.y)

        if not clicked:
            return
        
        clicked_id = clicked[0]

        if self.selected_piece is None:
            if clicked_id in self.pieces:
                self.selected_piece = clicked_id
                print(f"Selected piece at row {row}, col {col}")
        else:
            x = col * 80 * 40
            y = row * 80 * 40

            self.canvas.coords(self.selected_piece, x, y)

            print(f"Moved piece to row {row}, col {col}")
            
            self.selected_piece = None


    








if __name__ == "__main__": # makes code run
    app = Checkers() # creates window, triggers, __init__
    app.mainloop() #starts the GUI()