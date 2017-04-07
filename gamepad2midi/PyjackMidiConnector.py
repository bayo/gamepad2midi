#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""MIDI connector using pyjack library

Hmmmm... it looks like Pyjack do not support MIDI.

"""

from .MidiConnector import MidiConnector

class PyjackMidiConnector(MidiConnector):

    def __init__(self):
        raise Exception("Not implemented")

    def close(self):
        raise Exception("Not implemented")

    def note_on(self, channel, note):
        raise Exception("Not implemented")

    def note_off(self, channel, note):
        raise Exception("Not implemented")
