from collections import defaultdict


DATA = {
    0x80: ("Chan 1 Note off", "Note", "Velocity"),
    0x81: ("Chan 2 Note off", "Note", "Velocity"),
    0x82: ("Chan 3 Note off", "Note", "Velocity"),
    0x83: ("Chan 4 Note off", "Note", "Velocity"),
    0x84: ("Chan 5 Note off", "Note", "Velocity"),
    0x85: ("Chan 6 Note off", "Note", "Velocity"),
    0x86: ("Chan 7 Note off", "Note", "Velocity"),
    0x87: ("Chan 8 Note off", "Note", "Velocity"),
    0x88: ("Chan 9 Note off", "Note", "Velocity"),
    0x89: ("Chan 10 Note off", "Note", "Velocity"),
    0x8A: ("Chan 11 Note off", "Note", "Velocity"),
    0x8B: ("Chan 12 Note off", "Note", "Velocity"),
    0x8C: ("Chan 13 Note off", "Note", "Velocity"),
    0x8D: ("Chan 14 Note off", "Note", "Velocity"),
    0x8E: ("Chan 15 Note off", "Note", "Velocity"),
    0x8F: ("Chan 16 Note off", "Note", "Velocity"),
    0x90: ("Chan 1 Note on", "Note", "Velocity"),
    0x91: ("Chan 2 Note on", "Note", "Velocity"),
    0x92: ("Chan 3 Note on", "Note", "Velocity"),
    0x93: ("Chan 4 Note on", "Note", "Velocity"),
    0x94: ("Chan 5 Note on", "Note", "Velocity"),
    0x95: ("Chan 6 Note on", "Note", "Velocity"),
    0x96: ("Chan 7 Note on", "Note", "Velocity"),
    0x97: ("Chan 8 Note on", "Note", "Velocity"),
    0x98: ("Chan 9 Note on", "Note", "Velocity"),
    0x99: ("Chan 10 Note on", "Note", "Velocity"),
    0x9A: ("Chan 11 Note on", "Note", "Velocity"),
    0x9B: ("Chan 12 Note on", "Note", "Velocity"),
    0x9C: ("Chan 13 Note on", "Note", "Velocity"),
    0x9D: ("Chan 14 Note on", "Note", "Velocity"),
    0x9E: ("Chan 15 Note on", "Note", "Velocity"),
    0x9F: ("Chan 16 Note on", "Note", "Velocity"),
    0xA0: ("Chan 1 Polyphonic aftertouch", "Note", "Pressure"),
    0xA1: ("Chan 2 Polyphonic aftertouch", "Note", "Pressure"),
    0xA2: ("Chan 3 Polyphonic aftertouch", "Note", "Pressure"),
    0xA3: ("Chan 4 Polyphonic aftertouch", "Note", "Pressure"),
    0xA4: ("Chan 5 Polyphonic aftertouch", "Note", "Pressure"),
    0xA5: ("Chan 6 Polyphonic aftertouch", "Note", "Pressure"),
    0xA6: ("Chan 7 Polyphonic aftertouch", "Note", "Pressure"),
    0xA7: ("Chan 8 Polyphonic aftertouch", "Note", "Pressure"),
    0xA8: ("Chan 9 Polyphonic aftertouch", "Note", "Pressure"),
    0xA9: ("Chan 10 Polyphonic aftertouch", "Note", "Pressure"),
    0xAA: ("Chan 11 Polyphonic aftertouch", "Note", "Pressure"),
    0xAB: ("Chan 12 Polyphonic aftertouch", "Note", "Pressure"),
    0xAC: ("Chan 13 Polyphonic aftertouch", "Note", "Pressure"),
    0xAD: ("Chan 14 Polyphonic aftertouch", "Note", "Pressure"),
    0xAE: ("Chan 15 Polyphonic aftertouch", "Note", "Pressure"),
    0xAF: ("Chan 16 Polyphonic aftertouch", "Note", "Pressure"),
    0xB0: ("Chan 1 Control mode change", "", ""),
    0xB1: ("Chan 2 Control mode change", "", ""),
    0xB2: ("Chan 3 Control mode change", "", ""),
    0xB3: ("Chan 4 Control mode change", "", ""),
    0xB4: ("Chan 5 Control mode change", "", ""),
    0xB5: ("Chan 6 Control mode change", "", ""),
    0xB6: ("Chan 7 Control mode change", "", ""),
    0xB7: ("Chan 8 Control mode change", "", ""),
    0xB8: ("Chan 9 Control mode change", "", ""),
    0xB9: ("Chan 10 Control mode change", "", ""),
    0xBA: ("Chan 11 Control mode change", "", ""),
    0xBB: ("Chan 12 Control mode change", "", ""),
    0xBC: ("Chan 13 Control mode change", "", ""),
    0xBD: ("Chan 14 Control mode change", "", ""),
    0xBE: ("Chan 15 Control mode change", "", ""),
    0xBF: ("Chan 16 Control mode change", "", ""),
    0xC0: ("Chan 1 Program change", "Program #", ""),
    0xC1: ("Chan 2 Program change", "Program #", ""),
    0xC2: ("Chan 3 Program change", "Program #", ""),
    0xC3: ("Chan 4 Program change", "Program #", ""),
    0xC4: ("Chan 5 Program change", "Program #", ""),
    0xC5: ("Chan 6 Program change", "Program #", ""),
    0xC6: ("Chan 7 Program change", "Program #", ""),
    0xC7: ("Chan 8 Program change", "Program #", ""),
    0xC8: ("Chan 9 Program change", "Program #", ""),
    0xC9: ("Chan 10 Program change", "Program #", ""),
    0xCA: ("Chan 11 Program change", "Program #", ""),
    0xCB: ("Chan 12 Program change", "Program #", ""),
    0xCC: ("Chan 13 Program change", "Program #", ""),
    0xCD: ("Chan 14 Program change", "Program #", ""),
    0xCE: ("Chan 15 Program change", "Program #", ""),
    0xCF: ("Chan 16 Program change", "Program #", ""),
    0xD0: ("Chan 1 Channel aftertouch", "Pressure", ""),
    0xD1: ("Chan 2 Channel aftertouch", "Pressure", ""),
    0xD2: ("Chan 3 Channel aftertouch", "Pressure", ""),
    0xD3: ("Chan 4 Channel aftertouch", "Pressure", ""),
    0xD4: ("Chan 5 Channel aftertouch", "Pressure", ""),
    0xD5: ("Chan 6 Channel aftertouch", "Pressure", ""),
    0xD6: ("Chan 7 Channel aftertouch", "Pressure", ""),
    0xD7: ("Chan 8 Channel aftertouch", "Pressure", ""),
    0xD8: ("Chan 9 Channel aftertouch", "Pressure", ""),
    0xD9: ("Chan 10 Channel aftertouch", "Pressure", ""),
    0xDA: ("Chan 11 Channel aftertouch", "Pressure", ""),
    0xDB: ("Chan 12 Channel aftertouch", "Pressure", ""),
    0xDC: ("Chan 13 Channel aftertouch", "Pressure", ""),
    0xDD: ("Chan 14 Channel aftertouch", "Pressure", ""),
    0xDE: ("Chan 15 Channel aftertouch", "Pressure", ""),
    0xDF: ("Chan 16 Channel aftertouch", "Pressure", ""),
    0xE0: ("Chan 1 Pitch wheel range", "LSB", "MSB"),
    0xE1: ("Chan 2 Pitch wheel range", "LSB", "MSB"),
    0xE2: ("Chan 3 Pitch wheel range", "LSB", "MSB"),
    0xE3: ("Chan 4 Pitch wheel range", "LSB", "MSB"),
    0xE4: ("Chan 5 Pitch wheel range", "LSB", "MSB"),
    0xE5: ("Chan 6 Pitch wheel range", "LSB", "MSB"),
    0xE6: ("Chan 7 Pitch wheel range", "LSB", "MSB"),
    0xE7: ("Chan 8 Pitch wheel range", "LSB", "MSB"),
    0xE8: ("Chan 9 Pitch wheel range", "LSB", "MSB"),
    0xE9: ("Chan 10 Pitch wheel range", "LSB", "MSB"),
    0xEA: ("Chan 11 Pitch wheel range", "LSB", "MSB"),
    0xEB: ("Chan 12 Pitch wheel range", "LSB", "MSB"),
    0xEC: ("Chan 13 Pitch wheel range", "LSB", "MSB"),
    0xED: ("Chan 14 Pitch wheel range", "LSB", "MSB"),
    0xEE: ("Chan 15 Pitch wheel range", "LSB", "MSB"),
    0xEF: ("Chan 16 Pitch wheel range", "LSB", "MSB"),
    0xF0: ("System Exclusive", "", ""),
    0xF1: ("System Common  undefined", "", ""),
    0xF2: ("Sys Com Song Position Pntr", "LSB", "MSB"),
    0xF3: ("Sys Com Song Select(Song #)", "(0127)", ""),
    0xF4: ("System Common  undefined", "", ""),
    0xF5: ("System Common  undefined", "", ""),
    0xF6: ("Sys Com tune request", "", ""),
    0xF7: ("Sys Comend of SysEx (EOX)", "", ""),
    0xF8: ("Sys real time timing clock", "", ""),
    0xF9: ("Sys real time undefined", "", ""),
    0xFA: ("Sys real time start", "", ""),
    0xFB: ("Sys real time continue", "", ""),
    0xFC: ("Sys real time stop", "", ""),
    0xFD: ("Sys real time undefined", "", ""),
    0xFE: ("Sys real time active sensing", "", ""),
    0xFF: ("Sys real time sys reset", "", ""),
}

MIDI_BYTE_LOOKUP = defaultdict(str)
MIDI_BYTE_LOOKUP.update({x: y[0] for x, y in DATA.items()})
MIDI_NIBBLE_LOOKUP = defaultdict(lambda: ('', ''))
MIDI_NIBBLE_LOOKUP.update({x: (y[1], y[2]) for x, y in DATA.items()})
