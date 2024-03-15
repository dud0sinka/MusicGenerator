from midiutil import MIDIFile
from drums import generate_drums

file = MIDIFile(1)
file.addTempo(0, 0, 160)
number_of_bars = 64

generate_drums(file, number_of_bars)

with open("output.mid", "wb") as output_file:
    file.writeFile(output_file)
