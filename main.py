#!python3.7
import time
import tkinter as tk
from PIL import Image, ImageTk
geography = input("What country do you want to play?")
if geography == "US":
    from us_constants import *
elif geography == "Mexico":
    from mexico_constants import *
elif geography == "Brazil":
    from br_constants import *
else:
    exit("Unknown country!")


class MapGame:
    def __init__(self):
        self.window = tk.Tk()
        self.image = ImageTk.PhotoImage(Image.open(INITIAL_MAP).resize((800, 400)))
        self.map_picture = tk.Label(image=self.image)
        self.question = tk.Label(text="Blah")
        self.start_game(None)
        self.yes_button = tk.Button(text="Yes", width=25, height=5, bg="blue", fg="yellow")
        self.yes_button.bind("<Button-1>", self.yes_func)
        self.no_button = tk.Button(text="No",  width=25, height=5, bg="red",  fg="yellow")
        self.no_button.bind("<Button-1>", self.no_func)
        self.start_over_button = tk.Button(text="Start Over", width=25, height=5, bg="green", fg="yellow")
        self.start_over_button.bind("<Button-1>", self.start_game)
        self.map_picture.pack()
        self.question.pack()
        self.yes_button.pack()
        self.no_button.pack()
        self.start_over_button.pack()
        self.window.mainloop()

    def start_game(self, event):
        print("Starting Game... " + geography)
        self.score = 0
        self.rounds_left = MAX_ROUNDS
        self.game_over = False
        self.image = ImageTk.PhotoImage(Image.open(INITIAL_MAP).resize((MAP_WIDTH, MAP_HEIGHT)))
        self.map_picture.configure(image=self.image)
        response = "Can you find the " + AREA_DESCRIPTOR + " where you were born in on the map?"
        self.question.configure(text=response)

    def yes_func(self, event):
        if self.game_over:
            self.start_game(None)
        if self.rounds_left == MAX_ROUNDS:
            self.update_round()
        elif self.rounds_left >= 0:
            self.score += 2**(self.rounds_left)
            self.update_round()

    def no_func(self, event):
        if self.rounds_left == MAX_ROUNDS:
            self.question.configure(text="FIXME: We are going to have a very difficult time then...")
            time.sleep(5)
            exit()
        if self.game_over:
            time.sleep(5)
            exit()
        self.update_round()

    def game_end(self):
        if self.score in score_to_state:
            response = "I think your " + AREA_DESCRIPTOR + " is " + score_to_state[self.score]
        else:
            response = "You gave me bad input"
        response += "....   Would you like to play again?"
        self.question.configure(text=response)
        self.game_over = True

    def update_round(self):
        print(f"Score: {self.score} Rounds Left: {self.rounds_left}")
        if self.rounds_left == 0:
            self.game_end()
        else:
            self.rounds_left -= 1
            self.update_image()

    def update_image(self):
        self.new_image = ImageTk.PhotoImage(Image.open(self.round_to_image_file()).resize((MAP_WIDTH, MAP_HEIGHT)))
        self.map_picture.configure(image=self.new_image)
        self.question.configure(text="Is your " + AREA_DESCRIPTOR + " in " + HIGHLIGHT_COLOR)

    def round_to_image_file(self):
        filepath = MAP_DIRECTORY + "/" + MAP_FILENAME_PREFIX + str(2**(self.rounds_left)) + ".jpg"
        return filepath


if __name__ == "__main__":
    MapGame()


