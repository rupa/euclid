import abc
import logging
import time

import rtmidi.midiconstants as mc
from rtmidi.midiutil import open_midiport

from euclid import euclidean_rhythm
from midievents import MIDI_BYTE_LOOKUP as M


log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)


class MIDIClockedSequence(object):
    """
    ABC for stuff
    """
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
    Do up some Euclids
    """

    def __init__(
        self,
        e,
        port_in=None,
        port_out=None,
        channel_in=0,
        channel_out=0,
        gate_len=0.1,
        step_len=0.25,
    ):
        """
        e:           (number of fills, number of steps)
        port_in:     MIDI input port (0 based)
        port_out:    MIDI output port (0 based)
        channel_in:  MIDI input channel (0 based)
        channel_out: MIDI output channel (0 based)
        gate_len:    length of NOTE_ON signals, in seconds
        step_len:    time per step, in seconds. relevant if using play()/stop()
        """
        self.k, self.n = e

        self.port_in = port_in
        self.port_out = port_out

        self.channel_in = 0 if channel_in > 15 else channel_in
        self.channel_out = 0 if channel_out > 15 else channel_out

        self.STEP_LEN = step_len
        self.GATE_LEN = step_len if gate_len > step_len else gate_len

        # note, velocity
        self.k_ON = (mc.NOTE_ON + self.channel_out, 60, 127)
        self.k_OFF = (mc.NOTE_OFF + self.channel_out, 60, 0)
        self.n_ON = (mc.NOTE_ON + self.channel_out, 62, 127)
        self.n_OFF = (mc.NOTE_OFF + self.channel_out, 62, 0)

        # note, threshold
        self.step_ON = (mc.NOTE_ON + self.channel_out, 61, 0)
        self.rotate_ON = (mc.NOTE_ON + self.channel_out, 63, 0)

        self._ppqn = 24
        self._ppqn_count = 0

        self.setup_midi()

        self.pattern = (self.k, self.n)

    def setup_midi(self):
        log.info('setting up midi')
        self.midiin, self.port_in_name = open_midiport(
            self.port_in,
            'input',
            client_name='euclid',
            port_name='euclid input port'
        )
        log.info('set midi in port: {0}'.format(self.port_in_name))
        self.midiin.ignore_types(timing=False)
        log.info('listening for clock on midi in')
        self.midiout, self.port_out_name = open_midiport(
            self.port_out,
            'output',
            client_name='euclid',
            port_name='euclid output_port'
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
            try:
                if (m1[0], m1[1]) == (m2[0], m2[1]) and m1[2] > m2[2]:
                    return True
            except:
                print 'Errr', m1, m2
            return False

        message, deltatime = event

        if message in [[250], [251], [252]]: # start, continue, stop
            return
        if message[0] == 0xF2:               # Com Song Position Pntr
            return
        if 0xB0 <= message[0] <= 0xBF:       # Channel Control Mode change
            return
        if 0xE0 <= message[0] <= 0xEF:       # Channel Pitch Wheel range
            return

        self._wallclock += deltatime

        if message[0] == mc.TIMING_CLOCK:
            if self._ppqn_count % self._ppqn == 0:
                self.step()
                self._ppqn_count = 0
            self._ppqn_count += 1
        elif compare(message, self.step_ON):
            log.info('stepping')
            self.step()
        elif compare(message, self.rotate_ON):
            log.info('rotating')
            self.rotate()
        else:
            log.info('{0}:{1:0.6f} 0x{2[0]:02X}:{3} {2} {4}'.format(
                self.port_in_name,
                self._wallclock,
                message,
                M[message[0]],
                data if data else ''
            ))

    def rotate(self):
        """
        rotate the beat clockwise
        """
        return self.pattern.next()

    def step(self):
        """
        advance a step, and probably do stuff
        """
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
