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
               font=("Ariel", 15), command=self.reset).grid(row=0, column=1) # button to reset game, need to add command after
        
        self.pieces = set()
        self.selected_piece = None
        self.piece_position = {}

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

        red_crown = Image.open("Checkers/Images/redCrown.png")
        black_crown = Image.open("Checkers/Images/blackCrown.png")

        red = red.resize((size, size))
        black = black.resize((size, size))
        
        red_crown = red_crown.resize((size, size))
        black_crown = black_crown.resize((size, size))

        self.red_piece = ImageTk.PhotoImage(red)
        self.black_piece = ImageTk.PhotoImage(black)

        self.red_crown_piece = ImageTk.PhotoImage(red_crown)
        self.black_crown_piece = ImageTk.PhotoImage(black_crown)

    def draw_piece(self, row, column, image):
        square_size = 80
        x = column * square_size + square_size // 2
        y = row *square_size + square_size // 2

        piece_id = self.canvas.create_image(x, y, image=image)

        self.pieces.add(piece_id)
        self.piece_position[piece_id] = (row, column)

        return piece_id


    def set_piece(self): 
        self.board_state = [[None for _ in range(8)] for _ in range(8)]

        for row in range(3):
            for column in range(8):
                if (row + column) % 2 == 1:
                    self.draw_piece(row, column, self.red_piece)
                    self.board_state[row][column] = "R"
        for row in range(5, 8):
            for column in range(8):
                if (row + column) % 2 == 1:
                    self.draw_piece(row, column, self.black_piece)
                    self.board_state[row][column] = "B"
    

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
                print("Piece selected")
            return 
        if clicked_id in self.pieces:
            self.selected_piece = clicked_id
            print("Piece changed")
            return 

        old_row, old_col = self.piece_position[self.selected_piece]
        piece = self.board_state[old_row][old_col]

        

        if self.is_valid_move(piece, old_row, old_col, row, col):

            x = col * 80 + 40
            y = row * 80 + 40

            print("Selected piece moved")
        

            self.canvas.coords(self.selected_piece, x, y)

            self.board_state[old_row][old_col] = None
            self.board_state[row][col] = piece
            self.piece_position[self.selected_piece] = (row, col)

            self.is_crown()

            self.selected_piece = None
        


    def reset(self):
        for piece_id in self.pieces:
            self.canvas.delete(piece_id)

        self.pieces.clear()
        self.selected_piece = None
        
        self.set_piece()

        print("Game was reset")

        
    def is_valid_move(self, piece, old_row, old_col, new_row, new_col):

        if new_row < 0 or new_row >= 8 or new_col < 0 or new_col >= 8:
            return False

        if self.board_state[new_row][new_col] is not None:
            return False

        if (new_row + new_col) % 2 == 0:
            return False
        
        row_difference = new_row - old_row
        column_difference = abs(new_col - old_col)

        if piece == "R":
            return row_difference == 1 and column_difference == 1
        
        if piece == "B":
            return row_difference == -1 and column_difference == 1
        
        return False


    def is_crown(self):

        if self.selected_piece is None:
            return 
        position = self.piece_position.get(self.selected_piece)
        if position is None:
            return
        
        row = position
        col = position

        piece = self.board_state[row][col]

        if piece == "R" and row == 7:
            #remove old piece image
            old_id = self.selected_piece
            self.canvas.delete(old_id)
            self.pieces.discard(old_id)
            self.piece_position.pop(old_id, None)

            self.board_state[row][col] = "RC"
            new_id = self.draw_piece(row, col, self.red_crown_piece)

            self.selected_piece = new_id
            print(f"Red Crown was set at position {row}, {col}")

        elif piece == "B" and row == 0:
            old_id = self.selected_piece
            self.canvas.delete(old_id)
            self.pieces.discard(old_id)
            self.piece_position.pop(old_id, None)

            self.board_state[row][col] = "BC"
            new_id = self.draw_piece(row, col, self.black_crown_piece)

            self.selected_piece = new_id
            print(f"Black Crown was set at position {row}, {col}")
        
        #if self.board_state[row][col] == "R" and row == 7:
         #   self.board_state[row][col] = "RC"
          #  self.draw_piece(row, col, self.red_crown_piece)
           # print(f"Red crown was set at position {row}, {col}")
        #elif self.board_state[row][col] == "B" and row == 0:
         #   self.board_state[row][col] = "BC"
          #  self.draw_piece(row, col, self.black_crown_piece)
           # print(f"Black Crown was set at position {row}, {col}")
        


    #def eat(self):
    #def multiple_eat(self):
    #def promote(self):
    #def move_crown(self):
    #def crown_eat(self):
    #def crown_multiple_eat(self):

if __name__ == "__main__": # makes code run
    app = Checkers() # creates window, triggers, __init__
    app.mainloop() #starts the GUI()