import velocity


def generate_snare(bar, position, file):
    if position == 8:
        file.addNote(0, 0, 38, bar * 4 + position / 4, 0.25, velocity.main_velocity())
