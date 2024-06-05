import velocity


class Snare:
    def __init__(self, start_pos):
        self.start_pos = start_pos

    def snare_step(self, repetition, bars, file, fill_flag=0):
        for i in range(bars * 4):
            if (fill_flag == 1 and i >= bars * 3 and repetition == 1) or (fill_flag == 2 and i >= bars * 2.5 and repetition == 3):
                break
            position = i + bars * 4 * repetition + self.start_pos
            if i % 4 == 2:
                file.addNote(0, 0, 38, position, 0.25, velocity.main_velocity())

    def snare_half_step(self, repetition, bars, file, fill_flag=0):
        for i in range(bars * 4):
            if (fill_flag == 1 and i >= bars * 3 and repetition == 1) or (fill_flag == 2 and i >= bars * 2 and repetition == 3):
                break
            position = i + bars * 4 * repetition + self.start_pos
            if i % 8 == 4:
                file.addNote(0, 0, 38, position, 0.25, velocity.main_velocity())
