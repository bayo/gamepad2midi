#!/usr/bin/env python

"""
Gamepad2Midi translate gamepad input to MIDI messages.
The main use case is to use gamepad to control music softwares using JACK, not to direct play music.

It use pygame (SDL) to catch input controls and python-rtmidi to send MIDI messages.

TODO use configuration file for bindings
TODO use command line options to config MIDI connectors and binding configuration
TODO create a light-weight user interface
TODO use a light-weight API to get input
TODO use an input library witch allow plug and remove of device
"""

import sys

import pygame

class InputMapping:

    def __init__(self):
        self.bindings = {}
        self.joystick_ids = {}
        pass

    def get_button_note(self, joy_id, button):
        joy_name = self.joystick_ids[joy_id]
        key = ("buttons", joy_name)
        if not (key in self.bindings):
            return None, None
        channel = self.bindings[key]
        return channel, button

    def get_axis_note(self, joy_id, axis_id, value):
        joy_name = self.joystick_ids[joy_id]
        key = ("axis_range", joy_name, axis_id)
        if not (key in self.bindings):
            return None, None
        (channel, lower_note, upper_note) = self.bindings[key]

        # translate and clamp axis value
        value = ((value + 1)) / 2
        if value < 0: value = 0
        elif value > 1: value = 1

        note = int(round(lower_note + (upper_note - lower_note) * value))
        return channel, note

    def register_current_joystick(self, joy_name, jid):
        self.joystick_ids[jid] = joy_name

    def bind_all_buttons(self, joy_name, channel):
        """
        Bind all buttons of a joystick into a channel. It use the joystick name.
        """
        self.bindings[("buttons", joy_name)] = channel

    def bind_axis_range(self, joy_name, axis_id, channel, lower_note, upper_note):
        """
        Bind an axis of a joystick into a channel and a range of note. It use the joystick name.
        """
        self.bindings[("axis_range", joy_name, axis_id)] = (channel, lower_note, upper_note)


def midi_connector_factory(api):

    try:
        import rtmidi

        apis = {
            "CoreMIDI": rtmidi.API_MACOSX_CORE,
            "ALSA": rtmidi.API_LINUX_ALSA,
            "JACK": rtmidi.API_UNIX_JACK,
            "WS_MM": rtmidi.API_WINDOWS_MM,
        }
        if api in apis:
            rtmidi_api = apis[api]
            from RtmidiMidiConnector import RtmidiMidiConnector
            return RtmidiMidiConnector(rtmidi_api)
        else:
            print "rtmidi do not support API name \"%s\"" % api

    except ImportError:
        print "WARNING: rtmidi python library is not available"
        pass

    # here we can add another python lib

    print "WARNING: use pygame midi connector. MIDI api is not selectable"
    # TODO on my system (Ubuntu 12.10) pygame MIDI crash
    from PygameMidiConnector import PygameMidiConnector
    return PygameMidiConnector()


