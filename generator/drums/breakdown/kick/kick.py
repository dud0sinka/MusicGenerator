import velocity
import random


def default_kick(repetition, bars, kick_list, start_pos, kicks_generated, fill_flag=0):  # follows the pattern of the guitar
    print(kick_list)
    print(start_pos + bars * 3)
    for i in kick_list:
        if fill_flag == 1 and (i >= start_pos + 12 and repetition == 1) or (fill_flag == 2 and (repetition == 3 and i >= start_pos + 10)):
            break
        kicks_generated.append(i + bars * 4 * repetition)
    return kicks_generated


class Kick:
    def __init__(self, start_pos, kicks_generated):
        self.start_pos = start_pos
        self.kicks_generated = kicks_generated

    def four_on_the_floor(self, repetition, bars, fill_flag=0):
        for i in range(0, bars * 4):
            if (fill_flag == 1 and i >= bars * 3 and repetition == 1) or (fill_flag == 2 and i >= bars * 2.5 and repetition == 3):
                break
            if i % 4 == 0:
                self.kicks_generated.append(i + bars * 4 * repetition + self.start_pos)
            if i % 2 == 0 and i != 0:
                self.kick_bursts_before_snare(repetition, bars, i)

    def kick_bursts_before_snare(self, repetition, bars, i, variation=4):
        burst_chance = random.random()
        if burst_chance < 0.4 / variation:
            if variation == 2:
                self.kicks_generated.append(i + bars * 4 * repetition + self.start_pos)
            self.kicks_generated.append(i + bars * 4 * repetition - 0.25 + self.start_pos)
            self.kicks_generated.append(i + bars * 4 * repetition - 0.5 + self.start_pos)
            if variation == 4:
                self.kicks_after_snare(repetition, bars, i)

        if burst_chance < 0.2 / variation:
            self.kicks_generated.append(i + bars * 4 * repetition - 0.75 + self.start_pos)
            self.kicks_generated.append(i + bars * 4 * repetition - 1 + self.start_pos)
            if variation == 4:
                self.kicks_after_snare(repetition, bars, i)

    def kicks_after_snare(self, repetition, bars, i):
        kick_after_snare_chance = random.random()
        available_positions = [0.5, 0.75, 1, 1.5]

        if kick_after_snare_chance < 0.25:
            position = random.choice(available_positions)
            self.kicks_generated.append(i + bars * 4 * repetition + position + self.start_pos)
            available_positions.remove(position)
            if position == 0.75:
                self.kicks_generated.append(i + bars * 4 * repetition + 1.5 + self.start_pos)
                kick_after_snare_chance = 1
        if kick_after_snare_chance < 0.15:
            position = random.choice(available_positions)
            self.kicks_generated.append(i + bars * 4 * repetition + position + self.start_pos)
            available_positions.remove(position)
        if kick_after_snare_chance < 0.1:
            position = random.choice(available_positions)
            self.kicks_generated.append(i + bars * 4 * repetition + position + self.start_pos)
            available_positions.remove(position)

    def double_bass(self, repetition, bars, fill_flag=0):
        for i in range(0, bars * 4):
            if (fill_flag == 1 and i >= bars * 3 and repetition == 1) or (fill_flag == 2 and i >= bars * 2.5 and repetition == 3):
                break
            j = 0
            for _ in range(4):
                self.kicks_generated.append(i + bars * 4 * repetition + j + self.start_pos)
                j += 0.25

    def eighth_kicks(self, repetition, bars, fill_flag=0):
        for i in range(0, bars * 4):
            if (fill_flag == 1 and i >= bars * 3 and repetition == 1) or (
                    fill_flag == 2 and i >= bars * 2.5 and repetition == 3):
                break
            j = 0
            for _ in range(2):
                self.kicks_generated.append(i + bars * 4 * repetition + j + self.start_pos)
                j += 0.5
                if i % 2 == 0 and i != 0:
                    self.kick_bursts_before_snare(repetition, bars, i, 8)

    def two_on_the_floor(self, repetition, bars, fill_flag=0):
        for i in range(0, bars * 4):
            if (fill_flag == 1 and i >= bars * 3 and repetition == 1) or (fill_flag == 2 and i >= bars * 2.5 and repetition == 3):
                break
            if i % 8 == 0:
                self.kicks_generated.append(i + bars * 4 * repetition + self.start_pos)
            if i % 4 == 0 and i != 0:
                self.kick_bursts_before_snare(repetition, bars, i, 2)
