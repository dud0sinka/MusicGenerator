class BassIntoOpen0DrumFill:
    """
        A class to generate a bass into of "open 0 drum fill" type.
    """
    def __init__(self, root_note, file, start_pos=0):
        self.root_note = root_note
        self.file = file
        self.start_pos = start_pos

    def generate(self, bars):
        if self.root_note < 33:
            self.root_note += 12
        self.file.addNote(0, 0, self.root_note, 0 + self.start_pos, bars * 4, 120)
