import velocity


class BassIntoOpen0DrumFill:
    def __init__(self, root_note, file):
        self.root_note = root_note
        self.file = file

    def generate(self, bars):
        if self.root_note < 33:
            self.root_note += 12
        self.file.addNote(0, 0, self.root_note, 0, bars * 4, velocity.main_velocity())
