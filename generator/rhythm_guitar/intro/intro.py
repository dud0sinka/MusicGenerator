import random

import drums.common
import rhythm_guitar.verse.pedal_tone_riff
import velocity
from drums.intro.open0_drum_fill import DrumsIntoOpen0DrumFill as Drums
from bass.intro.intro import BassIntoOpen0DrumFill as Bass
from rhythm_guitar.verse.pedal_tone_riff import RGuitarPedalToneRiff as Guitar
from rhythm_guitar import common_stuff as common
import rhythm_guitar.verse.pedal_tone_riff as guitar

ROOT_NOTE_LOWEST = 29
ROOT_NOTE_HIGHEST = 38


def slide_or_dead_notes(gtr_file, bars):
    if random.random() > 0.5:
        gtr_file.addNote(0, 0, 102, bars * 4 - 2, 1, velocity.main_velocity())  # slide
        gtr_file.addNote(0, 0, 101, bars * 4 - 1, 1, velocity.main_velocity())
        return False
    else:
        gtr_file.addNote(0, 0, 94, bars * 4 - 2, 0.5, velocity.main_velocity())  # dead notes
        gtr_file.addNote(0, 0, 94, bars * 4 - 1.5, 0.5, velocity.main_velocity())
        gtr_file.addNote(0, 0, 94, bars * 4 - 1, 0.5, velocity.main_velocity())
        gtr_file.addNote(0, 0, 94, bars * 4 - 0.5, 0.5, velocity.main_velocity())
        return True


def choose_intro():
    intros = ["open0_drum_fill", "none", "drum_fill", "ambience"]
    return random.choice(intros)


class RGuitarIntro:

    def __init__(self):
        self.ROOT_NOTE = random.randint(ROOT_NOTE_LOWEST, ROOT_NOTE_HIGHEST)
        self.intro = choose_intro()

    def get_root(self):
        return self.ROOT_NOTE

    def generate(self, gtr_file, drum_file, bass_file, bars, amb_file=None):
        if self.intro == "open0_drum_fill":
            root_copy = self.ROOT_NOTE if self.ROOT_NOTE > 34 else self.ROOT_NOTE + 12

            gtr_file.addNote(0, 0, root_copy, 0, bars * 4 - 2, velocity.main_velocity())
            gtr_file.addNote(0, 0, root_copy + 7, 0, bars * 4 - 2, velocity.main_velocity())
            gtr_file.addNote(0, 0, root_copy + 12, 0, bars * 4 - 2, velocity.main_velocity())

            dead_notes = slide_or_dead_notes(gtr_file, bars)

            Drums(drum_file).generate(bars, dead_notes)
            Bass(self.ROOT_NOTE, bass_file).generate(bars)
        if self.intro == "drum_fill":
            bars //= 2
            drums.common.choose_and_generate_fill(0, bars, drum_file, True)
        if self.intro == "none":
            return 0
        if self.intro == "ambience":
            print("test")
            lets_choose_a_scale = common.choose_scale(guitar.SCALES)
            scale = common.fill_scale(self.ROOT_NOTE, lets_choose_a_scale, [], self.ROOT_NOTE)
            progression = random.choice(list(guitar.CHORD_PROGRESSIONS.values()))
            Guitar(0, self.ROOT_NOTE, progression, scale).generate(amb_file, None, None, bars, 0, False, False, True)
            fill_size = random.choice([0, 0.5, 1])
            drums.common.choose_and_generate_fill(bars * 4 - fill_size * 4, fill_size, drum_file, True)
        return bars * 4  # starting position for the next section
