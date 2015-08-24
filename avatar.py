from __future__ import division
import env
engine = env.engine
from pulse import Pulse
from util import load_sound


class Avatar(engine.sprite.Sprite):
    images = None
    mask = None
    sound = None

    def __init__(self, matrix, x=None, y=None):
        engine.sprite.Sprite.__init__(self)
        self.matrix = matrix
        self.x = float(x)
        self.y = float(y)
        if not self.images:
            self.images = {}
            image = engine.Surface((50,50), engine.SRCALPHA)
            color1 = (80,100,120)
            color2 = (80,100,200)
            color3 = (50,50,200)
            points = [(p[0]*2,p[1]*2) for p in [(12,0),(16,10),(24,13),(16,18),(12,24),(8,18),(0,13),(8,10)]]
            engine.draw.polygon(image, color1, points, 0)
            points = [(p[0]*2,p[1]*2) for p in [(16,11),(23,13),(16,17)]]
            engine.draw.polygon(image, color2, points, 0)
            points = [(p[0]*2,p[1]*2) for p in [(8,11),(1,13),(8,17)]]
            engine.draw.polygon(image, color2, points, 0)
            points = [(p[0]*2,p[1]*2) for p in [(12,8),(15,11),(15,17),(12,20),(9,17),(9,11)]]
            engine.draw.polygon(image, color3, points, 0)
            self.images['normal'] = image
            self.mask = engine.mask.from_surface(self.images['normal'])
            self.sound = {}
            self.sound['pulse'] = load_sound('pulse.wav')
            self.sound['pulse'].set_volume(0.1)
            self.sound['surge'] = load_sound('pulse.wav')
            self.sound['surge'].set_volume(0.2)
            self.sound['spike'] = load_sound('explode.wav')
            self.sound['spike'].set_volume(0.2)
            self.sound['shot'] = load_sound('explode.wav')
            self.sound['shot'].set_volume(0.05)
            self.sound['explode'] = load_sound('explode.wav')
            self.sound['explode'].set_volume(0.1)
            self.sound['repair'] = load_sound('repair.wav')
            self.sound['repair'].set_volume(0.2)
        self.image = self.images['normal']
        self.rect = self.image.get_rect(center=(int(self.x),int(self.y)))
        self.rect_center = self.rect.inflate(-40,-40)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.radius = self.image.get_width()//2
        self.channel = engine.mixer.Channel(0)
        if not self.matrix.adjust:
            self.velocity = 5
            self.vel = self.velocity
            self.vel_max = 10
        else:
            self.velocity = 10
            self.vel = self.velocity
            self.vel_max = 25
        self.node_position = [int(self.x), int(self.y)]
        self.motion = {'u':False,'d':False,'l':False,'r':False}
        self.moving = False
        self.dir = 'v'
        self.dirs = {'u':-1,'d':1,'l':-1,'r':1}
        self.dir_offset = {'u':(0,-1),'d':(0,1),'l':(-1,0),'r':(1,0)}
        self.orient = {'u':'v','d':'v','l':'h','r':'h'}
        self.field = {'u':50,'d':450,'l':50,'r':450}
        self.control = {'z':False,'x':False}
        self.active = False
        self.pulse_charge = 1.0
        self.pulse_aim = 'u'
        self.power = 1.0
        self.targets = [self.matrix.bots]
        self.identity = 'Avatar'
        self.controls = {'u':False,'d':False,'l':False,'r':False,'z':False,'x':False}

    def node(self):
        return (int(self.x), int(self.y)) in self.matrix.nodes

    def node_thread(self):
        return self.x in [node[0] for node in self.matrix.nodex]

    def set_control(self, ctrl, state):
        if ctrl in self.controls:
            if self.controls[ctrl] != state:
                self.controls[ctrl] = state
            if ctrl in self.motion:
                if state:
                    self.motion_state(ctrl)
            else:
                self.control_state(ctrl)

    def motion_state(self, ctrl=None):
        if not self.moving and not self.control['x']:
            if ctrl:
                direction = ctrl
            else:
                direction = None
                for ctl in self.motion:
                    if self.controls[ctl]:
                        direction = ctl
                        break
                if not direction:
                    return
            if (direction == 'l' and self.node_position[0]>self.field['l']) or \
               (direction == 'r' and self.node_position[0]<self.field['r']) or \
               (direction == 'u' and self.node_position[1]>self.field['u']) or \
               (direction == 'd' and self.node_position[1]<self.field['d']):
                self.motion[direction] = self.controls[direction]
                self.moving = True

    def control_state(self, ctrl=None):
        if ctrl:
            control = ctrl
        else:
            control = None
            for ctl in self.control:
                if self.controls[ctl]:
                    control = ctl
                    break
        self.control[control] = self.controls[control]
        if control:
            self.active = self.control[control]
        else:
            self.active = False

    def move(self):
        for direction in ('u','d'):
            if self.motion[direction]:
                if self.dir == self.orient[direction]:
                    self.y += (self.dirs[direction] * self.vel)
                elif self.node():
                    self.dir = 'v'
                    self.y += (self.dirs[direction] * self.vel)
                self.pulse_aim = direction
                return
        for direction in ('l','r'):
            if self.motion[direction]:
                if self.dir == self.orient[direction]:
                    self.x += (self.dirs[direction] * self.vel)
                elif self.node():
                    self.dir = 'h'
                    self.x += (self.dirs[direction] * self.vel)
                self.pulse_aim = direction
                return

    def momentum(self):
        if self.moving:
            if self.node():
                self.node_position[0] = int(self.x)
                self.node_position[1] = int(self.y)
                for direction in self.motion:
                    if self.motion[direction]:
                        self.motion[direction] = False
                self.vel = self.velocity
                self.moving = False
                self.motion_state()

    def action(self):
        if self.active:
            if self.control['x']:
                self.node_repair()
            else:
                self.activate_pulse()

    def activate_pulse(self):
        if (self.pulse_charge >= 1.0) and (self.power > 0.1):
            if (engine.key.get_mods() & engine.KMOD_CTRL) or self.identity != 'Avatar':
                pulse_aim = self.pulse_aim
            else:
                pulse_aim = 'u'
            if pulse_aim == 'u':
                x = self.x
                y = self.y - (self.height/2)
            if pulse_aim == 'd':
                x = self.x
                y = self.y + (self.height/2)
            if pulse_aim == 'l':
                x = self.x - (self.width/2)
                y = self.y
            if pulse_aim == 'r':
                x = self.x + (self.width/2)
                y = self.y
            self.matrix.pulses.add( Pulse(self.matrix, x, y, pulse_aim, self.targets) )
            self.power -= 0.01
            if env.sound:
                self.sound['pulse'].play()
            self.pulse_charge = 0.0

    def datum_collide(self):
        collided = engine.sprite.spritecollide(self, self.matrix.data, False, self.matrix.collide_mask)
        for datum in collided:
            datum.damage()

    def shot(self):
        self.power -= 0.1
        if self.power < 0.0:
            self.power = 0.0
        if env.sound:
            self.sound['shot'].play()

    def energy_surge(self, level):
        self.power += level
        if self.power > 1.0:
            self.power = 1.0
        if env.sound:
            self.sound['surge'].play()

    def energy_spike(self, level):
        self.power -= level
        if self.power < 0.0:
            self.power = 0.0
        if env.sound:
            self.sound['spike'].play()

    def regenerate(self):
        if self.power < 1.0:
            self.power += 0.001
        if self.pulse_charge < 1.0:
            self.pulse_charge += 0.2

    def node_repair(self):
        if self.moving:
            return
        if engine.key.get_mods() & engine.KMOD_SHIFT:
            for direction in ('u','d','l','r'):
                if self.controls[direction]:
                    node = self.matrix.node_offset_check(self, self.dir_offset[direction])
                    break
            else:
                node = self.matrix.node_offset_check(self, self.dir_offset[self.pulse_aim])
        else:
            node = self.matrix.node_check(self)
        if node and node.offline:
            energy = 0.1
            if self.power > 0.3:
                node.repair(energy)
                self.power -= energy/10.0
                if env.sound:
                    if not self.channel.get_busy():
                        self.channel.play(self.sound['repair'])

    def destroyed(self):
        self.matrix.avatar = None
        self.kill()

    def update(self):
        self.action()
        self.move()
        self.momentum()
        self.rect.x = int(self.x)-(self.rect[2]//2)
        self.rect.y = int(self.y)-(self.rect[3]//2)
        if self.datum_collide():
            self.power -= 0.1
            if self.power < 0.01:
                self.power = 0.0
        self.regenerate()

