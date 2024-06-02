import velocity
import random
from rhythm_guitar import common_stuff as common

# position: 0.25 = 16th note, 0.5 = 8th note, 1 = 4th note. 1 bar has 16 positions
# duration: 0.25 = 16th, 0.5 = 8th, 1 = 4th
# we use bar * 4 because we count bars as 0, 1, 2..... but in terms of position 1 bar equals to 4
# MyMIDI.addNote(track,channel,pitch,position,duration,volume)

ROOT_NOTE_LOWEST = 29
ROOT_NOTE_HIGHEST = 38
SCALES = {
    "MINOR_SCALE": [2, 1, 2, 2, 1, 2, 2],
    "PHRYGIAN_MODE": [1, 2, 2, 2, 1, 2, 2],
    "PHRYGIAN_DOMINANT_MODE": [1, 3, 1, 2, 1, 2, 2],
    "HARMONIC_MINOR_SCALE": [2, 1, 2, 2, 1, 3, 1],
    "MELODIC_MINOR_SCALE_ASCENDING": [2, 1, 2, 2, 2, 2, 1],
    "DORIAN_MODE": [2, 1, 2, 2, 2, 1, 2],
    "MIXOLYDIAN_MODE": [2, 2, 1, 2, 2, 1, 2],
    "LYDIAN_MODE": [2, 2, 2, 1, 2, 2, 1],
    "LOCRIAN_MODE": [1, 2, 2, 1, 2, 2, 2],
}
INTERVALS = {
    "second": 1,
    "third": 2,
    "fourth": 3,
    "sixth": 5,
}


# TODO: spice-up parts (octaves, runs, regenerate, chords etc.)
# TODO: different types of breakdowns (this one is default / melodic)
# TODO: dead notes

