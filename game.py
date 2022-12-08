import random
import itertools
import time
"""
SNAKES AND LADDERS GAME
Created 01.12.2022
RULE:
A player will enter the game only if they get 1 on the dice.
After that, if the player gets the number n in the dice, they move forward n boxes
If there is a ladder in the square the player is currently in, they move to the square where the ladder ends
If there is a snake in the square the player is currently in, they move to the square with the tail of the snake.
"""

# Snakes and ladders have been separated to create individual snakes and ladders for the player to interact with

ladders = {"ladder1": [27, 35, 39, 50], "ladder2": [59, 66, 73, 76],
           "ladder3": [89, 97, 99, 2], "ladder4": [8, 22, 28, 30], "ladder5": [44, 54, 70, 80, 87]}

snakes = {"snake1": [7, 5, 3, 34], "snake2": [46, 24, 12, 63],
          "snake3": [67, 86, 26, 23], "snake4": [29, 41, 77, 32], "snake5": [58, 69, 90, 83, 93]}


class Dice:

    # Since all the players will use the same dice to play, there does not need to be more than one die,
    # so Dice is made static.
    @staticmethod
    def roll():
        return random.randint(1, 6)


class Player:
    def __init__(self, name):
        self.name = name[0].capitalize()
        self.position = 0
        self.penalty = 0
        # Initially, the player is not playing (meaning she will remain at position 0 till dice shows 1
        self.playing = True
        self.tails = [34, 63, 23, 32, 93]

        # Store the last three consecutive moves, we will use this later to check if it equals [6,6,6]
        self.last_three_moves = [0, 0, 0]

        # if the player lands on a square corresponding to a snake or ladder,
        # they get a random comment in relation to their progress

    def has_won(self):
        winner = "Congratulations superhero! You have won!!!!!"
        if self.position == 100:
            print(winner)
            self.playing = False
            return True
        else:
            return False
    # if a player reaches the 100th square, they will receive the above message and win

    def update_position(self, dice_value):
        # the following two lines will remove the first element then add the latest dice_value to the list
        self.last_three_moves.pop(0)
        self.last_three_moves.append(dice_value)
        new_pos = self.position + dice_value

        # if player rolls three 6's on the dice, last element is removed and the game continues,
        # otherwise nothing changes

        if self.last_three_moves == [6, 6, 6]:
            self.last_three_moves.pop()

        else:
            self.position = new_pos
        # if the player rolls a number on the dice greater than 100,
        # they move back the number of positions they just rolled that is less than 100
        if self.position > 100:
            self.penalty = 0
            self.penalty += dice_value
            self.position -= self.penalty
            print(f'Your dice roll was greater than 100. You have to go {self.penalty} squares back')

        # if the new position has a snake or ladder, their position will be updated depending on what square they are in
        if self.position in snakes:
            self.position = snakes[self.position]
        if self.position in ladders:
            self.position = ladders[self.position]
        # if the player reaches a square corresponding to a part of the snake
        # (except if they encounter a square that forms one of the tails of the snakes)
        # then they move back the corresponding number of squares to the length of that snake
        # if the player encounters a ladder, they move the number of squares corresponding to the length of the ladder
        commentator_snakes = {"Injury": "Ouch! Looks like a snake bit you. That must have hurt",
                              "Training": "You need more training young Padawan, "
                                          "greater challenges await you in the future",
                              "Teasing": "Did you feel that? Looks like that snake just gave you a love bite",
                              "Loud": "SSSSSSSSSSSSSSSSS, looks like you caught yourself an aggressive one there!"}
        snake_comments = random.choice(list(commentator_snakes.values()))
        for i in range(len(snakes)):
            if self.position in snakes:
                self.position -= len(snakes[i])
                print(f'You reached a snake. You go {len(snakes[i])} squares down')
                print(snake_comments)

        else:
            if snakes in self.tails:
                self.position += 0
                print("You reached the tail of the snake. You must stay where you are!")
        commentator_ladders = {"Celebration": "Whee eeee! You're moving up in the world!",
                               "Idea": "You seem like a whiz at this, maybe your dreams are coming true!",
                               "Wonder": "Can you believe it? You may actually win this race!",
                               "Awe": "Looks like you are the champion of the world, as Queen would say!"}
        ladder_comments = random.choice(list(commentator_ladders.values()))
        for i in range(len(ladders)):
            if self.position in ladders:
                self.position += len(ladders[i])
                print(f'You reached a ladder. You go {len(ladders[i])} squares up')
                print(ladder_comments)

    def print_position(self):
        print(self.name, "Your position is....==>", str(self.position))

    def play(self):
        dice_value = Dice.roll()
        print(self.name + ": The dice shows a value of... " + str(dice_value))

        if dice_value >= 1:
            self.playing = True

        if not self.playing:
            print(self.name + ": tough luck hotshot, you missed out on this high-stakes game")
        else:

            # lets the player know where they currently are on the board and what position they are
            while True:
                self.update_position(dice_value)
                self.print_position()
                # if dice_value is not 6, their turn is finished
                if dice_value != 6:
                    break
                # else roll the dice again
                else:
                    dice_value = Dice.roll()


class SnakesAndLadders:
    def __init__(self, players):
        self.players = itertools.cycle(players)
        self.num_players = len(players)

        # This list is created so that we can check if any players have won and determine their progress
        self.mutable_players = itertools.cycle(players)

    def has_finished(self):
        # if any of the players has won, the game is finished
        for i in range(self.num_players):
            player = next(self.mutable_players)
            if player.has_won():
                return True
            return False

    def next_player(self):
        return next(self.players)


if __name__ == "__main__":
    try:
        no_of_players = int(input("Enter the no of players:"))
    except ValueError:
        print("Only numbers are allowed")
    player_names = [name for name in input("Enter the name of players:").split()]
    players = [Player(name) for name in player_names]
    game = SnakesAndLadders(players)

    while not game.has_finished():
        player = game.next_player()
        player.play()
        time.sleep(5)
