import velocity
import random

# cymbals: 27 - china, 28, 29 - china, 30, 31, 49, 51 - ride, 52 - china, 53 - ride top, 55 - splash, 57,
# 60 - open hat, 63 - closed hat
openers = [28, 30, 31, 49, 57]
power_hand = [27, 29, 52, 57, 60]

half_time = False


def generate_cymbals(bar, position, file, current_power_hand):
    if bar % 4 == 0 and position == 0:
        choose_opener(bar, position, file)

    if position % 4 == 0 and not (bar % 4 == 0 and position == 0):
        file.addNote(0, 0, current_power_hand, bar * 4 + position / 4, 0.25, velocity.main_velocity())


def choose_power_hand(power_hand_change_chance, current_power_hand):
    rand = random.random()
    if rand < power_hand_change_chance:
        return random.choice(power_hand)
    else:
        return current_power_hand


def choose_opener(bar, position, file):
    available_openers = openers.copy()
    first_cymbal = random.choice(openers)
    file.addNote(0, 0, first_cymbal, bar * 4 + position / 4, 0.25, velocity.main_velocity())

    available_openers.remove(first_cymbal)

    second_cymbal = random.choice(available_openers)
    file.addNote(0, 0, second_cymbal, bar * 4 + position / 4, 0.25, velocity.main_velocity())
