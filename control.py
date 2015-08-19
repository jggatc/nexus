from __future__ import division
import env
engine = env.engine
from interface import MatrixInterface


class Control:
    guide = \
"""Nexus Guide

Protect the integrity of the Nexus by maintaining data flow through the node network.

Controls:

Bot forward (UP/KP8/w)
Bot reverse (DOWN/KP2/s)
Bot left (LEFT/KP4/a)
Bot right (RIGHT/KP6/d)
Bot shoot (SPACE/KP0/z)
--directional (CTRL)
Node repair (x)
--directional (SHIFT)
Start/pause (Escape/r)
Panel toggle (p)
"""

    def __init__(self, matrix):
        self.matrix = matrix
        self.clock = engine.time.Clock()
        self.interface = MatrixInterface('Matrix Interface', matrix, self)
        for i in xrange(100):   #fix for interface problem
            self.interface.update()
            if self.interface._clock.get_fps() > 0.0:
                break
        self.interface.set_moveable()
        self.interface.set_moveable('Fixed')
        self.panel = engine.sprite.RenderUpdates(self.interface)
        self.panel_display = True
        self.fps = 60

    def process_event(self):
        for event in engine.event.get():
            if event.type == engine.KEYDOWN:
                if event.key in (engine.K_w, engine.K_UP, engine.K_KP8):
                    self.matrix.avatar.set_control('u', True)
                elif event.key in (engine.K_s, engine.K_DOWN, engine.K_KP2):
                    self.matrix.avatar.set_control('d', True)
                elif event.key in (engine.K_a, engine.K_LEFT, engine.K_KP4):
                    self.matrix.avatar.set_control('l', True)
                elif event.key in (engine.K_d, engine.K_RIGHT, engine.K_KP6):
                    self.matrix.avatar.set_control('r', True)
                elif event.key in (engine.K_z, engine.K_SPACE, engine.K_KP5):
                    self.matrix.avatar.set_control('z', True)
#                elif event.key in (engine.K_SPACE, engine.K_KP5):
#                    self.matrix.avatar.set_control('space', True)
                elif event.key == engine.K_x:
                    self.matrix.avatar.set_control('x', True)
#                    self.matrix.avatar.node_repair()
                elif event.key in (engine.K_ESCAPE, engine.K_r):      ###
#                elif event.key == engine.K_ESCAPE:
                    if not self.matrix.nexus.initiate:
                        self.set_panel_display()
                        self.interface.get_control('Bootup').set_active(False)
                        self.interface.get_control('Activate').set_active(True)
                        self.matrix.nexus.initiation_activate()
                    else:
                        if self.matrix.active:
                            self.interface.get_control('Activate').next()
                            self.matrix.set_active(False)
                        else:
                            self.interface.get_control('Activate').next()
                            self.matrix.set_active(True)
                elif event.key == engine.K_p:
                    self.set_panel_display()
#                elif event.key == engine.K_q:
#                    self.matrix.quit = True
            if event.type == engine.KEYUP:
                if event.key in (engine.K_w, engine.K_UP, engine.K_KP8):
                    self.matrix.avatar.set_control('u', False)
                elif event.key in (engine.K_s, engine.K_DOWN, engine.K_KP2):
                    self.matrix.avatar.set_control('d', False)
                elif event.key in (engine.K_a, engine.K_LEFT, engine.K_KP4):
                    self.matrix.avatar.set_control('l', False)
                elif event.key in (engine.K_d, engine.K_RIGHT, engine.K_KP6):
                    self.matrix.avatar.set_control('r', False)
                elif event.key in (engine.K_z, engine.K_SPACE, engine.K_KP5):
                    self.matrix.avatar.set_control('z', False)
#                elif event.key == engine.K_SPACE or event.key == engine.K_KP5:
#                    self.matrix.avatar.set_control('space', False)
                elif event.key == engine.K_x:
                    self.matrix.avatar.set_control('x', False)
            elif event.type == engine.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.matrix.avatar.set_control('z', True)
#                if event.button == 1:
#                    self.matrix.avatar.set_control('space', True)
            elif event.type == engine.MOUSEBUTTONUP:
                if event.button == 1:
                    self.matrix.avatar.set_control('z', False)
#                if event.button == 1:
#                    self.matrix.avatar.set_control('space', False)
            elif event.type == self.matrix.data_event:
                self.matrix.data_generator()
            elif event.type == self.matrix.surge_event:
                self.matrix.surge_generator()
            elif event.type == self.matrix.spike_event:
                self.matrix.spike_generator()
            elif event.type == self.matrix.bot_event:   ###
                self.matrix.bot_check()
            elif event.type == self.matrix.level_event:   ###
                self.matrix.level_set()
            elif event.type == engine.QUIT:
                self.matrix.quit = True
        self.clock.tick(self.fps)

    def set_panel_display(self):
        self.panel_display = not self.panel_display
        self.interface.set_moveable('Fixed')

    def update(self):
        self.process_event()

