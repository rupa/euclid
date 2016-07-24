Euclidean Rhythm Sequencer stuff

~$ pip install -r requirements.txt
~$ python
>>> from euclid import demo
>>> demo()

or

>>> from euclid import EuclideanSequencer
>>> e = EuclideanSequencer(5, 8)

then press MIDI note 61 to step, or MIDI note 63 to rotate.

Note: For now, hardcoded to do the following:

* Port 0 for in and out
* emits MIDI 60 (middle C) on each step
* emits MIDI 62 (middle D) on each fill
* MIDI 61 (middle C#) for step
* MIDI 63 (middle D#) for rotate
