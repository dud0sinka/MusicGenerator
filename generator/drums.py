import random

import kick
import snare
import cymbals
import fills


def generate_drums(file, number_of_bars):
    fill_chance = 0.1
    power_hand_change_chance = 0.75
    bar = 0
    position = 0
    current_power_hand = random.choice(cymbals.power_hand)

    while bar < number_of_bars:
        for i in range(16):
            kick.generate_kick(bar, position, file)
            snare.generate_snare(bar, position, file)
            cymbals.generate_cymbals(bar, position, file, current_power_hand)
            position += 1
        bar += 1
        position = 0

        if bar % 3 == 0:
            if not fills.determine_fill(bar + position, 16, file, fill_chance):
                fill_chance += 0.1
            else:
                fill_chance = 0.1

        if bar % 4 == 0:
            current_power_hand = cymbals.choose_power_hand(power_hand_change_chance, current_power_hand)
