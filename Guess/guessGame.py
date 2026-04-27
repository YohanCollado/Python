import tkinter as tk
from tkinter import *
import random

win = tk.Tk()
win.geometry("700x800")
win.title("Lets Win It")


num = random.randint(1,50)

hint = StringVar()
score = IntVar()
final_score = IntVar()
guess = IntVar()


Entry(win, textvariable=guess, width=3, font=('Ubuntu', 50),
relief="groove").place(relx=0.5, rely=0.3, anchor='center')

Label(win, textvariable=hint, width=40, font=('Courier', 15),
relief="groove", bg='red').place(relx=0.5, rely=0.7, anchor='center')

Label(win, textvariable=final_score, width=2, font=('Ubuntu', 24),
relief='groove').place(relx=0.1, rely=0.2, anchor='center')

Label(win, text='Guess the number. TRY! ',
font=("Courier", 25)).place(relx=0.3, rely=0.85, anchor='center')

Label(win, text='Score out of 5', font=("Courier",
25)).place(relx=0.3, rely=0.7, anchor='center')

hint.set("GUESS # 1 to 50")
score.set(5)

final_score.set(score.get())


def fun():
    x = guess.get()
    final_score.set(score.get())

    if score.get() > 0:

        if x > 50 or x < 0:
            hint.set("You just lost 1 chance, NUMBER NEEDS TO BE FROM 0 - 100")
            score.set(score.get() - 1)
            final_score.set(score.get())

        elif num == x:
            hint.set("Congratulations you have won")
            score.set(score.get() - 1)
            final_score.set(score.get())

        elif num > x:
            hint.set("Guess a higher number")

            score.set(score.get() -1)
            final_score.set(score.get())

        elif num < x:
            hint.set("Guess a lower number")

            score.set(score.get() -1)
            final_score.set(score.get())
    else:
        hint.set("game over you lost")


Button(win, width=8, text='CHECK', font=('Courier', 25),
command=fun, relief='groove', bg='light blue').place(relx=0.5, rely=0.5, anchor='center')
win.mainloop()