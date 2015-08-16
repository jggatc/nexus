from __future__ import division
import env
engine = env.engine
from surge import Surge


class Spike(Surge):

    def __init__(self,  matrix, x, y):
        if not self.images:
            self.images = {}
            color1 = (200,0,0)
            color2 = (100,0,0)
            image = engine.Surface((22,22), engine.SRCALPHA)
            points = [(p[0]*2,p[1]*2) for p in [(5,0),(9,1),(10,5),(9,9),(5,10),(1,9),(0,5),(1,1)]]
            engine.draw.polygon(image, color1, points, 0)
            engine.draw.polygon(image, color1, points, 1)
            self.images['hibit'] = image
            image = engine.Surface((22,22), engine.SRCALPHA)
            points = [(p[0]*2,p[1]*2) for p in [(5,2),(7,3),(8,5),(7,7),(5,8),(3,7),(2,5),(3,3)]]
            engine.draw.polygon(image, color2, points, 0)
            engine.draw.polygon(image, color2, points, 1)
            self.images['lobit'] = image
            self.mask = engine.mask.from_surface(self.images['hibit'])
            self.radius = (image.get_width()//2)
        Surge.__init__(self, matrix, x, y)
        self.level = 0.5

    def hit(self):
        for target in self.targets:
            collided = engine.sprite.spritecollide(self, target, False, engine.sprite.collide_mask)
            if collided:
                collided[0].energy_spike(self.level)
                return True
        return False

