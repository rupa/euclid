#!/usr/bin/env bash

for x in euclid/*.py; do python -m doctest $x; done
