#!/usr/bin/env python

import gamepad2midi


def main():
    mapping = gamepad2midi.InputMapping()

    # Put your gamepad name here and bind your custom mappings
    name = "Logitech Logitech(R) Precision(TM) Gamepad"
    mapping.bind_all_buttons(name, 9)
    mapping.bind_axis_range(name, 0, 10, 30, 40)
    mapping.bind_axis_range(name, 1, 11, 30, 40)

    # Select the API:
    # - JACK: Unix
    # - ALSA: Linux
    # - CoreMIDI: MacOSX
    # - WS_MM: Windows MM
    gamepad2midi.run("ALSA", mapping)

if __name__ == '__main__':
    main()
