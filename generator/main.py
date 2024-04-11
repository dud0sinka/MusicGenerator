from midiutil import MIDIFile
from drums import drums_main as dr
from rhythm_guitar import rhythm_guitar_main as rg

r_gtr_MIDI = MIDIFile(1)
r_gtr_MIDI.addTempo(0, 0, 160)
number_of_bars = 8

dr_MIDI = MIDIFile(1)
dr_MIDI.addTempo(0, 0, 160)

rg.generate_rhythm_guitar(r_gtr_MIDI, number_of_bars)
dr.generate_drums(dr_MIDI, number_of_bars)

with open("rhythm_guitar.mid", "wb") as output_file:
    r_gtr_MIDI.writeFile(output_file)

with open("drums.mid", "wb") as output_file:
    dr_MIDI.writeFile(output_file)
