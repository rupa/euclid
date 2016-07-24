Euclidean Rhythm Sequencer stuff

# Requirements

* ~$ pip install -r requirements.txt

# Usage

* ~$ python
* >>> from euclid import demo
* >>> demo()

or

* ~$ python
* >>> from euclid import EuclideanSequencer
* >>> e = EuclideanSequencer(5, 8)

then press MIDI note 61 to step, or MIDI note 63 to rotate.

# Notes

For now, hardcoded to do the following:

* uses port 0 for in and out
* emits MIDI 60 (middle C) on each step
* emits MIDI 62 (middle D) on each fill
* listens for MIDI 61 (middle C#) to step
* listens for MIDI 63 (middle D#) to rotate
