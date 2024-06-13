import velocity


class Snare:
    def __init__(self, start_pos):
        self.start_pos = start_pos

    def snare_double_time(self, repetition, bars, file, fill_flag=0):
        for i in range(bars * 4):
            if (fill_flag == 1 and i >= bars * 3) or (fill_flag == 2 and i >= bars * 2.5 and repetition in [3, 7])\
                    or (fill_flag == 3 and i == bars * 4 - 2) or (fill_flag == 4 and i == bars * 4 - 4):
                break
            position = i + bars * 4 * repetition + self.start_pos
            if i % 1 == 0 and i != 0:
                file.addNote(0, 0, 38, position, 0.25, velocity.main_velocity())

    def snare_step(self, repetition, bars, file, fill_flag=0):
        for i in range(bars * 4):
            if (fill_flag == 1 and i >= bars * 3) or (fill_flag == 2 and i >= bars * 2.5 and repetition in [3, 7])\
                    or (fill_flag == 3 and i == bars * 4 - 2) or (fill_flag == 4 and i == bars * 4 - 4):
                break
            position = i + bars * 4 * repetition + self.start_pos
            if i % 4 == 2:
                file.addNote(0, 0, 38, position, 0.25, velocity.main_velocity())

    def snare_half_step(self, repetition, bars, file, fill_flag=0):
        for i in range(bars * 4):
            if (fill_flag == 1 and i >= bars * 3) or (fill_flag == 2 and i >= bars * 2 and repetition in [3, 7])\
                    or (fill_flag == 3 and i == bars * 4 - 2) or (fill_flag == 4 and i == bars * 4 - 4):
                break
            position = i + bars * 4 * repetition + self.start_pos
            if i % 8 == 4:
                file.addNote(0, 0, 38, position, 0.25, velocity.main_velocity())

    def snare_blast1(self, repetition, bars, file, fill_flag=0):
        for i in range(bars * 4):
            if (fill_flag == 1 and i >= bars * 3) or (fill_flag == 2 and i >= bars * 2 and repetition in [3, 7]) \
                    or (fill_flag == 3 and i == bars * 4 - 2) or (fill_flag == 4 and i == bars * 4 - 4):
                break

            position = i + bars * 4 * repetition + self.start_pos

            if i == 0:
                file.addNote(0, 0, 38, position + 0.5, 0.25, velocity.main_velocity() - 25)

            if i % 1 == 0 and i != 0:
                file.addNote(0, 0, 38, position, 0.25, velocity.main_velocity() - 10)
                file.addNote(0, 0, 38, position + 0.5, 0.25, velocity.main_velocity() - 25)

    def snare_blast2(self, repetition, bars, file, fill_flag=0):
        for i in range(bars * 4):
            if (fill_flag == 1 and i >= bars * 3) or (fill_flag == 2 and i >= bars * 2 and repetition in [3, 7]) \
                    or (fill_flag == 3 and i == bars * 4 - 2) or (fill_flag == 4 and i == bars * 4 - 4):
                break

            position = i + bars * 4 * repetition + self.start_pos

            if i % 1 == 0 and i != 0:
                file.addNote(0, 0, 38, position, 0.25, velocity.main_velocity() - 10)
                file.addNote(0, 0, 38, position + 0.33, 0.25, velocity.main_velocity() - 35)
                file.addNote(0, 0, 38, position + 0.66, 0.25, velocity.main_velocity() - 30)
