from . import kick
from . import snare
from . import cymbals


def generate_drums(file, number_of_bars):
    kick.generate_kick(file)
    snare.generate_snare(number_of_bars, file)
    cymbals.generate_cymbals(number_of_bars, file)