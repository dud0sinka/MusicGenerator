import random

from generate_song import GenerateSong


def generate(r_gtr_MIDI, dr_MIDI, bass_MIDI, l_gtr_MIDI, amb_MIDI):
    song = GenerateSong(r_gtr_MIDI, dr_MIDI, bass_MIDI, l_gtr_MIDI, amb_MIDI)

    #######intro#######
    position = song.generate_intro()
    song.start_pos = position
    #######verse_1#######
    position = song.generate_verse()
    song.start_pos = position
    #######pre_chorus_1#######
    position = song.generate_pre_chorus()
    song.start_pos = position
    #######chorus_1#######
    position = song.generate_chorus()
    song.start_pos = position
    #######post_chorus_1#######
    position = song.generate_post_chorus()
    song.start_pos = position
    #######verse_2#######
    position = song.generate_verse(2)
    song.start_pos = position
    #######pre_chorus_2_optional#######
    if random.random() < 0.45:
        position = song.generate_pre_chorus()
    song.start_pos = position
    #######chorus_2_optional#######
    position = song.generate_chorus()
    song.start_pos = position
    #######pre_breakdown#######
    position = song.generate_pre_breakdown()
    song.start_pos = position
    #######breakdown#######
    position = song.generate_breakdown()
    song.start_pos = position
    #######chorus_3_optional#######
    position = song.generate_chorus()
    song.start_pos = position
    #######outro#######
    song.generate_outro()