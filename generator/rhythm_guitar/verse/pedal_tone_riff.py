import random
from rhythm_guitar import common_stuff as common
from drums.verse.pedal_tone_riff import DrumsPedalToneRiffVerse as Drums
from bass.verse.bass_verse import *
import velocity

SCALES = {
    "MINOR_SCALE": [2, 1, 2, 2, 1, 2, 2],
    "PHRYGIAN_MODE": [1, 2, 2, 2, 1, 2, 2],
    "HARMONIC_MINOR_SCALE": [2, 1, 2, 2, 1, 3, 1],
    "DORIAN_MODE": [2, 1, 2, 2, 2, 1, 2],
}

# TODO: second repeat is either stuff from todo in breakdown or just different random notes

CHORD_PROGRESSIONS = {  # the numbers are the intervals to add to the current root note
    "verse_0": [0, 0, 0, 0],  # 0 0 0 0
    "verse_1": [0, 0, 5, 4],  # 0 0 8 7
    "verse_2": [0, 0, 5, 3],  # 0 0 8 5
    "verse_3": [0, 0, 5, 6],  # 0 0 8 10
    "verse_4": [0, 0, 4, 2],  # 0 0 7 3
    "verse_5": [3, 3, 5, 4],  # 5 5 8 7
    "verse_6": [0, 0, 2, 3]  # 0 0 3 5
}


# data = {"position": ending_position, "scale": current_scale, "bars": number_of_bars, "repetitions": repetitions}


