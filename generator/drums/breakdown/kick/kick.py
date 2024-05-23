from rhythm_guitar.breakdown.default_melodic import kick
import velocity
import random


def default_kick(repetition, file, bars):  # follows the pattern of the guitar
    print(kick)
    print(bars*4*repetition)
    for i in kick:
        file.addNote(0, 0, 36, i + bars * 4 * repetition, 0.25, velocity.main_velocity())


def four_on_the_floor(repetition, file, bars):  # tun tsh tun tsh tun tsh tun tsh
    for i in range(0, bars * 4):
        if i % 4 == 0:
            file.addNote(0, 0, 36, i + bars * 4 * repetition, 0.25, velocity.main_velocity())
        if i % 2 == 0 and i != 0:
            kick_bursts_before_snare(repetition, file, bars, i)


def kick_bursts_before_snare(repetition, file, bars, i, variation=4):  # occasional kick bursts before snare
    burst_chance = random.random()
    if burst_chance < 0.4 / variation:
        if variation == 2:
            file.addNote(0, 0, 36, i + bars * 4 * repetition, 0.25, velocity.main_velocity())
        file.addNote(0, 0, 36, i + bars * 4 * repetition - 0.25, 0.25, velocity.main_velocity())
        file.addNote(0, 0, 36, i + bars * 4 * repetition - 0.5, 0.25, velocity.main_velocity())
        if variation == 4:
            kicks_after_snare(repetition, file, bars, i)

    if burst_chance < 0.2 / variation:
        file.addNote(0, 0, 36, i + bars * 4 * repetition - 0.75, 0.25, velocity.main_velocity())
        file.addNote(0, 0, 36, i + bars * 4 * repetition - 1, 0.25, velocity.main_velocity())
        if variation == 4:
            kicks_after_snare(repetition, file, bars, i)


def kicks_after_snare(repetition, file, bars, i):  # occasional kicks after snare
    kick_after_snare_chance = random.random()
    available_positions = [0.5, 0.75, 1, 1.5]

    if kick_after_snare_chance < 0.25:
        position = random.choice(available_positions)
        file.addNote(0, 0, 36, i + bars * 4 * repetition + position, 0.25, velocity.main_velocity())
        available_positions.remove(position)
        if position == 0.75:
            file.addNote(0, 0, 36, i + bars * 4 * repetition + 1.5, 0.25, velocity.main_velocity())
            kick_after_snare_chance = 1
    if kick_after_snare_chance < 0.15:
        position = random.choice(available_positions)
        file.addNote(0, 0, 36, i + bars * 4 * repetition + position, 0.25, velocity.main_velocity())
        available_positions.remove(position)
    if kick_after_snare_chance < 0.1:
        position = random.choice(available_positions)
        file.addNote(0, 0, 36, i + bars * 4 * repetition + position, 0.25, velocity.main_velocity())
        available_positions.remove(position)


def double_bass(repetition, file, bars):  # double bass kick pattern (brrrrrrrrrrrrrr)
    for i in range(0, bars * 4):
        j = 0
        for _ in range(4):
            file.addNote(0, 0, 36, i + bars * 4 * repetition + j, 0.25, velocity.double_bass_velocity())
            j += 0.25


def eighth_kicks(repetition, file, bars):  # tu tu tu tu tu tu tu tu
    for i in range(0, bars * 4):
        j = 0
        for _ in range(2):
            file.addNote(0, 0, 36, i + bars * 4 * repetition + j, 0.25, velocity.double_bass_velocity())
            j += 0.5
            if i % 2 == 0 and i != 0:
                kick_bursts_before_snare(repetition, file, bars, i, 8)


def two_on_the_floor(repetition, file, bars):  # tun     tsh     tun     tsh
    for i in range(0, bars * 4):
        if i % 8 == 0:
            file.addNote(0, 0, 36, i + bars * 4 * repetition, 0.25, velocity.main_velocity())
        if i % 2 == 0 and i != 0:
            kick_bursts_before_snare(repetition, file, bars, i, 2)
