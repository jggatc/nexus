from __future__ import division
import env
engine = env.engine


class Pulse(engine.sprite.Sprite):
    images = None
    masks = None
    radius = None

    def __init__(self, matrix, x, y, direction, targets):
        engine.sprite.Sprite.__init__(self)
        self.matrix = matrix
        self.x = float(x)
        self.y = float(y)
        self.direction = direction
        if not self.images:
            self.images = {}
            color = (200,200,200)
            image = engine.Surface((11,11), engine.SRCALPHA)
            points = [(5,0),(9,1),(10,5),(9,9),(5,10),(1,9),(0,5),(1,1)]
            engine.draw.polygon(image, color, points, 0)
            engine.draw.polygon(image, color, points, 1)
            self.images['hibit'] = image
            image = engine.Surface((11,11), engine.SRCALPHA)
            points = [(5,2),(7,3),(8,5),(7,7),(5,8),(3,7),(2,5),(3,3)]
            engine.draw.polygon(image, color, points, 0)
            engine.draw.polygon(image, color, points, 1)
            self.images['lobit'] = image
            self.masks = {}
            self.masks['hibit'] = engine.mask.from_surface(self.images['hibit'])
            self.masks['lobit'] = engine.mask.from_surface(self.images['lobit'])
            self.radius = (image.get_width()//2)
        self.image = self.images['hibit']
        self.mask = self.masks['hibit']
        self.current_image = 'hibit'
        self.image_timer = 2
        self.rect = self.image.get_rect(center=(int(self.x),int(self.y)))
        if not self.matrix.adjust:
            if direction in ('u','l'):
                self.vel = -10
            else:
                self.vel = 10
        else:
            if direction in ('u','l'):
                self.vel = -20
            else:
                self.vel = 20
        self.targets = targets

    def hit(self):
        for target in self.targets:
            collided = engine.sprite.spritecollide(self, target, False, self.matrix.collide_mask)
            if collided:
                collided[0].shot()
                return True
        for target in [self.matrix.data]:
            collided = engine.sprite.spritecollide(self, target, False, self.matrix.collide_mask)
            if collided:
                collided[0].damage()
                return True
        return False

    def move(self):
        if self.direction in ('u','d'):
            if -25 < self.y < self.matrix.height:
                self.y += self.vel
                self.rect.y = int(self.y)
            else:
                self.kill()
        else:
            if -25 < self.y < self.matrix.height:
                self.x += self.vel
                self.rect.x = int(self.x)
            else:
                self.kill()

    def update(self):
        self.image_timer -= 1
        if not self.image_timer:
            if self.current_image == 'hibit':
                self.image = self.images['lobit']
                self.mask = self.masks['lobit']
                self.current_image = 'lobit'
            else:
                self.image = self.images['hibit']
                self.mask = self.masks['hibit']
                self.current_image = 'hibit'
            self.image_timer = 2
        self.move()
        if self.hit():
            self.kill()

