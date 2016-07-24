import time
import rtmidi

from euclid import euclidean_rhythm


class EuclideanSequence(object):
    """
    todo:
        gets ports right
        clock this shit
        rotation
        set note(s)
    """

    def __init__(self, k, n, step_len, gate_len):
        self.k = k
        self.n = n

        self.step_len = step_len
        self.gate_len = gate_len

        assert self.gate_len <= self.step_len

        # channel 1, middle C/D, velocity 127
        self.k_note = ((0x90, 60, 127), (0x80, 60, 0))
        self.n_note = ((0x90, 62, 127), (0x80, 62, 0))

        self.e = euclidean_rhythm(self.k, self.n)

        self.midiin = rtmidi.MidiIn()
        self.midiout = rtmidi.MidiOut()

        available_in_ports = self.midiin.get_ports()
        available_out_ports = self.midiout.get_ports()
        # the same list on QuNexus
        print 'Ins, Outs:', available_in_ports, available_out_ports
        if available_out_ports:
            self.midiout.open_port(0)
        else:
            # ???
            self.midiout.open_virtual_port("My virtual output")

    def rotate(self):
        return self.e.next()

    def step(self, fill):
        if fill:
            self.midiout.send_message(self.k_note[0])
        self.midiout.send_message(self.n_note[0])
        time.sleep(self.gate_len)
        if fill:
            self.midiout.send_message(self.k_note[1])
        self.midiout.send_message(self.n_note[1])

    def stop(self):
        self.midiout.send_message(self.k_note[1])
        self.midiout.send_message(self.n_note[1])
        time.sleep(self.step_len)

    def play(self):
        print 'playing E({0}, {1}) ...'.format(self.k, self.n),
        try:
            while True:
                self.step(self.rotate())
                time.sleep(self.step_len - self.gate_len)
        except KeyboardInterrupt:
            self.stop()
            print 'stopping.'

    def __delete__(self):
        del self.midiin
        del self.midiout
