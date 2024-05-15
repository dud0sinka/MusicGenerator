import velocity
import random

# position: 0.25 = 16th note, 0.5 = 8th note, 1 = 4th note. 1 bar has 16 positions
# duration: 0.25 = 16th, 0.5 = 8th, 1 = 4th
# we use bar * 4 because we count bars as 0, 1, 2..... but in terms of position 1 bar equals to 4
# MyMIDI.addNote(track,channel,pitch,position,duration,volume)

ROOT_NOTE = 0
ROOT_NOTE_LOWEST = 29
ROOT_NOTE_HIGHEST = 38
SCALES = {
    "MINOR_SCALE": [2, 1, 2, 2, 1, 2, 2],
    "PHRYGIAN_MODE": [1, 2, 2, 2, 1, 2, 2],
    "PHRYGIAN_DOMINANT_MODE": [1, 3, 1, 2, 1, 2, 2],
    "MAJOR_SCALE_WITH_RAISED_4TH": [2, 2, 2, 1, 2, 2, 1],
    "MAJOR_SCALE": [2, 2, 1, 2, 2, 2, 1],
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

kick = []  # guitar 0's are being passed here to match the kick
current_scale = []  # scale that was chosen
root_notes_generated = []  # amount of generated 0's is affecting the amount of rests

recent_note = 0  # keep track of the last note played
recent_duration = 0  # keep track of the duration of the lat note played
notes_generated = []  # all notes generated
consecutive_16ths = 0  # this variable is used to prevent the generation of singular 16th notes


# TODO: change the breakdown the second time it repeats, spice-up parts (octaves, runs, chords etc.)
# TODO: different types of breakdowns (this one is default / melodic)
# TODO: choose closest notes with higher chance
# TODO: dead notes

def choose_scale():
    scale = random.choice(list(SCALES.keys()))
    return SCALES[scale]


def fill_scale(current_note, scale):  # fill the scale with notes
    if ROOT_NOTE not in scale:
        current_scale.append(ROOT_NOTE)
    for i in scale:
        current_note += i
        current_scale.append(current_note)
        if current_note >= ROOT_NOTE + 31:  # restrict the scale to 2.5 octaves
            break


def generate_rhythm_guitar(file, number_of_bars):
    global recent_note, recent_duration, ROOT_NOTE, current_scale, consecutive_16ths

    ROOT_NOTE = random.randint(ROOT_NOTE_LOWEST, ROOT_NOTE_HIGHEST)
    print(ROOT_NOTE)

    lets_choose_a_scale = choose_scale()
    fill_scale(ROOT_NOTE, lets_choose_a_scale)
    fill_scale(ROOT_NOTE + 12, lets_choose_a_scale)
    fill_scale(ROOT_NOTE + 24, lets_choose_a_scale)
    print(current_scale)

    bar = 0
    for _ in range(number_of_bars):
        position = 0
        while position < 4:
            rest_probability = random.random()  # rests
            if rest_probability < 0.05 * len(root_notes_generated) and root_notes_generated[  # half note rest
                -1] == ROOT_NOTE and position % 1 == 0 and \
                    recent_note == ROOT_NOTE and recent_duration > 0.5:
                position += 2
                root_notes_generated.clear()
                continue
            if rest_probability < 0.1 * len(root_notes_generated) and root_notes_generated[  # quarter note rest
                -1] == ROOT_NOTE and position % 0.5 == 0 and \
                    recent_note == ROOT_NOTE and recent_duration > 0.5:
                position += 1
                root_notes_generated.clear()
                continue
            if rest_probability < 0.1 * len(root_notes_generated) and root_notes_generated[  # 8th note rest
                -1] == ROOT_NOTE and position % 0.5 == 0 and \
                    recent_note == ROOT_NOTE and recent_duration >= 0.5:
                position += 0.5
                root_notes_generated.clear()
                continue

            current_duration = randomize_duration(position)  # generate duration
            if consecutive_16ths % 2 != 0 and current_duration != 0.25:  # prevent singular 16th notes
                current_duration = 0.25
            if current_duration == 0.25:
                consecutive_16ths += 1
            else:
                consecutive_16ths = 0

            palm_mute(bar, position, current_duration, file)

            current_note = insert_notes(bar, position, current_duration, file)
            file.addNote(0, 0, current_note, bar * 4 + position, current_duration, velocity.main_velocity())
            root_notes_generated.append(current_note)
            note = {  # save a note with the following parameters to the history of generated notes
                "pitch": current_note,
                "duration": current_duration,
                "position": bar * 4 + position
            }
            notes_generated.append(note)

            if current_note > 48 and position != 0:  # optional kick for higher notes
                if random.random() < 0.4:
                    kick.append(bar * 4 + position)
            else:
                kick.append(bar * 4 + position)  # remembering guitar accents to pass to the kick drum

            position += current_duration

            recent_note = current_note
            recent_duration = current_duration

        bar += 1


def randomize_duration(position):
    duration = [0.25, 0.5, 1, 2]
    weights = [1.2, 3, 3, 2]  # chances of generating a respective duration
    allowed_duration = [dur for dur in duration if dur <= (4 - position)]

    allowed_weights = [weights[duration.index(dur)] for dur in allowed_duration]

    choice = random.choices(allowed_duration, weights=allowed_weights, k=1)[0]
    return choice


def insert_notes(bar, position, current_duration, file):
    high_notes = current_scale[7:]
    chance = random.random()
    if chance < 0.7 and current_duration > 0.25 and position % 1 == 0:  # add high notes from the scale
        current_note = random.choice(high_notes)
        diversify_notes(current_note, bar, position, current_duration, file)
        return current_note
    else:  # add 0's with (optional) 5ths
        if (check_for_palm_mute(position, 14) is True or check_for_palm_mute(position, 12) is True) and current_duration >= 0.5 and ROOT_NOTE >= 35:
            file.addNote(0, 0, ROOT_NOTE + 7, bar * 4 + position, current_duration, velocity.main_velocity())
        return ROOT_NOTE


def diversify_notes(current_note, bar, position, current_duration, file):
    chance = random.random()
    interval = interval_randomizer(current_note)

    if current_duration == 1:
        if chance < 0.4:
            file.addNote(0, 0, interval, bar * 4 + position + 0.5, current_duration - 0.5,
                         velocity.main_velocity())
            note = {
                "pitch": interval,
                "duration": current_duration,
                "position": bar * 4 + position
            }
            notes_generated.append(note)

    if current_duration == 2:
        if chance < 0.66:
            file.addNote(0, 0, interval, bar * 4 + position + 1, current_duration - 1,
                         velocity.main_velocity())
            note = {
                "pitch": interval,
                "duration": current_duration,
                "position": bar * 4 + position
            }
            notes_generated.append(note)


def interval_randomizer(current_note):
    interval = INTERVALS[random.choice(list(INTERVALS.keys()))]

    if current_scale.index(current_note) + interval > len(current_scale) - 1:
        return current_scale[current_scale.index(current_note) - interval]
    else:
        return current_scale[current_scale.index(current_note) + interval]


def palm_mute(bar, position, duration, file):
    if duration <= 0.5:
        if bar == 0 and position == 0:
            file.addNote(0, 0, 14, bar * 4 + position, duration / 4, velocity.main_velocity())
            # so that palm muting the very first note works
        else:
            file.addNote(0, 0, 14, bar * 4 + position - 0.075, duration / 4, velocity.main_velocity())
        file.addNote(0, 0, 12, bar * 4 + position + duration / 2 - 0.075, duration / 4, velocity.main_velocity())
        note = {
            "pitch": 14,
            "duration": duration,
            "position": bar * 4 + position
        }
        notes_generated.append(note)
    else:  # palm mute a long note with a certain chance
        palm_mute_chance = random.random()
        if palm_mute_chance < 0.4:
            note = {
                "pitch": 14,
                "duration": duration,
                "position": bar * 4 + position
            }
            notes_generated.append(note)
            file.addNote(0, 0, 14, bar * 4 + position - 0.075, duration / 4, velocity.main_velocity())
            file.addNote(0, 0, 12, bar * 4 + position + duration / 2 - 0.075, duration / 4, velocity.main_velocity())


def check_for_palm_mute(position, pitch, tolerance=0.075):
    for note in notes_generated:
        if abs(note["position"] - position) <= tolerance and note["pitch"] == pitch:
            return True
    return False
