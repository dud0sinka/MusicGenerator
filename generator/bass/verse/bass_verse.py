def add_note(self, note):
    self.bass_notes.append(note)


def write(file, bass_notes):
    for note in bass_notes:
        if 14 < note["pitch"] < 33:
            note["pitch"] += 12
        if note["pitch"] > 47:
            note["pitch"] -= 12
        velocity = 120 if note["pitch"] < 43 else 108
        file.addNote(0, 0, note["pitch"], note["position"], note["duration"], velocity)
