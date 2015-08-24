from __future__ import division
import env
engine = env.engine
from pulse import Pulse


class Surge(Pulse):

    def __init__(self,  matrix, x, y):
        direction = 'd'
        targets = [matrix.avatars]
        if not self.images:
            self.images = {}
            color = (100,100,200)
            image = engine.Surface((22,22), engine.SRCALPHA)
            points = [(p[0]*2,p[1]*2) for p in [(5,0),(9,1),(10,5),(9,9),(5,10),(1,9),(0,5),(1,1)]]
            engine.draw.polygon(image, color, points, 0)
            engine.draw.polygon(image, color, points, 1)
            self.images['hibit'] = image
            image = engine.Surface((22,22), engine.SRCALPHA)
            points = [(p[0]*2,p[1]*2) for p in [(5,2),(7,3),(8,5),(7,7),(5,8),(3,7),(2,5),(3,3)]]
            engine.draw.polygon(image, color, points, 0)
            engine.draw.polygon(image, color, points, 1)
            self.images['lobit'] = image
            if self.masks is None:
                self.masks = {}
            self.masks['hibit'] = engine.mask.from_surface(self.images['hibit'])
            self.masks['lobit'] = engine.mask.from_surface(self.images['lobit'])
            self.radius = (image.get_width()//2)
        Pulse.__init__(self, matrix, x, y, direction, targets)
        self.level = 0.5

    def hit(self):
        for target in self.targets:
            collided = engine.sprite.spritecollide(self, target, False, engine.sprite.collide_mask)
            if collided:
                collided[0].energy_surge(self.level)
                return True
        return False

