class BassDefaultMelodicBreakdown:
    def __init__(self, guitar_notes):
        self.bass_notes = []
        self.current_low_note_position = -1
        self.last_16th_note = -1
        self.guitar_notes = guitar_notes

    def copy_guitar(self, file):
        for note in self.guitar_notes:
            if note["duration"] == 0.25:
                self.last_16th_note = note["position"]

            if note["pitch"] > 38 and note["position"] == self.current_low_note_position:
                continue

            if 29 <= note["pitch"] <= 38:
                self.current_low_note_position = note["position"]

            if note["pitch"] == 14 or note["pitch"] == 12:
                continue

            if note["pitch"] > 48 and note["duration"] <= 0.5 and note["position"] != self.last_16th_note + 0.25:
                continue

            if note["pitch"] > 48:
                bass_note = {
                    "pitch": note["pitch"] - 12,
                    "duration": note["duration"],
                    "position": note["position"]
                }
                self.bass_notes.append(bass_note)
                continue

            if 29 <= note["pitch"] < 33:
                bass_note = {
                    "pitch": note["pitch"] + 12,
                    "duration": note["duration"],
                    "position": note["position"]
                }
                self.bass_notes.append(bass_note)
            else:
                bass_note = {
                    "pitch": note["pitch"],
                    "duration": note["duration"],
                    "position": note["position"]
                }
                self.bass_notes.append(bass_note)

        self.bass_notes = self.check_for_the_same_positions()
        self.write(file)

    def check_for_the_same_positions(self):
        filtered_notes = []

        for i in range(len(self.bass_notes) - 1):
            current_note = self.bass_notes[i]
            next_note = self.bass_notes[i + 1]
            if current_note["position"] != next_note["position"]:
                filtered_notes.append(current_note)

        filtered_notes.append(self.bass_notes[-1])
        return filtered_notes

    def write(self, file):
        for note in self.bass_notes:
            file.addNote(0, 0, note["pitch"], note["position"], note["duration"], 120)
