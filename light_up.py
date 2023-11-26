import time
import rtmidi

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(port)
else:
    midiout.open_virtual_port("My virtual output")

with midiout:
    # channel 1, middle C, velocity 112
    note_on = [0x90, 81, 112]
    note_off = [0x90, 81, 0]
    midiout.send_message(note_on)
    time.sleep(0.5)
    midiout.send_message(note_off)
    time.sleep(0.1)

del midiout