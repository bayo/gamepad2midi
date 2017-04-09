#!/usr/bin/env python

import gamepad2midi


def main():
    mapping = gamepad2midi.InputMapping()

    # Put your gamepad name here and bind your custom mappings
    name = "Logitech Logitech(R) Precision(TM) Gamepad"

    # This command connects each buttons of the gamepad
    # to a note of the MIDI channel 10
    mapping.bind_all_buttons(name, channel=9)

    # This command connects the axis numero 0 of the gamepad
    # to a range of notes of the MIDI channel 11
    mapping.bind_axis_range(name, 0, channel=10, lower_note=30, upper_note=40)

    # You can add another gamepads if you like
    name = "Afterglow Wired Controller for Xbox One"
    mapping.bind_all_buttons(name, channel=11)

    # The software can be connected to different MIDI API
    # YOu can select one of:
    # - JACK: Unix
    # - ALSA: Linux
    # - CoreMIDI: Mac OS X
    # - WS_MM: Windows MM
    gamepad2midi.run("ALSA", mapping)

if __name__ == '__main__':
    main()
