from midiutil import MIDIFile

from misc import generate_main

r_gtr_MIDI = MIDIFile(1)
dr_MIDI = MIDIFile(1)
bass_MIDI = MIDIFile(1)
l_gtr_MIDI = MIDIFile(1)
amb_MIDI = MIDIFile(1)

generate_main.generate(r_gtr_MIDI, dr_MIDI, bass_MIDI, l_gtr_MIDI, amb_MIDI)

with open("midis/rhythm_guitar.mid", "wb") as output_file:
    r_gtr_MIDI.writeFile(output_file)
with open("midis/drums.mid", "wb") as output_file:
    dr_MIDI.writeFile(output_file)
with open("midis/bass.mid", "wb") as output_file:
    bass_MIDI.writeFile(output_file)
with open("midis/lead.mid", "wb") as output_file:
    l_gtr_MIDI.writeFile(output_file)
with open("midis/amb.mid", "wb") as output_file:
    amb_MIDI.writeFile(output_file)
