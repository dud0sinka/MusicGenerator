import random
import velocity
from drums.intro.open0_drum_fill import DrumsIntoOpen0DrumFill as Drums
from bass.intro.open0_drum_fill import BassIntoOpen0DrumFill as Bass

ROOT_NOTE_LOWEST = 29
ROOT_NOTE_HIGHEST = 38


class RGuitarIntoOpen0DrumFill:

    def __init__(self):
        self.ROOT_NOTE = random.randint(ROOT_NOTE_LOWEST, ROOT_NOTE_HIGHEST)

    def get_root(self):
        return self.ROOT_NOTE

    def generate(self, gtr_file, drum_file, bass_file, bars, repetitions=0):
        self.ROOT_NOTE = random.randint(ROOT_NOTE_LOWEST, ROOT_NOTE_HIGHEST)
        root_copy = self.ROOT_NOTE if self.ROOT_NOTE > 34 else self.ROOT_NOTE + 12

        gtr_file.addNote(0, 0, root_copy, 0, bars * 4 - 2, velocity.main_velocity())
        gtr_file.addNote(0, 0, root_copy + 7, 0, bars * 4 - 2, velocity.main_velocity())
        gtr_file.addNote(0, 0, root_copy + 12, 0, bars * 4 - 2, velocity.main_velocity())

        gtr_file.addNote(0, 0, 102, bars * 4 - 2, 1, velocity.main_velocity())  # slide
        gtr_file.addNote(0, 0, 101, bars * 4 - 1, 1, velocity.main_velocity())

        Drums(drum_file).generate(bars)
        Bass(self.ROOT_NOTE, bass_file).generate(bars)
        return bars * 4  # starting position for the next section
