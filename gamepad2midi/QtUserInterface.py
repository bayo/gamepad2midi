#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""User interface using SDL"""

try:
    from PyQt4 import Qt
except ImportError:
    from PyQt5 import Qt


class JoystickPanel(Qt.QWidget):

    def __init__(self, parent, jid, name, buttonCount, axisCount):
        Qt.QWidget.__init__(self, parent)
        label = Qt.QLabel(self)
        label.setText(name)
        layout = Qt.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        content = Qt.QWidget(self)
        content.setLayout(layout)

        mainLayout = Qt.QVBoxLayout(self)
        mainLayout.setSpacing(0)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(label)
        mainLayout.addWidget(content)

        self.buttons = {}
        self.axis = {}
        for buttonId in range(buttonCount):
            widget = self.createButton(content, buttonId)
            self.buttons[buttonId] = widget
            layout.addWidget(widget)

        for axisId in range(axisCount):
            widget = self.createAxis(content, axisId)
            self.axis[axisId] = widget
            layout.addWidget(widget)

        layout.addStretch()

    def createButton(self, parent, buttonId):
        widget = Qt.QToolButton(parent)
        widget.setText(str(buttonId))
        widget.setEnabled(False)
        widget.setCheckable(True)
        return widget

    def createAxis(self, parent, axisId):
        widget = Qt.QSlider(parent)
        widget.setOrientation(Qt.Qt.Horizontal)
        widget.setRange(-0x7FFF, 0x7FFF)
        widget.setToolTip("Axis %i" % axisId)
        widget.setEnabled(False)
        s = widget.sizeHint()
        s = Qt.QSize(s.height(), s.height())
        widget.setMinimumSize(s)
        widget.setMaximumSize(s)
        return widget

    def setButtonPressed(self, button, isPressed):
        widget = self.buttons.get(button, None)
        if widget is None:
            raise Exception("Button id %d not found" % button)
        widget.setChecked(isPressed)

    def setAxisValue(self, axis, value):
        widget = self.axis.get(axis, None)
        if widget is None:
            raise Exception("Axis id %d not found" % axis)
        widget.setValue(value * 0x7FFF)


class Game2MidiWindow(Qt.QMainWindow):

    def __init__(self, parent=None):
        Qt.QMainWindow.__init__(self, parent)
        self._isClosed = False
        self.setWindowTitle("gamepad2midi")
        self.panel = Qt.QWidget(self)
        self.panel.setLayout(Qt.QVBoxLayout())
        self.setCentralWidget(self.panel)

    def addJoystick(self, widget):
        self.panel.layout().addWidget(widget)

    def closeEvent(self, event):
        self._isClosed = True
        Qt.QMainWindow.closeEvent(self, event)

    def isClosed(self):
        return self._isClosed


class QtUserInterface:

    def __init__(self):
        self.joysticks = {}
        self.status = {}

    def init(self):
        self.app = Qt.QApplication([])
        self.window = Game2MidiWindow()
        self.window.setVisible(True)

    def close(self):
        self.window.setVisible(False)
        self.app = None

    def resize_screen(self, size):
        if self.screen_size == size:
            return
        self.window.resize(size[0], size[1])

    def register_joystick(self, jid, name, buttons, axis):
        widget = JoystickPanel(self.window, jid, name, buttons, axis)
        self.window.addJoystick(widget)
        self.joysticks[jid] = widget

    def release_button(self, joy, button):
        widget = self.joysticks.get(joy, None)
        if widget is None:
            raise Exception("Joystick widget %d not found" % joy)
        widget.setButtonPressed(button, False)

    def press_button(self, joy, button):
        widget = self.joysticks.get(joy, None)
        if widget is None:
            raise Exception("Joystick widget %d not found" % joy)
        widget.setButtonPressed(button, True)

    def set_axis_value(self, joy, axis, value):
        widget = self.joysticks.get(joy, None)
        if widget is None:
            raise Exception("Joystick widget %d not found" % joy)
        widget.setAxisValue(axis, value)

    def is_closed(self):
        return self.window.isClosed()

    def process(self):
        self.app.processEvents(Qt.QEventLoop.AllEvents, 5)
