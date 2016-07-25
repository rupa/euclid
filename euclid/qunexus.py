import time

from midi import EuclideanSequence

import rtmidi.midiconstants as mc

import qunexusconstants as qn


class QuNexusLED(EuclideanSequence):
    """
    Play with the blinking lights
    """
    def __init__(self, e, gate_len=0.1, step_len=0.25):
        """
        e:           (number of fills, number of steps)
        gate_len:    length of NOTE_ON signals, in seconds
        step_len:    time per step, in seconds. relevant if using play()/stop()
        """
        super(QuNexusLED, self).__init__(
            e,
            port_in=None,      # 0:listen to keyboard, virtual:listen to clock
            port_out=0,        # emit to LED control
            channel_in=0,      # listen to keyboard
            channel_out=0,     # emit to keyboard
            gate_len=gate_len,
            step_len=step_len,
        )

        step_note = qn.LED_LOW_NOTE
        k_note = qn.LED_LOW_NOTE + 1
        rotate_note = qn.LED_LOW_NOTE + 2
        n_note = qn.LED_LOW_NOTE + 3
        reset_note = qn.LED_LOW_NOTE + 4

        # note, velocity
        self.k_ON = (mc.NOTE_ON + self.channel_out, k_note, 127)
        self.k_OFF = (mc.NOTE_OFF + self.channel_out, k_note, 0)
        self.n_ON = (mc.NOTE_ON + self.channel_out, n_note, 127)
        self.n_OFF = (mc.NOTE_OFF + self.channel_out, n_note, 0)

        # note, threshold
        self.step_ON = (mc.NOTE_ON + self.channel_out, step_note, 0)
        self.rotate_ON = (mc.NOTE_ON + self.channel_out, rotate_note, 0)
        self.reset_ON = (mc.NOTE_ON + self.channel_out, reset_note, 0)

        self.test()

    def test(self):
        """
        Power On Self Test
        """
        for note in range(qn.LED_LOW_NOTE, qn.LED_HIGH_NOTE + 1):
            self.midiout.send_message(
                (mc.NOTE_ON + self.channel_out, note, 127)
            )
            time.sleep(self.GATE_LEN)
            self.midiout.send_message(
                (mc.NOTE_OFF + self.channel_out, note, 0)
            )
        for brightness in range(0, 16):
            for note in qn.LED_LOW_NOTE, qn.LED_HIGH_NOTE:
                self.midiout.send_message(
                    (mc.NOTE_ON + self.channel_out, note, brightness)
                )
                time.sleep(self.GATE_LEN)
        for brightness in range(15, -1, -1):
            for note in qn.LED_LOW_NOTE, qn.LED_HIGH_NOTE:
                self.midiout.send_message(
                    (mc.NOTE_ON + self.channel_out, note, brightness)
                )
                time.sleep(self.GATE_LEN)
        self.midiout.send_message(
            (mc.NOTE_OFF + self.channel_out, qn.LED_LOW_NOTE, 0)
        )
        self.midiout.send_message(
            (mc.NOTE_OFF + self.channel_out, qn.LED_HIGH_NOTE, 0)
        )
