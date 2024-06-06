from midiutil import MIDIFile
from rhythm_guitar.breakdown import default_melodic
from rhythm_guitar.intro import open0_drum_fill
#  tempo

r_gtr_MIDI = MIDIFile(1)
number_of_bars = 8

dr_MIDI = MIDIFile(1)
bass_MIDI = MIDIFile(1)

# generate_song.generate_section("breakdown", "default_melodic", 4, r_gtr_MIDI, dr_MIDI)
# b.copy_guitar(bass_MIDI)
# structure_elements.pick_structure()
# intro.generate(4, r_gtr_MIDI)
# drumintro.generate(4, dr_MIDI)
test1 = open0_drum_fill.RGuitarIntoOpen0DrumFill()
pos = test1.generate(r_gtr_MIDI, dr_MIDI, bass_MIDI, 4)
root = test1.get_root()
test = default_melodic.RGuitarDefaultMelodicBreakdown(pos, root)
test.generate(r_gtr_MIDI, dr_MIDI, bass_MIDI, 4, 4)

with open("midis/rhythm_guitar.mid", "wb") as output_file:
    r_gtr_MIDI.writeFile(output_file)

with open("midis/drums.mid", "wb") as output_file:
    dr_MIDI.writeFile(output_file)

with open("midis/bass.mid", "wb") as output_file:
    bass_MIDI.writeFile(output_file)

