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

# Snakes and ladders do basically the same thing, they take the player to another square. I put them
# here together, so it would be easier to check later.

ladders = [27, 35, 39, 50, 59, 66, 73, 76, 89, 97, 99, 2, 8, 22, 28, 30, 44, 54, 70, 80, 87]

snakes = [7, 5, 3, 34, 46, 24, 12, 63, 67, 86, 26, 23, 29, 41, 77, 32, 58, 69, 90, 83, 93]
class Dice:

    # Since all the players will use the same dice to play, there need not be more than one instances of dice
    # So, it is better if Dice is made static.
    @staticmethod
    def roll():
        return random.randint(1, 6)


class Player:
    def __init__(self, name):
        self.name = name[0].capitalize()
        self.position = 0

        # Initially, the player is not playing (meaning she will remain at position 0 till dice shows 1
        self.play = False

        # Store the last three consecutive moves, we will use this later to check if it equals [6,6,6]
        self.last_three_moves = [0, 0, 0]

    def has_won(self):
        # If position = 100, player has won
        return self.position == 100

    def update_position(self, dice_value):

        # the following two lines will pop one element(zeroth index element) from the list,
        # and add the latest dice_value to the list
        # so that the list will be updated
        self.last_three_moves.pop(0)
        self.last_three_moves.append(dice_value)

        if self.last_three_moves == [6, 6, 6]:
            self.position = 0
            self.play = False
            return

        new_pos = self.position + dice_value

        # if new position exceeds 100, don't update the current position
        # instead, return
        if new_pos >= 100:
            return
        else:
            self.position = new_pos

        # if the new position has a snake or ladder, update the position after snake or ladder
        while self.position in snakes or ladders:
            self.position = snakes[self.position] or ladders[self.position]

    def print_position(self):
        print(self.name, "Your position is....==>", str(self.position))

    def play(self):
        dice_value = Dice.roll()
        print(self.name + ": The dice shows a value of... " + str(dice_value))

        if dice_value == 1:
            self.play = True

        if not self.play:
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
class Commentator:
    def __init__(self, commentator):
        self.commentator = commentator
    def commentate(self):
        if player.print_position() in snakes:



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
    no_of_players = int(input("Enter the no of player:"))
    player_names = [name for name in input("Enter the name of players:").split()]
    players = [Player(name) for name in player_names]
    game = SnakesAndLadders(players)

    while not game.has_finished():
        player = game.next_player()
        player.play()
        time.sleep(5)
