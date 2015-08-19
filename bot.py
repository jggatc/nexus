from __future__ import division
import random
import env
engine = env.engine
from avatar import Avatar
from charge import Charge


class Bot(Avatar):
    bot_image = False
    images = None
    mask = None

    def __init__(self, matrix, x, y):
        Avatar.__init__(self, matrix, x, y)
        if not self.bot_image:
            image = engine.Surface((50,50), engine.SRCALPHA)
            color1 = (200,100,120)
            color2 = (200,0,0)
            color3 = (200,0,0)
#            color4 = (100,100,120)
            points = [(p[0]*2,p[1]*2) for p in [(12,0),(16,10),(24,13),(16,18),(12,24),(8,18),(0,13),(8,10)]]
            engine.draw.polygon(image, color1, points, 0)
            points = [(p[0]*2,p[1]*2) for p in [(16,11),(23,13),(16,17)]]
            engine.draw.polygon(image, color2, points, 0)
            points = [(p[0]*2,p[1]*2) for p in [(8,11),(1,13),(8,17)]]
            engine.draw.polygon(image, color2, points, 0)
            points = [(p[0]*2,p[1]*2) for p in [(12,8),(15,11),(15,17),(12,20),(9,17),(9,11)]]
            engine.draw.polygon(image, color3, points, 0)
#            points = [(p[0]*2,p[1]*2) for p in [(12,1),(12,23)]]
#            engine.draw.line(image, color4, points[0], points[1],1)
            image = engine.transform.flip(image, True, True)           
            self.images['normal'] = image
            self.mask = engine.mask.from_surface(self.images['normal'])
            self.bot_image = image
        self.image = self.images['normal']
        self.rect = self.image.get_rect(center=(int(self.x),int(self.y)))
        self.targets = [self.matrix.avatars]
        self.field = {'u':50,'d':350,'l':50,'r':450}
#        self.targets = (self.matrix.data, self.matrix.avatars)
        self.pulse_aim = 'd'
        self.nemesis = self.matrix.avatar
        self.identity = 'Bot'
        self.motion['d'] = True
        self.moving = True
        self.behaviours = {'roam':self.auto_move, 'node_attack':self.node_damage, 'target':self.target, 'evade':self.evade}     ###
        self.behaviours_types = list(self.behaviours.keys())   ###
        self.behaviours_special = {'move_reverse':self.move_reverse, 'move_forward':self.move_forward, 'inactive':self.offline, 'stalk':self.stalk}     ###
        self.behaviour = self.behaviours['roam']
#        self.behaviour = None
        self.behaviour_type = 'roam'

    def behaviour_mode(self):
#        self.behaviour = self.behaviours_special['stalk']      ###
#        self.behaviour_type = 'stalk'
#        return
#        self.behaviour = self.behaviours['stalk']       ###
#        return
#        if self.matrix.node_damage_check(self.nemesis):     ###
#            self.behaviour = self.behaviours['target']
#            self.behaviour_type = 'target'
#            return

#        if self.power < 0.1:       ###
#            self.behaviour = self.behaviours_special['move_reverse']
#            self.behaviour_type = 'move_reverse'
#            return
        self.behaviour = self.behaviours[random.choice(self.behaviours_types)]     ###
#        self.behaviour = self.behaviours[random.choice(self.behaviours.keys())]
        return

###
#target doing node repair with x key
#leave area if low on power

    def action(self):
        pass

    def shot(self):
        Avatar.shot(self)
        self.behaviour = self.behaviours['evade']      ###
        self.behaviour_type = 'evade'
        if self.power <= 0.0:   ###
            if not env.debug:
                self.sound['explode'].play()
            self.kill()

    def auto_move(self):
        if not self.moving:
            direction_choice = False
            while not direction_choice:
                direction = random.choice(self.matrix.directions)
                if (direction == 'l' and self.node_position[0]>self.field['l']) or \
                   (direction == 'r' and self.node_position[0]<self.field['r']) or \
                   (direction == 'u' and self.node_position[1]>self.field['u']) or \
                   (direction == 'd' and self.node_position[1]<self.field['d']):
                   direction_choice = True
#            self.pulse_aim = direction      ###
            self.motion[direction] = True
            self.moving = True

    def momentum(self):
        Avatar.momentum(self)
        if not self.moving:
            if self.behaviour_type == 'move_reverse':
                return
            if not self.matrix.charge_check(self):
                self.behaviour = None
                self.behaviour_type = None
            else:
                self.behaviour = self.behaviours['roam']
                self.behaviour_type = 'roam'

    def auto_shoot(self):
        if random.random() > 0.95:
            self.activate_pulse()

    def target(self):
        if not self.matrix.node_damage_check(self.nemesis):
            self.behaviour = None
            self.behaviour_type = None
            return
        if not self.moving:
            if self.x == self.nemesis.x:
                if self.y < self.nemesis.y:
                    self.pulse_aim = 'd'
                elif self.y > self.nemesis.y:
                    self.pulse_aim = 'u'
                self.activate_pulse()
