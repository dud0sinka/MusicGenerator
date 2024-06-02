import random
from drums import common
from drums.breakdown.kick.kick import *
from drums.breakdown.snare.snare import *

snare_variations = ["step", "half-step"]
kick_variations = ["double_bass", "4_on_the_floor", "default", "8th_kicks", "2_on_the_floor"]
previous_kick = ""  # used for generating opening cymbals
previous_snare = ""  # used for generating opening cymbals
current_cymbal = ""  # used for generating opening cymbals

# TODO: ghost notes
# TODO: opening cymbal on 2
# TODO: each section has its starting position
# TODO: bass on half step is matching kick drums


def generate(file, data):
    global previous_kick, previous_snare
    bars = data["bars"]
    repetitions = data["repetitions"]

    for repetition in range(repetitions):
        kick_snare = generate_kick_and_snare(repetition, bars, file)
        insert_snare(repetition, bars, file, kick_snare[1])
        generate_cymbals(repetition, bars, file, kick_snare[0], kick_snare[1])
        previous_kick = kick_snare[0]
        previous_snare = kick_snare[1]


def generate_kick_and_snare(repetition, bars, file):
    kick_variation = choose_kick_variation(repetition)
    snare_variation = ""
    if kick_variation == "default":
        default_kick(repetition, file, bars)
        snare_variation = random.choice(snare_variations)
    if kick_variation == "4_on_the_floor":
        four_on_the_floor(repetition, file, bars)
        snare_variation = "step"
    if kick_variation == "double_bass":
        double_bass(repetition, file, bars)
        snare_variation = random.choice(snare_variations)
    if kick_variation == "8th_kicks":
        eighth_kicks(repetition, file, bars)
        snare_variation = random.choice(snare_variations)
    if kick_variation == "2_on_the_floor":
        two_on_the_floor(repetition, file, bars)
        snare_variation = "half-step"
    return kick_variation, snare_variation


def insert_snare(repetition, bars, file, snare_variation):
    if snare_variation == "step":
        snare_step(repetition, bars, file)
    if snare_variation == "half-step":
        snare_half_step(repetition, bars, file)


def choose_kick_variation(repetition):
    if repetition <= 1:
        print("default")
        return "default"
    else:
        variation = random.choice(kick_variations)
        print(variation)
        return variation


def generate_cymbals(repetition, bars, file, current_kick, current_snare):
    global current_cymbal

    if current_kick != previous_kick or current_snare != previous_snare:  # conditions for current power hand change
        current_cymbal = random.choice(common.power_hand)
    else:
        pass

    for i in range(bars * 4):
        position = i + bars * 4 * repetition

        if (position == bars * 4 * repetition and current_kick != previous_kick)\
                or (position == bars * 4 * repetition and current_snare != previous_snare):  # opening cymbals
            common.opening_cymbals(file, position)

        if (i % 2 == 0 and position != bars * 4 * repetition) or (i % 2 == 0 and current_kick == previous_kick) \
                and current_snare == previous_snare:  # current power hand cymbal
            file.addNote(0, 0, current_cymbal, position, 0.25, velocity.main_velocity())

        if i % 2 == 1:  # add a random splash on a downbeat
            splash_chance = random.random()
            if splash_chance < 0.1:
                file.addNote(0, 0, 55, position, 0.25, velocity.main_velocity())


def generate_fill():
    return
