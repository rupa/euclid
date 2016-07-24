import abc
import logging
import time

import rtmidi
from rtmidi.midiutil import open_midiport

from euclid import euclidean_rhythm


log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)


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

    def __init__(
        self, k, n, port_in=None, port_out=None, step_len=0.25, gate_len=0.1
    ):
        self.k = k
        self.n = n

        self.port_in = port_in
        self.port_out = port_out

        self.STEP_LEN = step_len
        self.GATE_LEN = step_len if gate_len > step_len else gate_len

        # msgchannel, note, velocity
        self.k_ON = (0x90, 60, 127)
        self.k_OFF = (0x80, 60, 0)
        self.n_ON = (0x90, 62, 127)
        self.n_OFF = (0x80, 62, 0)

        # mshchannel, note, threshold
        self.control_ON = (0x90, 61, 0)
        self.rotate_ON = (0x90, 63, 0)

        self.pattern = (self.k, self.n)
        self.setup_midi()

    def setup_midi(self):
        log.info('setting up midi')
        self.midiin, self.port_in_name = open_midiport(
            self.port_in, 'input', port_name='euclid input port'
        )
        log.info('set midi in port: {0}'.format(self.port_in_name))
        self.midiout, self.port_out_name = open_midiport(
            self.port_in, 'output', port_name='euclid output_port'
        )
        log.info('set midi out port: {0}'.format(self.port_out_name))
        self.midiin.set_callback(self.on_midi_in)
        log.info('set midi in callback')
        self._wallclock = time.time()

    def teardown_midi(self):
        """
        cleanup objects
        """
        log.info('tearing down midi')
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

        def compare(m1, m2):
            if (m1[0], m1[1]) == (m2[0], m2[1]) and m1[2] > m2[2]:
                return True
            return False

        message, deltatime = event
        self._wallclock += deltatime
        if compare(message, self.control_ON):
            log.info('stepping')
            self.step()
        elif compare(message, self.rotate_ON):
            log.info('rotating')
            self.rotate()
        else:
            log.info('{0}@{1:0.6f} 0x{2[0]:02X} {2} {3}'.format(
                self.port_in_name, self._wallclock, message, data
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
        log.info('playing E({0}, {1})'.format(self.k, self.n))
        try:
            while True:
                self.step()
                time.sleep(self.STEP_LEN - self.GATE_LEN)
        except KeyboardInterrupt:
            self.stop()
            log.info('stopping')

    def __delete__(self):
        self.teardown_midi()
