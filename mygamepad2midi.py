#!/usr/bin/env python

from gamepad2midi import *


def main():
    mapping = InputMapping()

    # Put your gamepad name here and bind your custom mappings
    mapping.bind_all_buttons("Logitech Logitech(R) Precision(TM) Gamepad", 9)
    mapping.bind_axis_range("Logitech Logitech(R) Precision(TM) Gamepad", 0, 10, 30, 40)
    mapping.bind_axis_range("Logitech Logitech(R) Precision(TM) Gamepad", 1, 11, 30, 40)

    # Select the API:
    #	- JACK: Unix
    #	- ALSA: Linux
    #	- CoreMIDI: MacOSX
    #	- WS_MM: Windows MM
    # 	- WS_KS: Windows KS
    gamepad2midi("JACK", mapping)


if __name__ == '__main__':
    main()
