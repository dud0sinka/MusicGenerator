import random
import velocity

ROOT_NOTE = 0
ROOT_NOTE_LOWEST = 29
ROOT_NOTE_HIGHEST = 38


def generate(start_pos, bars, file):
    root_note = random.randint(ROOT_NOTE_LOWEST, ROOT_NOTE_HIGHEST)
    file.addNote(0, 0, root_note, 0, bars * 4 - 2, velocity.main_velocity())
    file.addNote(0, 0, root_note + 7, 0, bars * 4 - 2, velocity.main_velocity())
    file.addNote(0, 0, root_note + 12, 0, bars * 4 - 2, velocity.main_velocity())

    file.addNote(0, 0, 102, bars * 4 - 2, 1, velocity.main_velocity())  # slide
    file.addNote(0, 0, 101, bars * 4 - 1, 1, velocity.main_velocity())
    return bars * 4  # starting position for the next section
