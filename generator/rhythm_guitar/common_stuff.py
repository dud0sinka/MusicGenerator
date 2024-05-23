import random


def choose_scale(SCALES):
    scale = random.choice(list(SCALES.keys()))
    return SCALES[scale]


def fill_scale(current_note, scale, current_scale, ROOT_NOTE):  # fill the scale with notes
    if ROOT_NOTE not in scale:
        current_scale.append(ROOT_NOTE)
    for _ in range(2):
        for i in scale:
            current_note += i
            current_scale.append(current_note)
            if current_note >= ROOT_NOTE + 31:  # restrict the scale to 2.5 octaves
                break
        ROOT_NOTE += 12
    return current_scale
