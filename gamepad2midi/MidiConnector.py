#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""MIDI connector interface"""

class MidiConnector:

    def __init__(self):
        raise Exception("Method is not overrided")

    def close(self):
        raise Exception("Method is not overrided")

    def note_on(self, channel, note):
        raise Exception("Method is not overrided")

    def note_off(self, channel, note):
        raise Exception("Method is not overrided")
