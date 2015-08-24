from __future__ import division
import env
engine = env.engine
from util import load_sound


class Charge(engine.sprite.Sprite):
    images = None
    radius = None
    sound = None

    def __init__(self, matrix, x, y, time):
        engine.sprite.Sprite.__init__(self)
        self.matrix = matrix
        self.x = int(x)
        self.y = int(y)
        if not self.images:
            self.images = {}
            color1 = (100,0,0)
            color2 = (200,0,0)
            color3 = (50,50,50)
            image = engine.Surface((22,22), engine.SRCALPHA)
            points = [(p[0]*2,p[1]*2) for p in [(5,0),(10,2),(10,8),(5,10),(0,8),(0,2)]]
            engine.draw.polygon(image, color1, points, 0)
            engine.draw.polygon(image, color1, points, 1)
            self.images['normal'] = image
            image = engine.Surface((22,22), engine.SRCALPHA)
            points = [(p[0]*2,p[1]*2) for p in [(5,1),(9,3),(9,7),(5,9),(0,7),(0,3)]]
            engine.draw.polygon(image, color2, points, 0)
            engine.draw.polygon(image, color2, points, 1)
            pts = [points[i] for i in range(0,len(points),2)]
            engine.draw.polygon(image, color3, pts, 1)
            pts = [points[i] for i in range(1,len(points),2)]
            engine.draw.polygon(image, color3, pts, 1)
            engine.draw.line(image, color3, points[0], points[3],1)
            engine.draw.line(image, color3, (18,10), (0,10),1)
            self.images['blink'] = image
            self.radius = (image.get_width()//2)
            self.sound = {}
            self.sound['explode'] = load_sound('explode.wav')
            self.sound['explode'].set_volume(0.15)
        self.image = self.images['normal']
        self.current_image = 'normal'
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.image_timer = 2
        self.timer = time
        if not self.matrix.adjust:
            self.tick_value = 1
        else:
            self.tick_value = 2
        self.node_attached = None
        self.level = 1.0

    def tick(self):
        self.timer -= self.tick_value
        if self.timer >= 0:
            return True
        else:
            return False

    def detonate(self):
        targets = engine.sprite.spritecollide(self, self.matrix.network, False, engine.sprite.collide_circle)
        for target in targets:
            target.damage(self.level)
        if env.sound:
            self.sound['explode'].play()
        self.kill()

    def update(self):
        self.image_timer -= 1
        if not self.image_timer:
            if self.current_image == 'normal':
                self.image = self.images['blink']
                self.current_image = 'blink'
            else:
                self.image = self.images['normal']
                self.current_image = 'normal'
            self.image_timer = 2
        time_remain = self.tick()
        if not time_remain:
            self.detonate()

