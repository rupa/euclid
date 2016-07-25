# LED Control, notes wrap around, and disregard octave change
LED_USB_PORT = 1
LED_LOW_NOTE = 48
LED_HIGH_NOTE = 72

# computer-midi_device - use port 2
# computer-cv_device - use port 3
# CV Layer does not convert MIDI Messages from Controller Layer.
# CV in is converted to Port 3, MIDI Channel 2
# CV out is from MIDI channel 2 (either port?)
MIDI_USB_PORT = 2
CV_USB_PORT = 3

# CV ports are unipolar 0-5V
CV_VOLTS_LOW = 0
CV_VOLTS_HIGH = 5

# TRRS IN
EXPR_IN = None  # expression pedal voltage
CV_IN_1 = 112   # CC#112
CV_IN_2 = 113   # CC#113

# TRS OUT 1
GATE_OUT = None # gate (NOTE_ON, NOTE_OFF)
CV_OUT_1 = None # note

# TRS OUT 2
CV_OUT_2 = 001  # CC#1 (modulation) (if used)
CV_OUT_3 = None # pitch bend (if used)

# keyboard note/gate/etc sent out on MIDI channel 1
MIDI_OUT_CHANNEL = 1

# presets A, B, and C listen to MIDI channel 2
# controller layer is off

# Preset D overrides

# keyboard note/gate/etc sent out on MIDI channel 10
#MIDI_OUT_CHANNEL = 10
# controller layer listens to MIDI channel 9

# Voltage conversions

def uni2bi(v):
    """
    convert 0-5V (qunexus) to -5-5V (modular)
    >>> uni2bi(-0.01)
    Traceback (most recent call last):
    ValueError: clip!
    >>> uni2bi(0), uni2bi(2.5), uni2bi(5)
    (-5.0, 0.0, 5.0)
    >>> uni2bi(5.01)
    Traceback (most recent call last):
    ValueError: clip!
    """
    if 0 <= v <= 5:
        return (v * 2.0) - 5
    raise ValueError('clip!')


def bi2uni(v):
    """
    modular to qunexus
    >>> bi2uni(-5.01)
    Traceback (most recent call last):
    ValueError: clip!
    >>> bi2uni(-5), bi2uni(0), bi2uni(5)
    (0.0, 2.5, 5.0)
    >>> bi2uni(5.01)
    Traceback (most recent call last):
    ValueError: clip!
    """
    if -5 <= v <= 5:
        return (v + 5) / 2.0
    raise ValueError('clip!')
