import velocity


def generate_snare(number_of_bars, file):
    bar = 0
    for _ in range(number_of_bars):
        file.addNote(0, 0, 38, bar * 4 + 2, 0.25, velocity.main_velocity())
        bar += 1
