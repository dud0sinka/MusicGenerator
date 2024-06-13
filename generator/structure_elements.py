import random

song_structure_elements = {
    "intro": {"none": {0}, "open0_drum_fill": {2, 4}, "drum_fill": {1, 2}, "smth": {1, 2},
              "strings_smth": {4}, "halfbar_chug_octaves": {4, 8}},
    "verse1": {"pedal_tone_riff": {4, 8}, "open_string_riff": {4}, "tremolo_chord_root": {4},
               "tremolo_three_notes": {4, 8}},
    "pre-chorus1": {"lofi_verse_halfbar_chug": {4: {2, 4}}, "triplet_pm0_chugs_optional_lower_notes": {4: {2, 4}},
                    "rest": {1}, "none": {0}, "chord_prog_breakdown": {4: {2, 4}}},
    "chorus": {"chord_prog": {4, 8}},
    "post-chorus": {"not_chosen_pre_chorus": {}},
    "verse2": {"same_as_first_var": {}},
    "pre-chorus2": {"same_as_first": {}, "none": {0}},
    "chorus2": {"same": {}, "same_extended_chugging": {}, "same_ext_chug_diff_prog": {}},
    "bridge": {"chug_rest": {4, 8}, "none": {0}, "pm0_toms_056_lead": {4}, "intro": {}},
    "breakdown": {"default_melodic": {4}, "4th8th_chugs_dissonance_rests": {4, 8}, "slow_rests_4th8th": {4, 8},
                  "chromatic_double_time": {4, 8}},
    "verse3": {"none": {0}, "same_as_first": {0}},
    "pre-chorus3": {"same_as_first": {}, "none": {0}},
    "chorus3": {"none": {0}, "chorus2": {}},
    "outro": {"verse_loop_chug": {5}, "chug": {1}, "long_0": {4}}
}

# TODO: everything is guitar-based, each guitar section / repetition calls to other functions for variations and/or
#  additions (both for guitar and drum parts)
# TODO: each section type has its own set of allowed variations
# if pre-breakdown is intro drum fill then stop at 3 with a kick and tom snare hit
# smth is variations / spice-ups
#

endings = {

}


def pick_structure():
    total_bars = 0
    for section, choices in song_structure_elements.items():
        chosen_element = random.choice(list(choices.keys()))
        print(f"{section}: {chosen_element}")

        if choices[chosen_element]:  # Check if the set of possible bar counts is not empty
            chosen_bars = random.choice(list(choices[chosen_element]))
            total_bars += chosen_bars
            print(f"{chosen_bars}")
        else:
            print(f"x")

    print(f"Total bars: {total_bars}")

