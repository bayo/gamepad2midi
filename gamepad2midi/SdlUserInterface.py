#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""User interface using SDL"""

from pygame import *

class SdlUserInterface:

    def __init__(self):
        self.joysticks = []
        self.status = {}

        self.screen_size = (640, 480)
        display.set_caption("gamepad2midi")
        win = display.set_mode(self.screen_size)
        self.win = win

        self.font = font.Font(None, 26)

        #self.color_off = (120, 120, 120)
        self.color_off = (255, 50, 50)
        self.text_color_off = (255, 255, 255)
        self.color_on = (50, 255, 50)
        self.text_color_on = (255, 255, 255)

    def resize_screen(self, size):
        if self.screen_size == size:
            return

        display.quit()

        self.screen_size = size
        display.init()
        display.set_caption("gamepad2midi")
        self.win = display.set_mode(self.screen_size)

    def register_joystick(self, id, name, buttons, axis):
        while len(self.joysticks) < id + 1:
            self.joysticks.append(None)
        self.joysticks[id] = (id, name, buttons, axis)

    def release_button(self, joy, button):
        key = ("button", joy, button)
        self.status[key] = False

    def press_button(self, joy, button):
        key = ("button", joy, button)
        self.status[key] = True

    def set_axis_value(self, joy, axis, value):
        key = ("axis", joy, axis)
        self.status[key] = value

    def draw_text(self, pos, text, color, bgcolor):
        textimg = self.font.render(text, 1, color, bgcolor)
        self.win.blit(textimg, pos)
        return pos[0] + textimg.get_width() + 5, pos[1]

    def draw_axis(self, pos, axis, value):
        activated = value != 0
        value = int((value + 1) * 5 / 2)
        text = "a" + str(axis + 1)
        for i in xrange(0, 6):
            if i == value:
                text += "|"
            else:
                text += " "

        text_color = self.text_color_off                 
        color = self.color_off
        if activated:
            color = self.color_on
            text_color = self.text_color_on

        textimg = self.font.render(text, 1, text_color, color)
        self.win.blit(textimg, pos)
        return pos[0] + textimg.get_width() + 5, pos[1]

    def draw(self):
        bgcolor = (50, 50, 50)
        black = (0, 0, 0)
        self.win.fill(bgcolor, (0, 0, self.screen_size[0], self.screen_size[1]))
        width = 0
        pos = (2, 5)
        for id, name, buttons, axis in self.joysticks:
            pos = (2, pos[1])
            pos = self.draw_text(pos, name, (155, 155, 155), bgcolor)
            width = pos[0]
            pos = (10, pos[1] + 30)

            for button in xrange(0, buttons):
                key = ("button", id, button)
                pressed = False
                if key in self.status:
                    pressed = self.status[key]
                text_color = self.text_color_off
                color = self.color_off
                if pressed:
                    color = self.color_on
                    text_color = self.text_color_on
                pos = self.draw_text(pos, "b" + str(button + 1), text_color, color)
                if width < pos[0]:
                    width = pos[0]

            for axis_id in xrange(0, axis):
                key = ("axis", id, axis_id)
                value = 0
                if key in self.status:
                    value = self.status[key]
                pos = self.draw_axis(pos, axis_id, value)
                if width < pos[0]:
                    width = pos[0]

            pos = (10, pos[1] + 50)

        if len(self.joysticks) == 0:
            pos = self.draw_text(pos, "No joystick connected", (255, 0, 0), bgcolor)
            if width < pos[0]:
                width = pos[0]
            pos = (10, pos[1] + 30)

        self.resize_screen((width, pos[1]))
        display.flip()
