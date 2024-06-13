from drums import common
from drums.kick.kick import *
from drums.snare.snare import *
from drums.common import *

snare_variations = ["step", "half-step"]
kick_variations = ["double_bass", "4_on_the_floor", "default", "8th_kicks", "2_on_the_floor"]


# TODO: ghost notes
# TODO: copy the entire breakdown another time and add ambience or not

class DrumsDefaultMelodicBreakdown:
    def __init__(self, start_pos, outside_flag=False):
        self.previous_kick = ""  # used for generating opening cymbals
        self.previous_snare = ""  # used for generating opening cymbals
        self.current_cymbal = ""  # used for generating opening cymbals
        self.start_pos = start_pos
        self.snare = Snare(start_pos)
        self.kicks_generated = []
        self.kick = Kick(start_pos)
        self.outside_flag = outside_flag

    def generate(self, file, data, kick_list):
        bars = data["bars"]
        repetitions = data["repetitions"]

        for repetition in range(repetitions):
            fill_flag = 0
            if repetition in [1, 5]:
                fill_flag = 1
            if repetition in [3, 7]:
                fill_flag = 2

            kick_snare = self.generate_kick_and_snare(repetition, bars, kick_list, fill_flag)
            self.insert_snare(repetition, bars, file, kick_snare[1], fill_flag)
            self.generate_cymbals(repetition, bars, file, kick_snare[0], kick_snare[1], fill_flag)
            self.previous_kick = kick_snare[0]
            self.previous_snare = kick_snare[1]

            if repetition in [1, 5]:
                choose_and_generate_fill(self.start_pos + bars * 4 * repetition + bars * 3, 1, file)
            if repetition in [3, 7]:
                fill_size = 1.5 if random.random() < 0.5 else 2
                choose_and_generate_fill(self.start_pos + bars * 4 * repetition + bars * (4 - fill_size), fill_size,
                                         file)
        self.write_kicks_to_file(file)

    def write_kicks_to_file(self, file):
        for kick in self.kicks_generated:
            file.addNote(0, 0, 36, kick, 0.25, velocity.main_velocity())

    def generate_kick_and_snare(self, repetition, bars, kick_list, fill_flag=0):
        kick_variation = self.choose_kick_variation(repetition)
        snare_variation = ""
        if kick_variation == "default":
            self.kicks_generated.extend(
                default_kick(repetition, bars, kick_list, self.start_pos, self.kicks_generated, fill_flag))
            snare_variation = random.choice(snare_variations)
        if kick_variation == "4_on_the_floor":
            self.kicks_generated.extend(
                self.kick.four_on_the_floor(repetition, bars, fill_flag))
            snare_variation = "step"
        if kick_variation == "double_bass":
            self.kicks_generated.extend(
                self.kick.double_bass(repetition, bars, fill_flag))
            snare_variation = random.choice(snare_variations)
        if kick_variation == "8th_kicks":
            self.kicks_generated.extend(
                self.kick.eighth_kicks(repetition, bars, fill_flag))
            snare_variation = random.choice(snare_variations)
        if kick_variation == "2_on_the_floor":
            self.kicks_generated.extend(
                self.kick.two_on_the_floor(repetition, bars, fill_flag))
            snare_variation = "half-step"
        return kick_variation, snare_variation

    def insert_snare(self, repetition, bars, file, snare_variation, fill_flag=0):
        if snare_variation == "step":
            self.snare.snare_step(repetition, bars, file, fill_flag)
        if snare_variation == "half-step":
            self.snare.snare_half_step(repetition, bars, file, fill_flag)

    def choose_kick_variation(self, repetition):
        if repetition <= 1 or self.outside_flag is True:
            return "default"
        else:
            variation = random.choice(kick_variations)
            return variation

    def generate_cymbals(self, repetition, bars, file, current_kick, current_snare, fill_flag=0):
        if current_kick != self.previous_kick or current_snare != self.previous_snare:
            self.current_cymbal = random.choice(common.power_hand)  # conditions for current power hand change
        else:
            pass

        for i in range(bars * 4):
            position = i + bars * 4 * repetition + self.start_pos
            if (fill_flag == 1 and position >= self.start_pos + bars * 4 * repetition + bars * 3)\
                    or (fill_flag == 2 and position >= self.start_pos + bars * 4 * repetition + bars * 2.5):
                break

            if (position == bars * 4 * repetition + self.start_pos and current_kick != self.previous_kick) \
                    or (
                    position == bars * 4 * repetition + self.start_pos and current_snare != self.previous_snare):  # opening cymbals
                common.opening_cymbals(file, position)

            if (i % 2 == 0 and position != bars * 4 * repetition + self.start_pos) or (
                    i % 2 == 0 and current_kick == self.previous_kick) \
                    and current_snare == self.previous_snare:  # current power hand cymbal
                file.addNote(0, 0, self.current_cymbal, position, 0.25, velocity.main_velocity())

            if i % 2 == 1:  # add a random splash on a downbeat
                splash_chance = random.random()
                if splash_chance < 0.1:
                    file.addNote(0, 0, 55, position, 0.25, velocity.main_velocity())
