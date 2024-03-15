import random

drums = [36, 38, 41, 43, 45, 47, 48]


def generate_fill(position, fill_size, file):
    print("FIIIIIIIIILL")


def determine_fill(position, fill_size, file, fill_chance):
    rand = random.random()
    if rand < fill_chance:
        generate_fill(position, fill_size, file)
    else:
        return False
