import velocity
import random

# cymbals: 27 - china, 28, 29 - china, 30, 31, 49, 51 - ride, 52 - china, 53 - ride top, 55 - splash, 57,
# 60 - open hat, 63 - closed hat
# MyMIDI.addNote(track,channel,pitch,position,duration,volume)
openers = [28, 30, 31, 49, 57]
power_hand = [27, 29, 52, 57, 60]


def generate_cymbals(number_of_bars, file):
    bar = 0
    for _ in range(number_of_bars):
        if bar % 8 == 0:
            file.addNote(0, 0, 49, bar * 4, 0.25, velocity.main_velocity())
            file.addNote(0, 0, 57, bar * 4, 0.25, velocity.main_velocity())

        position = 0
        while position < 4:
            if bar % 8 != 0 or position != 0:
                file.addNote(0, 0, 52, bar * 4 + position, 0.25, velocity.main_velocity())
            position += 2

        bar += 1
