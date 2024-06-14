import random

from rhythm_guitar.verse.pedal_tone_riff import RGuitarPedalToneRiff as Guitar


def generate(amb_file, number_of_bars, repetitions, start_pos, root, scale, is_lead):
    if is_lead:
        repetitions //= 2
    else:
        if random.random() > 0.69:
            start_pos += 32
            repetitions //= 2

    if random.random() > 0.45:
        Guitar(start_pos, root, [0, 0, 0, 0], scale).generate(amb_file, None, None,
                                                              number_of_bars, repetitions,
                                                              False, False, True)

# TOD0: ambient pre breakdown with drums and bass
