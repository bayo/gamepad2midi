gamepad2midi
============

Python application to convert gamepad input to MIDI events.

It displays a graphic user interface for gamepad feedback.
It tries to use `PyQt` 4 or 5, then use `pygame` if none of them are installed.

The gamepad events are catched using `pygame`.

The MIDI events are send using `rtmidi` library.

The binding description is done in Python source code,
you can find an example in the file `mygamepad2midi.py`.

Installation
------------

### Ubuntu / Debian / Raspbian

You have to install `pygame`, PyQt if you like and `rtmidi`.
```bash
sudo apt-get install python-pygame python-pyqt python-rtmidi
```

If `rtmidi` for Python is not packaged for your distribution,
you can install it like that.

```bash
sudo apt-get install librtmidi-dev
sudo pip install python-rtmidi
```

Configuration
-------------

You have first to find the name of your gamepad.
For that, plug your gamepad and use `lsusb`, or execute
`./mygamepad2midi.py` (gamepad names will be displayed).

Then you have to configure the binding provided on `mygamepad2midi.py`.
You can create your own file based on it.

```bash
cp mygamepad2midi.py test.py
# configure test.py
./test.py
```

You can use the application in place by executing `mygamepad2midi.py`
or your own file placed in the same directory.
Or you can use it as a library, and execute your own script
based on `mygamepad2midi.py` anywhere you want.

```bash
cd gamepad2midi.py
pip install --user .
```

Todo
----

- headless option
- command line argument
- file format for the binding
- use library supporting plug in/out of gamepad