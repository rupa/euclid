Euclidean Rhythm Sequencer stuff

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
>>> e = EuclideanSequencer(5, 8, 0, 0, 0, 0)
```

then press MIDI note 61 to step, or MIDI note 63 to rotate.

# Notes

For now, hardcoded to do the following:

* uses port 0 for in and out
* emits MIDI 60 (middle C) on each step
* emits MIDI 62 (middle D) on each fill
* listens for MIDI 61 (middle C#) to step
* listens for MIDI 63 (middle D#) to rotate
