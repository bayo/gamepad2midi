#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""MIDI connector using rtmidi library"""

import rtmidi
from .MidiConnector import *


class RtmidiMidiConnector(MidiConnector):

	def __init__(self, rtapi):
		out = rtmidi.MidiOut(rtapi, "gamepad2midi")

		ports = self.select_midiport(out)
		if ports is None:
			raise Exception("No port was found")
		else:
			port, portname = ports

		if port is not None:
			print "Opening MIDI output port %i (%s)." % (port, portname)
			out.open_port(port, portname)
		else:
			print "Opening virtual MIDI input port (%s)." % midioutportname
			out.open_virtual_port(portname)
		
		self.out = out

	def select_midiport(self, midi, default=0):
		ports = midi.get_ports()
		if not ports:
			print("No MIDI ports found.")
			return None
		else:
			port = 0
			return port, ports[port]

	def close(self):
		self.out.close_port()

	def note_on(self, channel, note):
		if channel < 0x00 or channel > 0x0F:
			raise Exception("channel must be 0..15 but %i found" % channel)
		self.out.send_message([0x90 + channel, note, 112])

	def note_off(self, channel, note):
		if channel < 0x00 or channel > 0x0F:
			raise Exception("channel must be 0..15 but %i found" % channel)
		self.out.send_message([0x80 + channel, note, 0])

