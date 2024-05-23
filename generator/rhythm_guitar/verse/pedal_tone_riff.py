import random
from rhythm_guitar import common_stuff as common
import velocity

SCALES = {
    "MINOR_SCALE": [2, 1, 2, 2, 1, 2, 2],
    "PHRYGIAN_MODE": [1, 2, 2, 2, 1, 2, 2],
    "HARMONIC_MINOR_SCALE": [2, 1, 2, 2, 1, 3, 1],
    "DORIAN_MODE": [2, 1, 2, 2, 2, 1, 2],
}

# TODO: second repeat is either stuff from todo in breakdown or just different random notes
# TODO: if its 0 0 0 0 8 8 7 7 then modify each segment's end

MODES = ["default", "progression"]
CHORD_PROGRESSIONS = {  # the numbers are the intervals to add to the current root note
    "verse_1": [0, 0, 5, 4],  # 0 0 8 7
}


def generate(number_of_bars, file, data):
    current_scale = []  # scale that was chosen
    last_notes = []  # note history

    print("VERSE:")
    root_note = data["scale"][0]
    starting_position = data["position"]
    lets_choose_a_scale = common.choose_scale(SCALES)
    common.fill_scale(root_note, lets_choose_a_scale, current_scale, root_note)
    mode = choose_mode()
    progression = CHORD_PROGRESSIONS["verse_1"]
    print(current_scale)
    print(starting_position)

    bar = 0
    for _ in range(number_of_bars):
        current_root_note = set_root_note(current_scale, mode, bar, progression)
        print(current_root_note)
        position = 0
        while position < 4:
            last_notes = insert_notes(bar, position, current_root_note, file, starting_position, current_scale,
                                      last_notes)
            position += 0.5
        bar += 1


def insert_notes(bar, position, root_note, file, starting_position, current_scale, last_notes):
    if len(last_notes) >= 2 and last_notes[-1] >= current_scale[7] and last_notes[-2] >= current_scale[7]:  # no more
        # than two consecutive high notes
        note = root_note
    else:
        chance = random.random()
        if chance < 0.51:
            note = root_note
        else:
            note = random.choice(current_scale[7:])

    file.addNote(0, 0, note, bar * 4 + position + starting_position, 0.5, velocity.main_velocity())

    if note == root_note:  # palm mute the root notes
        if bar == 0 and position == 0:
            file.addNote(0, 0, 14, bar * 4 + position + starting_position, 0.125, velocity.main_velocity())
            # so that palm muting the very first note works
        else:
            file.addNote(0, 0, 14, bar * 4 + position - 0.075 + starting_position, 0.125, velocity.main_velocity())
        file.addNote(0, 0, 12, bar * 4 + position + 0.5 / 2 - 0.075 + starting_position, 0.5 / 4,
                     velocity.main_velocity())

    last_notes.append(note)

    return last_notes


def choose_mode():
    return random.choice(MODES)


def set_root_note(current_scale, mode, bar, progression):  # choose current root note for pedal tone riffs
    if mode == "default":
        return current_scale[0]
    else:
        return current_scale[progression[bar]]
