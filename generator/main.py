from midiutil import MIDIFile
from rhythm_guitar.breakdown import default_melodic
from rhythm_guitar.intro import open0_drum_fill
from rhythm_guitar.verse import pedal_tone_riff
from rhythm_guitar.pre_chorus import chord_prog_breakdown
from rhythm_guitar.chorus import chorus

r_gtr_MIDI = MIDIFile(1)
dr_MIDI = MIDIFile(1)
bass_MIDI = MIDIFile(1)
l_gtr_MIDI = MIDIFile(1)

####intro#####
intro = open0_drum_fill.RGuitarIntoOpen0DrumFill()
intro_bars = 4  # 4 or 2
pos = intro.generate(r_gtr_MIDI, dr_MIDI, bass_MIDI, intro_bars)
root = intro.get_root()
#####verse####
verse_bars = 4  # 4
verse = pedal_tone_riff.RGuitarPedalToneRiff(pos, root)
pos = verse.generate(r_gtr_MIDI, dr_MIDI, bass_MIDI, verse_bars, 4)
####pre-chorus####
pos = chord_prog_breakdown.generate(r_gtr_MIDI, dr_MIDI, bass_MIDI, pos, root, verse.progression, verse.current_scale)
####chorus####
chorus_bars = 4  # reps 4
chorus = chorus.RGuitarChorus(pos, root)
pos = chorus.generate(r_gtr_MIDI, dr_MIDI, bass_MIDI, chorus_bars, 4, l_gtr_MIDI)
####breakdown#####
breakdown_repetitions = 4  # reps 4
breakdown = default_melodic.RGuitarDefaultMelodicBreakdown(pos, root, None, None, l_gtr_MIDI)
breakdown.generate(r_gtr_MIDI, dr_MIDI, bass_MIDI, 4, breakdown_repetitions)  # add variation

# TODO: pre-breakdown two bars of melodic br guitar
with open("midis/rhythm_guitar.mid", "wb") as output_file:
    r_gtr_MIDI.writeFile(output_file)

with open("midis/drums.mid", "wb") as output_file:
    dr_MIDI.writeFile(output_file)

with open("midis/bass.mid", "wb") as output_file:
    bass_MIDI.writeFile(output_file)

with open("midis/lead.mid", "wb") as output_file:
    l_gtr_MIDI.writeFile(output_file)
