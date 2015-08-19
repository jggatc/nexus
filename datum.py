from __future__ import division
import env
engine = env.engine
from util import load_sound


class Datum(engine.sprite.Sprite):
    images = None
    masks = None
#    mask = None
    radius = None
    sound = None

    def __init__(self, matrix, x, y, dtype):
        engine.sprite.Sprite.__init__(self)
        self.matrix = matrix
        self.x = float(x)
        self.y = float(y)
        self.dtype = dtype
        if not self.images:
            self.images = {}
            image = engine.Surface((11,11), engine.SRCALPHA)
            color1 = (0,200,0)
            color2 = (0,150,0)
            color3 = (200,0,0)
#            color1 = (0,255,0)
#            color2 = (0,200,0)
#            color3 = (255,0,0)
            points = [(5,0),(10,2),(10,8),(5,10),(0,8),(0,2)]
            engine.draw.polygon(image, color1, points, 0)
            engine.draw.polygon(image, color1, points, 1)
            self.images['hibit'] = image
            image = engine.Surface((11,11), engine.SRCALPHA)
            points = [(5,1),(9,3),(9,7),(5,9),(0,7),(0,3)]
            engine.draw.polygon(image, color2, points, 0)
            engine.draw.polygon(image, color2, points, 1)
            self.images['lobit'] = image
            image = engine.Surface((11,11), engine.SRCALPHA)
            points = [(5,1),(9,3),(9,7),(5,9),(0,7),(0,3)]
            engine.draw.polygon(image, color3, points, 0)
            engine.draw.polygon(image, color3, points, 1)
            self.images['lobit_corrupt'] = image
            self.masks = {}     ###
            self.masks['hibit'] = engine.mask.from_surface(self.images['hibit'])
            self.masks['lobit'] = engine.mask.from_surface(self.images['lobit'])
            self.masks['lobit_corrupt'] = engine.mask.from_surface(self.images['lobit_corrupt'])
#            self.mask = engine.mask.from_surface(self.images['lobit'])
            self.radius = (image.get_width()//2)
            self.sound = {}
            self.sound['blip'] = load_sound('blip.wav')
            self.sound['blip'].set_volume(0.5)
        self.image = self.images['hibit']
        self.mask = self.masks['hibit']     ###
        self.current_image = 'hibit'
        self.rect = engine.Rect(0,0,11,11)      ###
#        self.rect = engine.Rect(0,0,42,42)
        self.rect.x = int(self.x) - (self.image.get_width()//2)
        self.rect.y = int(self.y) - (self.image.get_height()//2)
        if not self.matrix.adjust:
            self.vel = 5
        else:
            self.vel = 10
        self.state_changed = False
        self.direction = 'd'    ###?
        self.node_previous = None

    def state_change(self):
        if self.current_image == 'hibit':
            if self.dtype == 'noncorrupt':
                self.image = self.images['lobit']
                self.mask = self.masks['lobit']     ###
            else:
                self.image = self.images['lobit_corrupt']
                self.mask = self.masks['lobit_corrupt']     ###
            self.current_image = 'lobit'
        else:
            self.image = self.images['hibit']
            self.mask = self.masks['hibit']     ###
            self.current_image = 'hibit'
        self.rect.x = int(self.x) - (self.image.get_width()//2)
        self.rect.y = int(self.y) - (self.image.get_height()//2)
#        if not env.debug:      ###
#            self.sound['blip'].play()
        self.state_changed = True

    def damage(self):
        self.matrix.nexus.data_loss(self)
        if not env.debug:
            self.sound['blip'].play()

    def move(self):
        if self.direction == 'd':
            self.y += self.vel
            self.rect.y = int(self.y) - (self.image.get_height()//2)
        else:
            if self.direction == 'l':
                self.x -= self.vel
                self.rect.x = int(self.x) - (self.image.get_width()//2)
            elif self.direction == 'r':
                self.x += self.vel
                self.rect.x = int(self.x) - (self.image.get_width()//2)

    def update(self):
        if not self.state_changed:
            node = self.matrix.node_check(self)
        else:
            self.state_changed = False
            node = None
        if node:
            response = node.communicate(self)
            if not response:
                self.matrix.nexus.data_loss(self)
            self.direction = response
            self.node_previous = node.id
            self.state_change()
        else:
            self.move()

