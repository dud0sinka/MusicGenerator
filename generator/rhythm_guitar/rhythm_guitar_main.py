import velocity
import random

# position: 0.25 = 16th note, 0.5 = 8th note, 1 = 4th note. 1 bar has 16 positions
# duration: 0.25 = 16th, 0.5 = 8th, 1 = 4th
# we use bar * 4 because we count bars as 0, 1, 2..... but in terms of position 1 bar equals to 4
# MyMIDI.addNote(track,channel,pitch,position,duration,volume)

kick = []


def generate_rhythm_guitar(file, number_of_bars):
    bar = 0
    for _ in range(number_of_bars):
        position = 0
        while position < 4:
            current_duration = randomize_duration(position)

            palm_mute(bar, position, current_duration, file)

            file.addNote(0, 0, 34, bar * 4 + position, current_duration, velocity.main_velocity())

            kick.append(bar * 4 + position)  # remembering guitar accents to pass to the kick drum
            position += current_duration

        bar += 1


def randomize_duration(position):
    duration = [0.25, 0.5, 1, 2]
    allowed_duration = [dur for dur in duration if dur <= (4 - position)]
    choice = random.choice(allowed_duration)
    return choice


def palm_mute(bar, position, duration, file):
    if duration <= 0.5:
        if bar == 0 and position == 0:
            file.addNote(0, 0, 14, bar * 4 + position, duration / 4, velocity.main_velocity())
            # so that palm muting the very first note works
        else:
            file.addNote(0, 0, 14, bar * 4 + position - 0.075, duration / 4, velocity.main_velocity())

        file.addNote(0, 0, 12, bar * 4 + position + duration / 2 - 0.075, duration / 4, velocity.main_velocity())
    else:  # palm mute a long note with a certain chance
        palm_mute_chance = random.random()
        if palm_mute_chance < 0.4:
            file.addNote(0, 0, 14, bar * 4 + position - 0.075, duration / 4, velocity.main_velocity())
            file.addNote(0, 0, 12, bar * 4 + position + duration / 2 - 0.075, duration / 4, velocity.main_velocity())