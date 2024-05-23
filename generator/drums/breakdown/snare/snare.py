import velocity


def snare_step(repetition, bars, file):
    for i in range(bars * 4):
        position = i + bars * 4 * repetition
        if i % 4 == 2:
            file.addNote(0, 0, 38, position, 0.25, velocity.main_velocity())


def snare_half_step(repetition, bars, file):
    for i in range(bars * 4):
        position = i + bars * 4 * repetition
        if i % 8 == 4:
            file.addNote(0, 0, 38, position, 0.25, velocity.main_velocity())