class RGuitarPedalToneRiff:
    def __init__(self, start_pos, root_note, progression=None, scale=None):
        self.start_pos = start_pos
        self.ROOT_NOTE = root_note
        self.current_scale = [] if scale is None else scale
        self.notes_generated = []
        self.progression = None if progression is None else progression
        self.palm_mutes_generated = 0
        self.bass_notes = []
        self.number_of_bars = 0  # used for creating leads
        self.repetitions = 0  # used for creating leads

    def set_number_of_bars(self, number_of_bars, repetitions):
        self.number_of_bars = number_of_bars
        self.repetitions = repetitions

    def extend_progression(self, number_of_bars):
        extended_progression = []
        chosen_progression = random.choice(list(CHORD_PROGRESSIONS.values())) if number_of_bars == 4 else \
            random.choice([v for k, v in CHORD_PROGRESSIONS.items() if k != "verse_0"])

        for i in range(4):
            extended_progression.append(chosen_progression[i])
            extended_progression.append(chosen_progression[i])

        return extended_progression

    def generate(self, gtr_file, drum_file, bass_file, number_of_bars, repetitions, lead_flag=False, lead_var=0.45):
        self.set_number_of_bars(number_of_bars, repetitions)
        ending_position = 0
        high_note_multiplier = 0 if lead_flag is False else 0.45

        if not self.current_scale:
            lets_choose_a_scale = common.choose_scale(SCALES)
            common.fill_scale(self.ROOT_NOTE, lets_choose_a_scale, self.current_scale, self.ROOT_NOTE)

        if self.progression is None:
            self.progression = random.choice(list(CHORD_PROGRESSIONS.values())) if number_of_bars == 4 \
                else self.extend_progression(number_of_bars)

        bar = 0
        for _ in range(number_of_bars):
            self.generate_bar(bar, number_of_bars, 0, high_note_multiplier)
            bar += 1
            ending_position = bar * 4

        ending_position = self.create_repetitions(ending_position, repetitions, number_of_bars)
        data = {"position": ending_position + self.start_pos,
                "bars": number_of_bars, "repetitions": repetitions}
        self.write_to_file(gtr_file, lead_flag, lead_var)

        if lead_flag is False:
            Drums(self.start_pos).generate(drum_file, data)  # generate drums
            write(bass_file, self.bass_notes)  # generate bass

        return ending_position + self.start_pos

    def create_repetitions(self, ending_position, repetitions, number_of_bars):
        end_pos_to_return = ending_position
        notes_to_repeat = self.notes_generated.copy()

        last_root_note_of_progression = self.progression[-1]
        # optional change of the last root note of the progression

        for current_repeat in range(1, repetitions):
            for note in notes_to_repeat:
                if current_repeat == 1 and number_of_bars == 4:  # modify 1st repeat for 4 bars
                    if random.random() < 0.15:
                        # optional change of the last root note of the progression
                        self.progression[-1] = random.choice(
                            list(set(range(len(self.current_scale[:8]))) - set(self.progression)))
                    if note["position"] >= 12 + self.start_pos:
                        self.generate_bar(7, 4, 1, 0.6)
                        break
                    else:
                        note_to_repeat = {"pitch": note["pitch"], "duration": note["duration"],
                                          "position": note["position"] + ending_position * current_repeat}
                        self.notes_generated.append(note_to_repeat)
                        if note_to_repeat["pitch"] > 14:
                            self.bass_notes.append(note_to_repeat)

                elif current_repeat == 3 and number_of_bars == 4:  # modify 3rd repeat for 4 bars
                    if random.random() < 0.25:
                        # optional change of the last root note of the progression
                        self.progression[-1] = random.choice(
                            list(set(range(len(self.current_scale[:8]))) - set(self.progression)))
                    if note["position"] >= 8 + self.start_pos:
                        self.generate_bar(14, 4, 3, 0)
                        self.generate_bar(15, 4, 3, 0.6)
                        break
                    else:
                        note_to_repeat = {"pitch": note["pitch"], "duration": note["duration"],
                                          "position": note["position"] + ending_position * current_repeat}
                        self.notes_generated.append(note_to_repeat)
                        if note_to_repeat["pitch"] > 14:
                            self.bass_notes.append(note_to_repeat)

                elif current_repeat == 1 and number_of_bars == 8:  # modify 1st repeat for 8 bars
                    if random.random() < 0.30:
                        # optional change of the last root note of the progression
                        self.progression[-1] = random.choice(
                            list(set(range(len(self.current_scale[:8]))) - set(self.progression)))
                    if note["position"] >= 28 + self.start_pos:
                        self.generate_bar(15, 8, 1, 0.6)
                        break
                    else:
                        note_to_repeat = {"pitch": note["pitch"], "duration": note["duration"],
                                          "position": note["position"] + ending_position * current_repeat}
                        self.notes_generated.append(note_to_repeat)
                        if note_to_repeat["pitch"] > 14:
                            self.bass_notes.append(note_to_repeat)

                elif current_repeat == 3 and number_of_bars == 8:  # modify 3rd repeat for 8 bars
                    if note["position"] >= 24 + self.start_pos:
                        self.generate_bar(30, 8, 3, 0.6)
                        if random.random() < 0.45:
                            # optional change of the last root note of the progression
                            self.progression[-1] = random.choice(
                                list(set(range(len(self.current_scale[:8]))) - set(self.progression)))
                        self.generate_bar(31, 8, 3, 0.6)
                        break
                    else:
                        note_to_repeat = {"pitch": note["pitch"], "duration": note["duration"],
                                          "position": note["position"] + ending_position * current_repeat}
                        self.notes_generated.append(note_to_repeat)

                        if note_to_repeat["pitch"] > 14:
                            self.bass_notes.append(note_to_repeat)

                else:
                    note_to_repeat = {"pitch": note["pitch"], "duration": note["duration"],
                                      "position": note["position"] + ending_position * current_repeat}
                    note_to_repeat["pitch"] = note_to_repeat["pitch"] - 12 if random.random() < 0.8 and note_to_repeat[
                        "pitch"] > 48 else note_to_repeat[
                        "pitch"]
                    self.notes_generated.append(note_to_repeat)

                    if note_to_repeat["pitch"] > 14:
                        self.bass_notes.append(note_to_repeat)

            self.progression[-1] = last_root_note_of_progression
            end_pos_to_return += number_of_bars * 4

        return end_pos_to_return

    def write_to_file(self, file, lead_flag=False, chance=0.45):
        if lead_flag is False:
            for note in self.notes_generated:  # normal verse riffs
                file.addNote(0, 0, note["pitch"], note["position"], note["duration"], velocity.main_velocity())
        else:

            lead_start_pos = self.start_pos + self.number_of_bars * 4 * self.repetitions / 2
            skip_1st_half_flag = True if random.random() < chance else False

            for note in self.notes_generated:  # lead licks
                if note["position"] < lead_start_pos and skip_1st_half_flag:
                    continue
                if note["pitch"] not in [12, 14]:
                    file.addNote(0, 0, note["pitch"] + 12, note["position"], note["duration"], velocity.main_velocity())
                else:
                    file.addNote(0, 0, note["pitch"], note["position"], note["duration"], velocity.main_velocity())

    def generate_bar(self, bar, number_of_bars, repeat=0, high_note_multiplier=0.0):
        multiplier = 4
        if number_of_bars == 8:
            multiplier = 8
        current_root_note = self.set_root_note(bar) if repeat == 0 \
            else self.set_root_note(bar - multiplier * repeat)
        position = 0
        while position < 4:
            current_note = self.insert_notes(bar, position + self.start_pos, current_root_note, high_note_multiplier)
            note = {  # save a note with the following parameters to the history of generated notes
                "pitch": current_note,
                "duration": 0.5,
                "position": bar * 4 + position + self.start_pos
            }
            bass_note = current_note if current_note > 32 else current_note + 12
            bass_note = {  # bass note
                "pitch": bass_note,
                "duration": 0.5,
                "position": bar * 4 + position + self.start_pos
            }
            self.notes_generated.append(note)
            self.bass_notes.append(bass_note)

            position += 0.5

    def insert_notes(self, bar, position, riff_root_note, high_note_multiplier=0.0):
        if len(self.notes_generated) >= 2 - self.palm_mutes_generated and self.notes_generated[-1]["pitch"] >= \
                self.current_scale[7] \
                and self.notes_generated[-2]["pitch"] >= self.current_scale[7]:
            # no more than two consecutive high notes
            current_note = riff_root_note
        else:
            chance = random.random()
            if chance < 0.65 - high_note_multiplier:
                current_note = riff_root_note
            else:
                current_note = random.choice(self.current_scale[7:])

        if current_note == riff_root_note:  # palm mute the root notes
            if bar == 0 and position == 0:
                pm = {"pitch": 14, "duration": 0.5 / 4, "position": bar * 4 + position - 0.125}
                self.notes_generated.append(pm)
                self.palm_mutes_generated += 1
                # so that palm muting the very first note works
            else:
                pm = {"pitch": 14, "duration": 0.5 / 4, "position": bar * 4 + position - 0.125}
                self.notes_generated.append(pm)
                self.palm_mutes_generated += 1

            pm = {"pitch": 12, "duration": 0.5 / 4, "position": bar * 4 + position + 0.5 / 2 - 0.125}
            self.notes_generated.append(pm)
            self.palm_mutes_generated += 1

        return current_note

    def set_root_note(self, bar):  # choose current root note for pedal tone riffs
        return self.current_scale[self.progression[bar]]
