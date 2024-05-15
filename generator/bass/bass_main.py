import velocity
from rhythm_guitar import generate_default_breakdown as gtr
from velocity import main_velocity


def copy_guitar(file):
    bass_notes = []

    current_low_note_position = -1
    last_16th_note = -1

    for note in gtr.notes_generated:
        if note["duration"] == 0.25:
            last_16th_note = note["position"]

        if note["pitch"] > 38 and note["position"] == current_low_note_position:
            continue

        if 29 <= note["pitch"] <= 38:
            current_low_note_position = note["position"]

        if note["pitch"] == 14:
            continue

        if note["pitch"] > 48 and note["duration"] <= 0.5 and note["position"] != last_16th_note + 0.25:
            continue

        if note["pitch"] > 48:
            bass_note = {
                "pitch": note["pitch"] - 12,
                "duration": note["duration"],
                "position": note["position"]
            }
            bass_notes.append(bass_note)
            continue

        if 29 <= note["pitch"] < 33:
            bass_note = {
                "pitch": note["pitch"] + 12,
                "duration": note["duration"],
                "position": note["position"]
            }
            bass_notes.append(bass_note)
        else:
            bass_note = {
                "pitch": note["pitch"],
                "duration": note["duration"],
                "position": note["position"]
            }
            bass_notes.append(bass_note)

    bass_notes = check_fo_the_same_positions(bass_notes)
    write(file, bass_notes)


def check_fo_the_same_positions(bass_notes):
    filtered_notes = []

    for i in range(len(bass_notes) - 1):
        current_note = bass_notes[i]
        next_note = bass_notes[i + 1]
        if current_note["position"] != next_note["position"]:
            filtered_notes.append(current_note)

    filtered_notes.append(bass_notes[-1])
    return filtered_notes


def write(file, bass_notes):
    for note in bass_notes:
        file.addNote(0, 0, note["pitch"], note["position"], note["duration"], 120)
