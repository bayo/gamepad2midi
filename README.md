# gamepad2midi

Python application to convert gamepad input to MIDI

## Installation

### Ubuntu / Debian / Raspbian

1. Install dependencies:
    ``` bash
    sudo apt-get install librtmidi-dev
    sudo pip install python-rtmidi
    ```

2. Plug the gamepad and find the name
    ``` bash
    lsusb
    ```

3. Configure `mygamepad2midi.py` with the gamepad name.

4. Run
    ``` bash
    ./mygamepad2midi.py
    ```