class DefaultMelodicBreakdown:
    def __init__(self, start_pos):
        self.start_pos = start_pos
        self.kick = []  # guitar 0's are being passed here to match the kick
        self.current_scale = []  # scale that was chosen
        self.root_notes_generated = []  # amount of generated 0's is affecting the amount of rests
        self.ROOT_NOTE = 0
        self.recent_note = 0  # keep track of the last note played
        self.recent_duration = 0  # keep track of the duration of the lat note played
        self.notes_generated = []  # all notes generated
        self.consecutive_16ths = 0  # this variable is used to prevent the generation of singular 16th notes

    def generate(self, file, number_of_bars, repetitions):
        self.ROOT_NOTE = random.randint(ROOT_NOTE_LOWEST, ROOT_NOTE_HIGHEST)
        ending_position = 0

        lets_choose_a_scale = common.choose_scale(SCALES)
        common.fill_scale(self.ROOT_NOTE, lets_choose_a_scale, self.current_scale, self.ROOT_NOTE)

        bar = 0
        for _ in range(number_of_bars):
            self.generate_bar(bar)
            bar += 1
            ending_position = bar * 4

        self.create_kick_pattern()
        self.create_repetitions(ending_position, repetitions)

        self.add_to_file(file)
        data = {"position": ending_position + self.start_pos, "scale": self.current_scale,
                "bars": number_of_bars, "repetitions": repetitions}
        return data

    def generate_bar(self, bar):
        position = 0
        while position < 4:

            position_copy = position
            position = self.insert_rests(position)
            if position == -1:
                position = position_copy
            else:
                continue

            current_duration = self.randomize_duration(position)  # generate duration
            if self.consecutive_16ths % 2 != 0 and current_duration != 0.25:  # prevent singular 16th notes
                current_duration = 0.25
            if current_duration == 0.25:
                self.consecutive_16ths += 1
            else:
                self.consecutive_16ths = 0

            self.palm_mute(bar, position + self.start_pos, current_duration)

            current_note = self.insert_notes(bar, position + self.start_pos, current_duration)
            self.root_notes_generated.append(current_note)
            note = {  # save a note with the following parameters to the history of generated notes
                "pitch": current_note,
                "duration": current_duration,
                "position": bar * 4 + position + self.start_pos
            }
            self.notes_generated.append(note)

            position += current_duration

            self.recent_note = current_note
            self.recent_duration = current_duration

    def add_to_file(self, file):
        for note in self.notes_generated:
            file.addNote(0, 0, note["pitch"], note["position"], note["duration"], velocity.main_velocity())

    def create_repetitions(self, ending_position, repetitions):
        notes_to_repeat = self.notes_generated.copy()
        for current_repeat in range(1, repetitions):
            for note in notes_to_repeat:
                if note["pitch"] not in [12, 14]:  # Check if the pitch is not 12 or 14
                    if current_repeat == 1:
                        if note["position"] >= 12 + self.start_pos:
                            self.generate_bar(7)
                            break
                        else:
                            self.notes_generated.append({"pitch": note["pitch"], "duration": note["duration"],
                                                         "position": note[
                                                                         "position"] + ending_position * current_repeat})
                    elif current_repeat == 3:
                        if note["position"] >= 8 + self.start_pos:
                            self.generate_bar(14)
                            self.generate_bar(15)
                            break
                        else:
                            self.notes_generated.append({"pitch": note["pitch"], "duration": note["duration"],
                                                         "position": note[
                                                                         "position"] + ending_position * current_repeat})
                    else:
                        self.notes_generated.append({"pitch": note["pitch"], "duration": note["duration"],
                                                     "position": note["position"] + ending_position * current_repeat})
            self.copy_palm_mutes_to_repetitions(current_repeat, notes_to_repeat, ending_position)

    def copy_palm_mutes_to_repetitions(self, current_repeat, notes_to_repeat,
                                       ending_position):  # copying palm mutes sometimes
        # causes exceptions i cant find the reason behind; hence a separate function
        if current_repeat == 1:
            for pm in notes_to_repeat:  # copy to 1 repetition
                if pm["pitch"] == 12 or pm["pitch"] == 14:
                    if pm["position"] < 11.925 + self.start_pos:
                        self.notes_generated.append({"pitch": pm["pitch"], "duration": pm["duration"],
                                                     "position": pm["position"] + ending_position * current_repeat})
        elif current_repeat == 2:
            for pm in notes_to_repeat:  # copy to 2 repetition
                if pm["pitch"] == 12 or pm["pitch"] == 14:
                    if 0.25 < pm["position"] < 15.25 + self.start_pos:
                        self.notes_generated.append({"pitch": pm["pitch"], "duration": pm["duration"],
                                                     "position": pm["position"] + ending_position * current_repeat})
        elif current_repeat == 3:
            for pm in notes_to_repeat:  # copy to 3 repetition
                if pm["pitch"] == 12 or pm["pitch"] == 14:
                    if pm["position"] < 7.925 + self.start_pos:
                        self.notes_generated.append({"pitch": pm["pitch"], "duration": pm["duration"],
                                                     "position": pm["position"] + ending_position * current_repeat})

    def create_kick_pattern(self):
        for note in self.notes_generated:
            if note["position"] == self.start_pos and note["position"] not in self.kick:
                self.kick.append(self.start_pos)
                continue
            if note["pitch"] > ROOT_NOTE_HIGHEST and note["position"] not in self.kick:  # optional kick for high notes
                if random.random() < 0.4:
                    self.kick.append(note["position"])
                continue
            if ROOT_NOTE_LOWEST <= note["pitch"] <= ROOT_NOTE_HIGHEST and note["position"] not in self.kick:
                self.kick.append(note["position"])  # remembering guitar accents to pass to the kick drum\

    @staticmethod
    def randomize_duration(position):
        duration = [0.25, 0.5, 1, 2]
        weights = [1.2, 3, 3, 1]  # chances of generating a respective duration
        allowed_duration = [dur for dur in duration if dur <= (4 - position)]

        allowed_weights = [weights[duration.index(dur)] for dur in allowed_duration]

        choice = random.choices(allowed_duration, weights=allowed_weights, k=1)[0]
        return choice

    def insert_notes(self, bar, position, current_duration):
        high_notes = self.current_scale[7:]
        chance = random.random()
        if chance < 0.7 and current_duration > 0.25 and position % 1 == 0 and current_duration < 2:  # add high notes
            # from the scale
            current_note = random.choice(high_notes)
            self.diversify_notes(current_note, bar, position, current_duration)
            return current_note
        else:  # add 0's with (optional) 5ths
            if (self.check_for_palm_mute(position, 14) is True or self.check_for_palm_mute(position, 12) is True) \
                    and current_duration >= 0.5 and self.ROOT_NOTE >= 35:
                fifth = {"pitch": self.ROOT_NOTE + 7, "duration": current_duration, "position": bar * 4 + position}
                self.notes_generated.append(fifth)
            return self.ROOT_NOTE

    def insert_rests(self, position):
        rest_probability = random.random()  # rests
        if rest_probability < 0.02 * len(self.root_notes_generated) and self.root_notes_generated[  # half note rest
            -1] == self.ROOT_NOTE and position % 1 == 0 and \
                self.recent_note == self.ROOT_NOTE and self.recent_duration > 0.5:
            position += 2
            self.root_notes_generated.clear()
            return position
        if rest_probability < 0.05 * len(self.root_notes_generated) and self.root_notes_generated[  # quarter note rest
            -1] == self.ROOT_NOTE and position % 0.5 == 0 and \
                self.recent_note == self.ROOT_NOTE and self.recent_duration > 0.5:
            position += 1
            self.root_notes_generated.clear()
            return position
        if rest_probability < 0.05 * len(self.root_notes_generated) and self.root_notes_generated[  # 8th note rest
            -1] == self.ROOT_NOTE and position % 0.5 == 0 and \
                self.recent_note == self.ROOT_NOTE and self.recent_duration >= 0.5:
            position += 0.5
            self.root_notes_generated.clear()
            return position
        return -1

    def diversify_notes(self, current_note, bar, position, current_duration):
        chance = random.random()
        interval = self.interval_randomizer(current_note)

        if current_duration == 1:
            if chance < 0.4:
                note = {
                    "pitch": interval,
                    "duration": current_duration - 0.5,
                    "position": bar * 4 + position + 0.5
                }
                self.notes_generated.append(note)

        if current_duration == 2:
            if chance < 0.66:
                note = {
                    "pitch": interval,
                    "duration": current_duration - 1,
                    "position": bar * 4 + position + 1
                }
                self.notes_generated.append(note)

    def interval_randomizer(self, current_note):
        interval = INTERVALS[random.choice(list(INTERVALS.keys()))]

        if self.current_scale.index(current_note) + interval > len(self.current_scale) - 1:
            return self.current_scale[self.current_scale.index(current_note) - interval]
        else:
            return self.current_scale[self.current_scale.index(current_note) + interval]

    def palm_mute(self, bar, position, duration):
        if duration <= 0.5:
            if bar == 0 and position == 0:
                # so that palm muting the very first note works
                pm = {"pitch": 14, "duration": duration / 4, "position": bar * 4 + position}
                self.notes_generated.append(pm)
            else:
                pm = {"pitch": 14, "duration": duration / 4, "position": bar * 4 + position - 0.05}
                self.notes_generated.append(pm)

            pm = {"pitch": 12, "duration": duration / 4, "position": bar * 4 + position + duration / 2}
            self.notes_generated.append(pm)

        else:  # palm mute a long note with a certain chance
            palm_mute_chance = random.random()
            if palm_mute_chance < 0.4 and position != 0:
                pm_on = {"pitch": 14, "duration": duration / 4, "position": bar * 4 + position - 0.05}
                self.notes_generated.append(pm_on)
                pm_off = {"pitch": 12, "duration": duration / 4, "position": bar * 4 + position + duration / 2}
                self.notes_generated.append(pm_off)

    def check_for_palm_mute(self, position, pitch, tolerance=0.075):
        for note in self.notes_generated:
            if abs(note["position"] - position) <= tolerance and note["pitch"] == pitch:
                return True
        return False
