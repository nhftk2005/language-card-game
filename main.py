from tkinter import *
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}
current_card = {}

try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/hebrew_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(title_text, text="English", fill="black")
    canvas.itemconfig(word_text, text=current_card["English"], fill="black")
    canvas.itemconfig(canvas_img, image=card_front_img)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(title_text, text="Hebrew", fill="white")
    canvas.itemconfig(word_text, text=current_card["Hebrew"], fill="white")
    canvas.itemconfig(canvas_img, image=card_back_img)


def is_know():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
canvas_img = canvas.create_image(400, 263, image=card_front_img)
title_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(column=1, row=1, columnspan=2)


# Buttons
wrong_sing_image = PhotoImage(file="./images/wrong.png")
wrong_sing_button = Button(image=wrong_sing_image, highlightthickness=0, borderwidth=0, command=next_card)
wrong_sing_button.grid(column=1, row=2)

right_sing_image = PhotoImage(file="./images/right.png")
check_image_button = Button(image=right_sing_image, highlightthickness=0, borderwidth=0, command=is_know)
check_image_button.grid(column=2, row=2)

next_card()

window.mainloop()
