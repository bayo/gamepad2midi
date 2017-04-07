#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""MIDI connector using pygame library"""

import pygame
from .MidiConnector import MidiConnector


"""

I can't use that right now...

  File "./gamepad2midi.py", line 20, in <module>
    midiConnector = pygameMidiConnector()
  File "/home/valentin/workspace/Music/gamepad2midi/pygameMidiConnector.py", line 10, in __init__
    pygame.midi.init()
  File "/usr/lib/python2.7/dist-packages/pygame/midi.py", line 71, in init
    import pygame.pypm
ImportError: /usr/lib/libportmidi.so.0: undefined symbol: snd_seq_event_input_pending

"""

class PygameMidiConnector(MidiConnector):

    def __init__(self):
        pygame.init()
        pygame.midi.init()
        self.port = pygame.midi.get_default_output_id()
        self.midi_out = pygame.midi.Output(self.port, 0)

    def close(self):
        pygame.midi.quit()

    def note_on(self, channel, note):
        self.midi_out.note_on(note, channel=channel)
        print channel, note, "on"

    def note_off(self, channel, note):
        self.midi_out.note_off(note, channel=channel)
        print channel, note, "off"