class Gamepad2Midi:

    def __init__(self, api, mapping):
        self.midi_connector = midi_connector_factory(api)
        self.mapping = mapping
        self.old_axis_note = {}

    def send_button(self, joy, button, enabled):
        channel, _note = self.mapping.get_button_note(joy, button)
        if channel == None:
            return

        if enabled:
            print "note on ", channel + 1, button
            self.midi_connector.note_on(channel, button)
        else:
            print "note off", channel + 1, button
            self.midi_connector.note_off(channel, button)

    def send_axis(self, joy, axis_id, value):
        global old_axis_note
        channel, note = self.mapping.get_axis_note(joy, axis_id, value)
        if channel == None:
            return

        key = (joy, axis_id)
        old_note = None
        if key in self.old_axis_note:
            old_note = self.old_axis_note[key]
        if note == old_note:
            return

        if old_note != None:
            print "note off", channel + 1, old_note
            self.midi_connector.note_off(channel, old_note)
        if note != None:
            print "note on ", channel + 1, note
            self.midi_connector.note_on(channel, note)

        self.old_axis_note[(joy, axis_id)] = note

    def init_inputs(self, ui, mapping):
        #let's turn on the joysticks just so we can play with em
        print "Inputs:"
        for jid in range(pygame.joystick.get_count()):
            j = pygame.joystick.Joystick(jid)
            j.init()
            print "[%i] %s" % (j.get_id(), j.get_name())
            mapping.register_current_joystick(j.get_name(), j.get_id())
    
            channel, _note = mapping.get_button_note(j.get_id(), 0)
            if channel == None:
                print "\t- Buttons are not binded"
            else:
                print "\t- Buttons are binded into channel %i" % (channel+1)

            for axis_id in xrange(0, j.get_numaxes()):
                channel, _note = mapping.get_axis_note(j.get_id(), axis_id, 0)
                if channel == None:
                    print "\t- Axis %i is not binded" % (axis_id+1)
                else:
                    print "\t- Axis %i is binded into channel %i" % (axis_id+1, channel+1)

            # init ui
            ui.register_joystick(j.get_id(), j.get_name(), j.get_numbuttons(), j.get_numaxes())
            # looks like reaching state is not working
            for button_id in range(j.get_numbuttons()):
                pressed = j.get_button(button_id)
                if pressed:
                    ui.press_button(jid, button_id)
            for axis_id in range(j.get_numaxes()):
                value = j.get_axis(axis_id)
                ui.set_axis_value(jid, axis_id, value)

        if not pygame.joystick.get_count():
            print "No joystick connected"
            return

    def create_user_interface(self):
        try:
            from .QtUserInterface import QtUserInterface
            return QtUserInterface()
        except ImportError:
            from .SdlUserInterface import SdlUserInterface
            return SdlUserInterface()

    def run(self):
        pygame.init()

        ui = self.create_user_interface()
        ui.init()

        self.init_inputs(ui, self.mapping)

        going = True
        while going:
            has_changed = False
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    going = False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        going = False
                    else:
                        global LastKey
                        LastKey = e.key

                if e.type == pygame.JOYAXISMOTION:
                    joy, axis, value = e.joy, e.axis, e.value
                    ui.set_axis_value(joy, axis, value)
                    self.send_axis(joy, axis, value)
                elif e.type == pygame.JOYBUTTONDOWN:
                    joy, button = e.joy, e.button
                    ui.press_button(joy, button)
                    self.send_button(joy, button, True)
                elif e.type == pygame.JOYBUTTONUP:
                    joy, button = e.joy, e.button
                    ui.release_button(joy, button)
                    self.send_button(joy, button, False)

                has_changed = True

            if has_changed:
                ui.process()

            if ui.is_closed():
                going = False

            pygame.time.wait(10)

        ui.close()
        pygame.quit()


available_midi_apis = {
    "CoreMIDI":  "Apple Mac OS X CoreMIDI interface",
    "ALSA":     "Linux ALSA interface",
    "JACK":     "UNIX JACK interface",
    "WS_MM":    "Microsoft Windows Multimedia interface",
    "WS_KS":    "Microsoft Windows Kernel Streaming interface (witch is right now (rtmidi 0.3a) unsupported by rtmidi)",
}

def run(api, mapping):
    """
    Launch gamepad2midi.
    """
    job = Gamepad2Midi(api, mapping)
    job.run()

def main(mapping=None):
    """
    Launch gamepad2midi with command line options and an empty binding.
    Call the function ``gamepad2midi(api, mapping)`` to custom it.
    """
    # TODO read a config file or generate an auto config instead of an empty one
    if mapping is None:
        mapping = InputMapping()
        print "WARNING: Gamepad mapping is empty. Create your own mapping using the template mygamepad2midi.py "

    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option("-O", "--output", dest="api", help="MIDI output interface",
        choices=available_midi_apis.keys(), type="choice")

    # TODO rework "print" with logger
    # parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False,
    #    help="Print more information to stdout")

    # it is quite a hack to display choices options, but it works
    g = parser.add_option_group("Available output interfaces")
    keys = available_midi_apis.keys()
    keys.sort()
    for api in keys:
        comment = available_midi_apis[api]
        g.add_option("--" + api, help=comment, dest="api", action="store_const", const=api)

    options, _args = parser.parse_args()

    if options.api == None:
        parser.print_help()
        return

    run(options.api, mapping)
