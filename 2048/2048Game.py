from tkinter import *
import random

class Play_2048(Tk):
    def __init__(self):
        super().__init__()

        self.title("2048 Game")
        self.minsize(430, 470)

        self.score = 0
        self.high_score = 0

        self.game_score = StringVar(value="0")
        self.highest_score = StringVar(value="0")

        top = Frame(self)
        top.pack(side="top")

        Button(top, text="New Game", font=("Arial", 15), command=self.new_game).grid(row=0, column=0)
        Label(top, text="Score:", font=("Arial", 15)).grid(row=0, column=1)
        Label(top, textvariable=self.game_score, font=("Arial", 15)).grid(row=0, column=2)
        Label(top, text="Record:", font=("Arial", 15)).grid(row=0, column=3)
        Label(top, textvariable=self.highest_score, font=("Arial", 15)).grid(row=0, column=4)

        self.canvas = Canvas(self, width=420, height=420, borderwidth=5, highlightthickness=0)
        self.canvas.pack(side="top")

        self.bind_all("<Key>", self.moves)

        self.new_game()

    def new_game(self):
        self.score = 0
        self.game_score.set("0")
        self.game_board = [[0 for _ in range(4)] for _ in range(4)]

        self.add_tile()
        self.add_tile()
        self.show_board()

    def full(self):
        for row in self.game_board:
            if 0 in row:
                return False
        return True

    def add_tile(self):
        if self.full():
            return

        while True:
            row = random.randint(0, 3)
            col = random.randint(0, 3)

            if self.game_board[row][col] == 0:
                self.game_board[row][col] = random.choice([2, 2, 2, 2, 4])
                break

    def show_board(self):
        self.canvas.delete("all")

        bg_color = {
            0: "#f5f5f5",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#edc850",
            16: "#edc53f",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#f2b179",
            1024: "#f59563",
            2048: "#edc22e",
        }

        text_color = {
            2: "#776e65",
            4: "#776e65",
            8: "#f9f6f2",
            16: "#f9f6f2",
            32: "#f9f6f2",
            64: "#f9f6f2",
            128: "#f9f6f2",
            256: "#f9f6f2",
            512: "#f9f6f2",
            1024: "#f9f6f2",
            2048: "#f9f6f2",
        }

        cell = 105

        for row in range(4):
            for col in range(4):
                x1 = col * cell
                y1 = row * cell
                x2 = x1 + cell - 5
                y2 = y1 + cell - 5

                num = self.game_board[row][col]

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=bg_color.get(num, "#3c3a32"),
                    outline=""
                )

                if num != 0:
                    self.canvas.create_text(
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        text=str(num),
                        font=("Arial", 32, "bold"),
                        fill=text_color.get(num, "#f9f6f2")
                    )

    def compress(self, row):
        new_row = [num for num in row if num != 0]

        while len(new_row) < 4:
            new_row.append(0)

        return new_row

    def merge(self, row):
        for i in range(3):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0

        return row

    def move_left(self):
        old_board = [row[:] for row in self.game_board]

        for i in range(4):
            row = self.compress(self.game_board[i])
            row = self.merge(row)
            row = self.compress(row)
            self.game_board[i] = row

        return old_board != self.game_board

    def move_right(self):
        old_board = [row[:] for row in self.game_board]

        for i in range(4):
            row = list(reversed(self.game_board[i]))
            row = self.compress(row)
            row = self.merge(row)
            row = self.compress(row)
            self.game_board[i] = list(reversed(row))

        return old_board != self.game_board

    def move_up(self):
        old_board = [row[:] for row in self.game_board]

        for col in range(4):
            column = [self.game_board[row][col] for row in range(4)]
            column = self.compress(column)
            column = self.merge(column)
            column = self.compress(column)

            for row in range(4):
                self.game_board[row][col] = column[row]

        return old_board != self.game_board

    def move_down(self):
        old_board = [row[:] for row in self.game_board]

        for col in range(4):
            column = [self.game_board[row][col] for row in range(4)]
            column.reverse()
            column = self.compress(column)
            column = self.merge(column)
            column = self.compress(column)
            column.reverse()

            for row in range(4):
                self.game_board[row][col] = column[row]

        return old_board != self.game_board

    def moves(self, event):
        moved = False

        if event.keysym == "Left":
            moved = self.move_left()
        elif event.keysym == "Right":
            moved = self.move_right()
        elif event.keysym == "Up":
            moved = self.move_up()
        elif event.keysym == "Down":
            moved = self.move_down()

        if moved:
            self.add_tile()
            self.game_score.set(str(self.score))

            if self.score > self.high_score:
                self.high_score = self.score
                self.highest_score.set(str(self.high_score))

            self.show_board()
            self.game_over()

    def game_over(self):
        if any(2048 in row for row in self.game_board):
            self.canvas.create_text(210, 210, text="YOU WON!", font=("Arial", 40, "bold"), fill="green")
            return True

        if not self.full():
            return False

        for row in range(4):
            for col in range(3):
                if self.game_board[row][col] == self.game_board[row][col + 1]:
                    return False

        for col in range(4):
            for row in range(3):
                if self.game_board[row][col] == self.game_board[row + 1][col]:
                    return False

        self.canvas.create_text(210, 210, text="GAME OVER", font=("Arial", 40, "bold"), fill="red")
        return True


if __name__ == "__main__":
    app = Play_2048()
    app.mainloop()