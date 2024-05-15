import velocity
import random
from rhythm_guitar import generate_default_breakdown


def generate_kick(file):
    for i in generate_default_breakdown.kick:
        file.addNote(0, 0, 36, i, 0.25, velocity.main_velocity())