#                else:
#                    self.behaviour = None
            elif self.y == self.nemesis.y:
                if self.x > self.nemesis.x:
                    self.pulse_aim = 'l'
                elif self.x < self.nemesis.x:
                    self.pulse_aim = 'r'
                self.activate_pulse()
            else:
                if self.x > self.nemesis.x:
                    direction = 'l'
                else:
                    direction = 'r'
                self.motion[direction] = True
                self.moving = True

    def stalk(self):    ###
        if self.moving:
            return None
        directions = []
        if self.x > self.nemesis.x:
            directions.append('l')
        else:
            directions.append('r')
        if self.y > self.nemesis.y:
            directions.append('u')
        else:
            directions.append('d')
        if directions:
            direction = random.choice(directions)
        else:
            direction = None
        if not direction:
            self.behaviour = None
            self.behaviour_type = None
        else:
            self.motion[direction] = True       ###
            self.moving = True
        return direction

    def evade(self):
        if self.moving:
#        if self.moving:
            return None
        if self.matrix.separation(self, self.nemesis) > 100:    ###
            self.behaviour = None
            self.behaviour_type = None
            return None
        directions = []
        if self.x == self.nemesis.x:
            if self.node_position[0]>self.field['l']:
                directions.append('l')
            else:
                directions.append('r')
            if self.node_position[0]<self.field['r']:
                directions.append('r')
            else:
                directions.append('l')
        elif self.y == self.nemesis.y:
            if self.node_position[1]>self.field['u']:
                directions.append('u')
            else:
                directions.append('d')
            if self.node_position[1]<self.field['d']:
                directions.append('d')
            else:
                directions.append('u')
        if directions:   ###
            direction = random.choice(directions)
            self.motion[direction] = True
            self.moving = True
            return direction
#        if self.matrix.separation(self, self.nemesis) > 100:
#            self.behaviour = None
#            self.behaviour_type = None
#            return None
        if self.x > self.nemesis.x:
            if self.node_position[0]<self.field['r']:
                directions.append('r')
            else:
                directions.append('l')
        else:
            if self.node_position[0]>self.field['l']:
                directions.append('l')
            else:
                directions.append('r')
        if self.y > self.nemesis.y:
            if self.node_position[1]<self.field['d']:
                directions.append('d')
            else:
                directions.append('u')
        else:
            if self.node_position[1]>self.field['u']:
                directions.append('u')
            else:
                directions.append('d')
        if directions:
            direction = random.choice(directions)
        else:
            direction = None
        if direction:   ###
            self.motion[direction] = True
            self.moving = True
        return direction

    def move_destination(self, position):   ###
        pass

    def move_forward(self):     ###
        if not self.moving:
            if self.y > self.field['u']:
                self.behaviour = None
                self.behaviour_type = None
            else:
                self.motion['d'] = True
                self.moving = True

    def move_reverse(self):     ###
        if not self.moving:
            self.field['u'] = -1000      ###
            if self.y < self.field['u']:
                self.behaviour = self.behaviours_special['inactive']
                self.behaviour_type = 'inactive'
            else:
                self.motion['u'] = True
                self.moving = True

    def offline(self):      ###
        if self.power > 0.3:
            self.behaviour = self.behaviours_special['move_forward']
            self.behaviour_type = 'move_forward'

    def retreat(self):      ###
        self.behaviour = self.behaviours_special['move_reverse']
        self.behaviour_type = 'move_reverse'

    def node_damage(self, position=None):
        if self.power < 0.2 or random.random() > 0.1:   ###
#        if self.power < 0.2:
            self.behaviour = None
            self.behaviour_type = None
            return
        if not position:
            node = self.matrix.node_check(self)
            if node and not node.offline and node.id[1] != 1:
#            if node and not node.shutdown and node.id[1] != 1:
                charge = Charge(self.matrix, self.x, self.y, 90)
                self.matrix.charges.add(charge)
        else:
            charge = Charge(self.matrix, position[0], position[1], 90)
            self.matrix.charges.add(charge)
        self.behaviour = self.behaviours['roam']
        self.behaviour_type = 'roam'

    def update(self):
        if not self.behaviour:
            self.behaviour_mode()
        if self.behaviour:
            self.behaviour()
#        self.auto_shoot()      ###
        Avatar.update(self)

