# Synopsis

MIDI Euclidean Rhythm Sequencer stuff

Somewhat QuNexus oriented.

Sequences can be stepped, rotated, and reset.

# Requirements

* ~$ pip install -r requirements.txt

# Usage

```
~$ python
>>> from euclid import demo
>>> demo()
setting up midi
Do you want to create a virtual MIDI input port? (y/N) n
Available MIDI input ports:

[0] QuNexus Port 1
[1] QuNexus Port 2
[2] QuNexus Port 3

Select MIDI input port (Control-C to exit): 0
Opening MIDI input port #0 (euclid input port).
set midi in port: euclid input port
Do you want to create a virtual MIDI ouput port? (y/N) n
Available MIDI ouput ports:

[0] QuNexus Port 1
[1] QuNexus Port 2
[2] QuNexus Port 3

Select MIDI ouput port (Control-C to exit): 0
Opening MIDI ouput port #0 (euclid output_port).
set midi out port: euclid output_port
set midi in callback
playing E(5, 8)
^Cstopping
>>>
```

or

```
~$ python
>>> from euclid import EuclideanSequencer
>>> e = EuclideanSequencer((13, 17), 0, 0, 0, 0)
```

then press MIDI note 60 (middle C) to step, 62 (D) to rotate, 64 (E) to reset.
k is emitted on MIDI note 61 (C#), n on note 63 (D#).

# Tests

./tests.sh
