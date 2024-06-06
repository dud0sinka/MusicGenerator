import velocity
from drums import common
import random


class DrumsIntoOpen0DrumFill:
    def __init__(self, file):
        self.file = file

    def generate(self, bars):
        self.kick_and_openers()
        if bars == 2:
            if random.random() > 0.5:  # randomize where the fill begins
                common.generate_triplet_fill(4, 1, self.file)
            else:
                common.generate_fast_fill(6, 0.5, self.file)
        if bars == 4:
            if random.random() > 0.5:  # randomize where the fill begins
                common.generate_fast_fill(8, 2, self.file)
                self.insert_cymbals_on_upbeat(8)
            else:
                common.generate_fast_fill(12, 1, self.file)
                self.insert_cymbals_on_upbeat(12)

    def kick_and_openers(self):
        self.file.addNote(0, 0, 36, 0, 0.25, velocity.main_velocity())
        common.opening_cymbals(self.file, 0)

    def insert_cymbals_on_upbeat(self, fill_start_pos):
        if random.random() > 0.7:
            cymbal = random.choice(common.power_hand)
            half_time = random.random() > 0.5
            positions = [2, 6, 10] if half_time else [1, 3, 5, 7, 9, 11]

            for pos in positions:
                if pos >= fill_start_pos:
                    break
                self.file.addNote(0, 0, cymbal, pos, 0.25, velocity.main_velocity())
