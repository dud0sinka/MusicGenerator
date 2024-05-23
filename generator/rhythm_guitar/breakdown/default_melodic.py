import velocity
import random
from rhythm_guitar import common_stuff as common

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

start_position = 0

# TODO: change the breakdown the second time it repeats, spice-up parts (octaves, runs, chords etc.)
# TODO: different types of breakdowns (this one is default / melodic)
# TODO: choose closest notes with higher chance
# TODO: dead notes


def generate(file, number_of_bars, repetitions):
    global recent_note, recent_duration, ROOT_NOTE, current_scale, consecutive_16ths
    print("BREAKDOWN:")
    ROOT_NOTE = random.randint(ROOT_NOTE_LOWEST, ROOT_NOTE_HIGHEST)
    ending_position = 0

    lets_choose_a_scale = common.choose_scale(SCALES)
    common.fill_scale(ROOT_NOTE, lets_choose_a_scale, current_scale, ROOT_NOTE)
    print(current_scale)

    bar = start_position
    for _ in range(number_of_bars):
        generate_bar(bar)
        bar += 1
        ending_position = bar * 4

    create_kick_pattern()
    repeat(ending_position, repetitions)

    print(notes_generated)
    add_to_file(file)
    data = {"position": ending_position, "scale": current_scale, "bars": number_of_bars, "repetitions": repetitions}
    return data


def generate_bar(bar):
    global consecutive_16ths, recent_note, recent_duration
    position = 0
    while position < 4:

        position_copy = position
        position = insert_rests(position)
        if position == -1:
            position = position_copy
        else:
            continue

        current_duration = randomize_duration(position)  # generate duration
        if consecutive_16ths % 2 != 0 and current_duration != 0.25:  # prevent singular 16th notes
            current_duration = 0.25
        if current_duration == 0.25:
            consecutive_16ths += 1
        else:
            consecutive_16ths = 0

        palm_mute(bar, position, current_duration)

        current_note = insert_notes(bar, position, current_duration)
        root_notes_generated.append(current_note)
        note = {  # save a note with the following parameters to the history of generated notes
            "pitch": current_note,
            "duration": current_duration,
            "position": bar * 4 + position
        }
        notes_generated.append(note)

        position += current_duration

        recent_note = current_note
        recent_duration = current_duration


def add_to_file(file):
    for note in notes_generated:
        file.addNote(0, 0, note["pitch"], note["position"], note["duration"], velocity.main_velocity())


def repeat(ending_position, repetitions):
    notes_to_repeat = notes_generated.copy()
    for current_repeat in range(1, repetitions):  # Start from 1, as we've already generated the first section
        # Make a copy of the current notes_generated list
        print(current_repeat)
        for note in notes_to_repeat:
            notes_generated.append({"pitch": note["pitch"], "duration": note["duration"],
                                    "position": note["position"] + ending_position * current_repeat})


def create_kick_pattern():
    for note in notes_generated:
        if note["position"] == 0 and note["position"] not in kick:
            kick.append(0)
            continue
        if note["pitch"] > ROOT_NOTE_HIGHEST and note["position"] not in kick:  # optional kick for higher notes
            if random.random() < 0.4:
                kick.append(note["position"])
            continue
        if ROOT_NOTE_LOWEST <= note["pitch"] <= ROOT_NOTE_HIGHEST and note["position"] not in kick:
            kick.append(note["position"])  # remembering guitar accents to pass to the kick drum\


def randomize_duration(position):
    duration = [0.25, 0.5, 1, 2]
    weights = [1.2, 3, 3, 1]  # chances of generating a respective duration
    allowed_duration = [dur for dur in duration if dur <= (4 - position)]

    allowed_weights = [weights[duration.index(dur)] for dur in allowed_duration]

    choice = random.choices(allowed_duration, weights=allowed_weights, k=1)[0]
    return choice


def insert_notes(bar, position, current_duration):
    high_notes = current_scale[7:]
    chance = random.random()
    if chance < 0.7 and current_duration > 0.25 and position % 1 == 0 and current_duration < 2:  # add high notes
        # from the scale
        current_note = random.choice(high_notes)
        diversify_notes(current_note, bar, position, current_duration)
        return current_note
    else:  # add 0's with (optional) 5ths
        if (check_for_palm_mute(position, 14) is True or check_for_palm_mute(position, 12) is True) \
                and current_duration >= 0.5 and ROOT_NOTE >= 35:
            fifth = {"pitch": ROOT_NOTE + 7, "duration": current_duration, "position": bar * 4 + position}
            notes_generated.append(fifth)
        return ROOT_NOTE


def insert_rests(position):
    global root_notes_generated
    rest_probability = random.random()  # rests
    if rest_probability < 0.02 * len(root_notes_generated) and root_notes_generated[  # half note rest
        -1] == ROOT_NOTE and position % 1 == 0 and \
            recent_note == ROOT_NOTE and recent_duration > 0.5:
        position += 2
        root_notes_generated.clear()
        return position
    if rest_probability < 0.05 * len(root_notes_generated) and root_notes_generated[  # quarter note rest
        -1] == ROOT_NOTE and position % 0.5 == 0 and \
            recent_note == ROOT_NOTE and recent_duration > 0.5:
        position += 1
        root_notes_generated.clear()
        return position
    if rest_probability < 0.05 * len(root_notes_generated) and root_notes_generated[  # 8th note rest
        -1] == ROOT_NOTE and position % 0.5 == 0 and \
            recent_note == ROOT_NOTE and recent_duration >= 0.5:
        position += 0.5
        root_notes_generated.clear()
        return position
    return -1


def diversify_notes(current_note, bar, position, current_duration):
    chance = random.random()
    interval = interval_randomizer(current_note)

    if current_duration == 1:
        if chance < 0.4:
            note = {
                "pitch": interval,
                "duration": current_duration - 0.5,
                "position": bar * 4 + position + 0.5
            }
            notes_generated.append(note)

    if current_duration == 2:
        if chance < 0.66:
            note = {
                "pitch": interval,
                "duration": current_duration - 1,
                "position": bar * 4 + position + 1
            }
            notes_generated.append(note)


def interval_randomizer(current_note):
    interval = INTERVALS[random.choice(list(INTERVALS.keys()))]

    if current_scale.index(current_note) + interval > len(current_scale) - 1:
        return current_scale[current_scale.index(current_note) - interval]
    else:
        return current_scale[current_scale.index(current_note) + interval]


def palm_mute(bar, position, duration):
    if duration <= 0.5:
        if bar == 0 and position == 0:
            # so that palm muting the very first note works
            pm = {"pitch": 14, "duration": duration / 4, "position": bar * 4 + position}
            notes_generated.append(pm)
        else:
            pm = {"pitch": 14, "duration": duration / 4, "position": bar * 4 + position - 0.075}
            notes_generated.append(pm)

        pm = {"pitch": 12, "duration": duration / 4, "position": bar * 4 + position + duration / 2 - 0.075}
        notes_generated.append(pm)

    else:  # palm mute a long note with a certain chance
        palm_mute_chance = random.random()
        if palm_mute_chance < 0.4 and position != 0:
            pm_on = {"pitch": 14, "duration": duration / 4, "position": bar * 4 + position - 0.075}
            notes_generated.append(pm_on)
            pm_off = {"pitch": 12, "duration": duration / 4, "position": bar * 4 + position + duration / 2 - 0.075}
            notes_generated.append(pm_off)


def check_for_palm_mute(position, pitch, tolerance=0.075):
    for note in notes_generated:
        if abs(note["position"] - position) <= tolerance and note["pitch"] == pitch:
            return True
    return False
