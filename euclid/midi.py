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

    def __init__(self, k, n, step_len=0.25, gate_len=0.1):
        self.k = k
        self.n = n

        # channel 1, middle C/D, velocity 127
        self.k_ON = (0x90, 60, 127)
        self.k_OFF = (0x80, 60, 0)
        self.n_ON = (0x90, 62, 127)
        self.n_OFF = (0x80, 62, 0)

        self.STEP_LEN = step_len
        self.GATE_LEN = step_len if gate_len > step_len else gate_len

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

    def step(self):
        fill = self.rotate()
        self.midiout.send_message(self.n_ON)
        if fill:
            self.midiout.send_message(self.k_ON)
        time.sleep(self.GATE_LEN)
        self.midiout.send_message(self.n_OFF)
        if fill:
            self.midiout.send_message(self.k_OFF)

    def stop(self):
        self.midiout.send_message(self.k_OFF)
        self.midiout.send_message(self.n_OFF)
        time.sleep(self.STEP_LEN)

    def play(self):
        print 'playing E({0}, {1}) ...'.format(self.k, self.n),
        try:
            while True:
                self.step()
                time.sleep(self.STEP_LEN - self.GATE_LEN)
        except KeyboardInterrupt:
            self.stop()
            print 'stopping.'

    def __delete__(self):
        self.midiin.close_port()
        self.midout.close_port()
        del self.midiin
        del self.midiout
