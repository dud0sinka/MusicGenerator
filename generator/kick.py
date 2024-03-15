import velocity
import random


def generate_kick(bar, position, file):
    gallop_before_snare = 0.35
    random_gallop = 0.25

    if position % 2 == 0:
        file.addNote(0, 0, 36, bar * 4 + position / 4, 0.25, velocity.main_velocity())

        rand = random.random()
        if rand < random_gallop:
            file.addNote(0, 0, 36, bar * 4 + position / 4 + 0.25, 0.25, velocity.main_velocity())

        rand = random.random()
        if rand < gallop_before_snare and position == 8:
            file.addNote(0, 0, 36, bar * 4 + position / 4 - 0.25, 0.25, velocity.main_velocity())

