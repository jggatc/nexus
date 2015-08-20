from __future__ import division
import env
engine = env.engine
try:	###
	from interface import MatrixInterface
except ImportError:
	MatrixInterface = None


class Control:
    guide = \
"""Nexus Guide

Protect the integrity of the Nexus by maintaining data flow through the node network.

Controls:
Bot forward (UP/KP8/w)
Bot reverse (DOWN/KP2/s)
Bot left (LEFT/KP4/a)
Bot right (RIGHT/KP6/d)
Bot shoot (SPACE/KP0/z/LMouse)
--directional (CTRL)
Node repair (x)
--directional (SHIFT)
Start/pause (Escape/r)
Sound toggle (o)
Panel toggle (p)

Status indicators:
Nexus integrity (grey)
Bot power (blue)
Data integration (green)
"""

    def __init__(self, matrix):
        self.matrix = matrix
        self.clock = engine.time.Clock()
        self.interface = MatrixInterface('Matrix Interface', matrix, self)
        for i in range(100):   #fix for interface problem
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
                elif event.key == engine.K_o:   ###
                    env.debug = not env.debug
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


class InterfaceObj(engine.sprite.Sprite):   ###

    def __init__(self, identity, matrix, control):
        engine.sprite.Sprite.__init__(self)
        self.matrix = matrix
        self.control = control
        self.width = 42
        self.height = 44
        self.dataprocessed = 0
        self.dataprocessedtop = 0
        self.color1 = engine.Color(20,20,20)
        self.color2 = engine.Color(125,175,200)
        self.image = engine.Surface((self.width,self.height))
        self.image.fill(self.color1)
        self.x, self.y = self.matrix.width-75, self.matrix.height-25
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.font = engine.font.SysFont('arial', 10)
        s = self.font.render('Top', True, self.color2)
        self.image.blit(s, (self.width//2-s.get_width()//2, 0))
        s = self.font.render('Current', True, self.color2)
        self.image.blit(s, (self.width//2-s.get_width()//2, 23))
        self.surf = self.font.render('        ', True, self.color1, self.color1)
        self.surf_pos = (self.width//2-self.surf.get_width()//2)
        self._clock = engine.time.Clock()

    def set_data_processed(self, dataprocessed):
        self.dataprocessed = dataprocessed
        s = self.font.render(str(dataprocessed), True, self.color2)
        self.image.blit(self.surf, (self.surf_pos, 34))
        self.image.blit(s, (self.width//2-s.get_width()//2, 34))

    def set_data_processed_top(self, dataprocessed):
        self.dataprocessedtop = dataprocessed
        s = self.font.render(str(dataprocessed), True, self.color2)
        self.image.blit(self.surf, (self.surf_pos, 11))
        self.image.blit(s, (self.width//2-s.get_width()//2, 11))

    def reset(self):
        self.control.set_panel_display()

    def set_moveable(self, setting=None):
        pass

    def get_control(self, *control):
        class Control:
            def set_active(self, setting=None):
                pass
            def next(self):
                pass
        return Control()

    def update(self):
        pass

if not MatrixInterface:
    MatrixInterface = InterfaceObj

