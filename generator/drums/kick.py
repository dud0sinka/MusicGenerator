import velocity
import random
from rhythm_guitar import rhythm_guitar_main


def generate_kick(file):
    for i in rhythm_guitar_main.kick:
        file.addNote(0, 0, 36, i, 0.25, velocity.main_velocity())

