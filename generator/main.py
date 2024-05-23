from midiutil import MIDIFile
import generate_song
import structure_elements
from bass import bass_default_breakdown as b
#  tempo

r_gtr_MIDI = MIDIFile(1)
number_of_bars = 8

dr_MIDI = MIDIFile(1)
bass_MIDI = MIDIFile(1)

generate_song.generate_section("breakdown", "default_melodic", 4, r_gtr_MIDI, dr_MIDI)
b.copy_guitar(bass_MIDI)
# structure_elements.pick_structure()


with open("midis/rhythm_guitar.mid", "wb") as output_file:
    r_gtr_MIDI.writeFile(output_file)

with open("midis/drums.mid", "wb") as output_file:
    dr_MIDI.writeFile(output_file)

with open("midis/bass.mid", "wb") as output_file:
    bass_MIDI.writeFile(output_file)

