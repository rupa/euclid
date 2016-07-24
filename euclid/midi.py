import abc
import time

import rtmidi
from rtmidi.midiutil import open_midiport

from euclid import euclidean_rhythm


IN_PORT, OUT_PORT = 0, 0


class MIDIClockedSequence(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def on_midi_in(self, event, data=None):
        """
        should be set as callback, and should call step
        """
        raise NotImplementedError

    @abc.abstractmethod
    def step(self):
        raise NotImplementedError


class EuclideanSequence(MIDIClockedSequence):
    """
    MIDI and Euclid
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

        self.pattern = (self.k, self.n)
        self.setup_midi()

    def setup_midi(self):
        print 'setting up midi'
        self.midiin, self.port_in_name = open_midiport(
            IN_PORT, 'input', port_name='euclid input port'
        )
        print 'set midi in port:', self.port_in_name
        self.midiout, self.port_out_name = open_midiport(
            OUT_PORT, 'output', port_name='euclid output_port'
        )
        print 'set midi out port:', self.port_out_name
        self.midiin.set_callback(self.on_midi_in)
        print 'set midi in callback'
        self._wallclock = time.time()

    def teardown_midi(self):
        """
        cleanup objects
        """
        print 'tearing down midi'
        self.midiin.close_port()
        self.midout.close_port()
        del self.midiin
        del self.midiout

    @property
    def pattern(self):
        if not hasattr(self, '_pattern'):
            self._pattern = euclidean_rhythm(self.k, self.n)
        return self._pattern

    @pattern.setter
    def pattern(self, val):
        self._pattern = euclidean_rhythm(val[0], val[1])

    def on_midi_in(self, event, data=None):
        """
        handle MIDI events
        """
        message, deltatime = event
        message[0] = hex(message[0])
        self._wallclock += deltatime
        print('{0}@{1:0.6f} {2}'.format(
            self.port_in_name, self._wallclock, message
        ))

    def rotate(self):
        return self.pattern.next()

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
        """
        make sure everything is turned off
        """
        self.midiout.send_message(self.k_OFF)
        self.midiout.send_message(self.n_OFF)
        time.sleep(self.STEP_LEN)

    def play(self):
        """
        not clocked
        """
        print 'playing E({0}, {1})'.format(self.k, self.n)
        try:
            while True:
                self.step()
                time.sleep(self.STEP_LEN - self.GATE_LEN)
        except KeyboardInterrupt:
            self.stop()
            print 'stopping'

    def __delete__(self):
        self.teardown_midi()
