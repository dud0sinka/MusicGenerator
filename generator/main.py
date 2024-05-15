from midiutil import MIDIFile
from drums import drums_main as dr
from rhythm_guitar import generate_default_breakdown as rg
from bass import bass_main as b

r_gtr_MIDI = MIDIFile(1)
r_gtr_MIDI.addTempo(0, 0, 180)
number_of_bars = 4

dr_MIDI = MIDIFile(1)
dr_MIDI.addTempo(0, 0, 160)

bass_MIDI = MIDIFile(1)
bass_MIDI.addTempo(0, 0, 160)

rg.generate_rhythm_guitar(r_gtr_MIDI, number_of_bars)
dr.generate_drums(dr_MIDI, number_of_bars)
b.copy_guitar(bass_MIDI)

with open("rhythm_guitar.mid", "wb") as output_file:
    r_gtr_MIDI.writeFile(output_file)

with open("drums.mid", "wb") as output_file:
    dr_MIDI.writeFile(output_file)

with open("bass.mid", "wb") as output_file:
    bass_MIDI.writeFile(output_file)

