import time
import digitalio
import board
import usb_midi
import adafruit_midi
from adafruit_midi.midi_message import MIDIUnknownEvent
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.control_change import ControlChange

LED = 25
led = None

RELAYS = [board.GP20, board.GP18, board.GP19]
relays = []

midi_in = None

pressed_midi = []
current_keys = [0, 0, 0]

map_midi_to_keys = {
    64: [1, 1, 1],
    65: [1, 0, 1],
    66: [0, 1, 1],
    67: [1, 1, 0],
    68: [1, 0, 0],
    69: [0, 1, 0],
    70: [0, 0, 0], #Bb

    71: [1, 1, 1],
    72: [1, 0, 1],
    73: [0, 1, 1],
    74: [1, 1, 0],
    75: [1, 0, 0],
    76: [0, 1, 0],
    77: [0, 0, 0], #F

    78: [0, 1, 1],
    79: [1, 1, 0],
    80: [1, 0, 0],
    81: [0, 1, 0],
    82: [0, 0, 0], #Bb

    83: [1, 1, 0],
    84: [1, 0, 0],
    85: [0, 1, 0],
    86: [0, 0, 0], #D

    87: [1, 0, 0],
    88: [0, 1, 0],
    89: [0, 0, 0], #F

    90: [0, 1, 0],
    91: [0, 0, 0], #Ab
}

def init():
    global relays, midi_in
    for r in RELAYS:
        p = digitalio.DigitalInOut(r)
        p.direction = digitalio.Direction.OUTPUT
        p.value = False
        relays.append(p)
    midi_in = adafruit_midi.MIDI(midi_in=usb_midi.ports[0], midi_out=None, in_channel=(0,1,2))

def set_solenoid(index: int, state: bool):
    print(f"set_solenoid: {index}:{state}")
    relays[index].value = state

def control_manual(msg):
    if isinstance(msg, NoteOn):
        set_solenoid(msg.note - 48 + 0, True)
    elif isinstance(msg, NoteOff):
        set_solenoid(msg.note - 48 + 0, False)
    else:
        pass

def insert_midi(midi):
    global pressed_midi
    position = 0
    while position < len(pressed_midi) and pressed_midi[position] < midi:
        position += 1
    pressed_midi.insert(position, midi)

def remove_midi(midi):
    global pressed_midi
    try:
        pressed_midi.remove(midi)
    except ValueError:
        print(f"remove_number: {midi} is not in the list")

def control_automatic(msg):
    global pressed_midi
    if isinstance(msg, NoteOn):
        insert_midi(msg.note)
    elif isinstance(msg, NoteOff):
        remove_midi(msg.note)
    else:
        pass
    pass

    print(pressed_midi)
    if len(pressed_midi) > 0:
        keys = map_midi_to_keys[pressed_midi[-1]]
        if current_keys[0] != keys[0]:
            current_keys[0] = keys[0]
            set_solenoid(0, bool(keys[0]))
        if current_keys[1] != keys[1]:
            current_keys[1] = keys[1]
            set_solenoid(1, bool(keys[1]))
        if current_keys[2] != keys[2]:
            current_keys[2] = keys[2]
            set_solenoid(2, bool(keys[2]))
    else:
        print("turn off")
        if current_keys[0] != 0:
            current_keys[0] = 0
            set_solenoid(0, False)
        if current_keys[1] != 0:
            current_keys[1] = 0
            set_solenoid(1, False)
        if current_keys[2] != 0:
            current_keys[2] = 0
            set_solenoid(2, False)


def check_midi_in():
    msg = midi_in.receive()

    if msg is not None and hasattr(msg, 'note'):
        print(f"check_midi_in: {msg}")
        if msg.channel == 1 and msg.note in [48, 49, 50]:
            control_manual(msg)
        elif msg.channel == 0 and msg.note >= 64 and msg.note <= 91:
            control_automatic(msg)

def loop():
    while True:
        check_midi_in()

def test():
    init()
    loop()
