from __future__ import division
import math
import random
from datum import Datum
from node import Node
from core import Core
from avatar import Avatar
from bot import Bot
from surge import Surge
from spike import Spike
from control import Control
import env
engine = env.engine


class Matrix:

    def __init__(self):
        engine.display.set_caption('Nexus')
        self.screen = engine.display.get_surface()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.background = engine.Surface((self.width, self.height))
        self.control = Control(self)
        if env.platform in ('pc','jvm'):
            self.adjust = False
        else:
            self.adjust = False     ###
#            self.adjust = True
#        if not env.platform == 'js':    #unidentity problem    ###
        self.collide_mask = engine.sprite.collide_mask
#        else:
#            self.collide_mask = None
        self.data = engine.sprite.RenderUpdates()
        self.network = engine.sprite.RenderUpdates()    #nodes
        self.network_node = engine.sprite.RenderUpdates()   #nodes to update
        self.level = 1
        self.bot = None     ###
        self.bots = engine.sprite.RenderUpdates()
        self.avatar = Avatar(self, 250, 550)
        self.avatars = engine.sprite.RenderUpdates(self.avatar)
        self.pulses = engine.sprite.RenderUpdates()
        self.charges = engine.sprite.RenderUpdates()
        self.data_construct = []     ###
        engine.display.set_icon(self.avatar.image)
        self.quit = False
        self.update_rect = []
        self.nodes = [(x,y) for x in range(50,self.width,50) for y in range(50,self.height+50,50)]
        self.node_id = [(x,y) for x in range(1,int(self.width/50)) for y in range(1,int((self.height+50)/50))]
        self.nodex = [(x,-20) for x in range(50,self.width,50)]
        self.node = {}
        for i in range(len(self.nodes)):
            node_pos = self.nodes[i]
            identity = self.node_id[i]
            if identity == (5,10):
                node = Core(self,node_pos[0],node_pos[1],identity)
                self.nexus = node
            else:
                node = Node(self,node_pos[0],node_pos[1],identity)
            self.node[identity] = node
            self.network.add(node)
        self.directions = ['u','d','l','r']
        self.data_count = 0
        self.data_max = 25
        self.time_prev = 0
        self.time_diff = 0
        self.data_event = engine.USEREVENT
        self.data_event_time = 500
        self.surge_event = engine.USEREVENT+1
        self.surge_event_time = 15555
        self.spike_event = engine.USEREVENT+2
        self.spike_event_time = 21500
        self.bot_event = engine.USEREVENT+3     ###
        self.bot_event_time = 5000
        self.level_event = engine.USEREVENT+4     ###
        self.level_event_time = 60000
        if env.platform == 'pc':
            self.set_timer = engine.time.set_timer
        else:
            from util import set_timer
            self.set_timer = set_timer
        self.draw_grid()
        self.active = True
#        self.init()

    def draw_grid(self):
        self.background.fill((20,20,20))
        for line in range(0,self.width+50,50):
            engine.draw.line(self.background, (43,50,58), (0,line), (self.height,line), 3)
        for line in range(0,self.height+50,50):
            engine.draw.line(self.background, (43,50,58), (line,0), (line,self.width), 3)
        self.network.update()
        self.update_rect.extend( self.network.draw(self.background) )
        self.screen.blit(self.background, (0,0))
        self.update_rect.append(self.screen.get_rect())

    def init(self):
        self.data_generator()
        self.set_timer(self.data_event,self.data_event_time)
        self.set_timer(self.surge_event,self.surge_event_time)
        self.set_timer(self.spike_event,self.spike_event_time)
        self.set_timer(self.bot_event,self.bot_event_time)
        self.set_timer(self.level_event,self.level_event_time)
#        self.bot_generator()

    def set_active(self, state):
        self.active = state

    def node_check(self, entity):
        thread = int(entity.x)
        for i, node in enumerate(self.nodes):
            if node[0] == thread:
                if node[1] == int(entity.y):
                    return self.node[self.node_id[i]]
        return None

    def node_offset_check(self, entity, offset=(0,0)):
        pos_offset_x = offset[0] * 50
        pos_offset_y = offset[1] * 50
        thread = int(entity.x) + pos_offset_x
        for i, node in enumerate(self.nodes):
            if node[0] == thread:
                if node[1] == (int(entity.y) + pos_offset_y):
                    return self.node[self.node_id[i]]
        return None

    def node_update(self, node, status=True):
        if status:
            self.network_node.add(node)
        else:
            self.network_node.remove(node)
            rect = self.screen.blit(node.image,node.rect)
            rect = self.background.blit(node.image,node.rect)
            self.update_rect.append(rect)
        return None

    def transmit(self, node, message=None):
        node.transmit(message)

    def charge_check(self, entity):
        for charge in self.charges:
            if charge.x == int(entity.x) and charge.y == int(entity.y):
                return True
        return False

    def node_damage_check(self, entity):
        for node in self.network_node:
            if node.x == int(entity.x) and node.y == int(entity.y):
                return True
        return False

    def separation(self, entity, other):
        return ((entity.x-other.x)**2 + (entity.y-other.y)**2)**0.5

    def level_set(self):    ###
        self.level += 1

    def data_generator(self):
        if self.data_count < self.data_max:
            node = random.choice(self.nodex)
            if random.random() > 0.1:
                self.data.add( self.data_retrival(node[0], node[1], self.nexus.data_type[0]) )
            else:
                self.data.add( self.data_retrival(node[0], node[1], self.nexus.data_type[1]) )
            self.data_count += 1

    def bot_generator(self):
#        if not self.bots.sprites():    ###
        node = random.choice(self.nodex)
        self.bot = Bot(self, node[0], node[1])
        self.bots.add(self.bot)

    def bot_check(self):    ###
        if len(self.bots.sprites()) < self.level:
            self.bot_generator()

    def surge_generator(self):
        node = random.choice(self.nodex)
        self.pulses.add( Surge(self, node[0], node[1]) )

    def spike_generator(self):
        node = random.choice(self.nodex)
        self.pulses.add( Spike(self, node[0], node[1]) )

    def data_retrival(self, x, y, dtype):
        if self.data_construct:
            datum = self.data_construct.pop()
            datum.x = float(x)
            datum.y = float(y)
            datum.dtype = dtype
            datum.image = datum.images['hibit']
            datum.current_image = 'hibit'
            datum.rect.x = int(datum.x) - (datum.image.get_width()//2)
            datum.rect.y = int(datum.y) - (datum.image.get_height()//2)
            datum.state_changed = False
            datum.direction = 'd'    ###?
            datum.node_previous = None
            return datum
        else:
            return Datum(self, x, y, dtype)

    def data_status(self):
        rect = engine.draw.line(self.screen, (0,0,0), (self.width-40,self.height-30), (self.width-10,self.height-30),2)
        self.update_rect.append(rect)
        if self.avatar:
            integrity = int(self.nexus.integrity*30)
            rect = engine.draw.line(self.screen, (50,80,100), (self.width-40,self.height-30), (self.width-40+integrity,self.height-30),2)
            self.update_rect.append(rect)
        rect = engine.draw.line(self.screen, (0,0,0), (self.width-40,self.height-20), (self.width-10,self.height-20),2)
        self.update_rect.append(rect)
        if self.avatar:
            power = int(self.avatar.power*30)
            rect = engine.draw.line(self.screen, (50,50,200), (self.width-40,self.height-20), (self.width-40+power,self.height-20),2)
#            rect = engine.draw.line(self.screen, (0,200,0), (self.width-40,self.height-20), (self.width-40+power,self.height-20),2)
            self.update_rect.append(rect)
        if self.avatar:
            data = self.nexus.data_integration
            rect = engine.draw.line(self.screen, (0,200,0), (self.width-40,self.height-10), (self.width-40+data,self.height-10),2)
#            rect = engine.draw.line(self.screen, (0,200,0), (self.width-40,self.height-20), (self.width-40+power,self.height-20),2)
            self.update_rect.append(rect)

    def update_time(self):      ###
        time = self.control.clock.get_time()
        self.time_diff = self.time_prev - time
        self.time_prev = time
        return self.time_diff

    def shutdown(self):
        if env.platform == 'pc':
            self.set_timer(self.data_event,0)
            self.set_timer(self.surge_event,0)
            self.set_timer(self.spike_event,0)
            self.set_timer(self.bot_event,0)
            self.set_timer(self.level_event,0)
        else:
            from util import timers
            try:
                timers[self.data_event].cancel()
                timers[self.surge_event].cancel()
                timers[self.spike_event].cancel()
                timers[self.bot_event].cancel()
                timers[self.level_event].cancel()
            except:
                pass
        self.control.interface.reset()      ###
        for bot in self.bots:   ###
            bot.retreat()
#        self.matrix.level = 1      ###
#        self.data_count = 0

    def pause_mode(self):
        self.control.panel.clear(self.screen,self.background)
        for group in [self.pulses, self.charges, self.data, self.bots, self.avatars]:
            group.clear(self.screen,self.background)
        for group in [self.pulses, self.charges, self.data, self.bots, self.avatars]:
            rects = group.draw(self.screen)
            self.update_rect.extend(rects)
        self.control.panel.update()
        rects = self.control.panel.draw(self.screen)
        self.update_rect.extend(rects)
        self.control.update()

    def update(self):
        if not self.active:
            self.pause_mode()
            return
        self.update_rect[:] = []
        self.control.panel.clear(self.screen,self.background)
        for group in [self.pulses, self.charges, self.data, self.bots, self.avatars]:
            group.clear(self.screen,self.background)
        self.network_node.update()
        self.network_node.draw(self.background)
        rects = self.network_node.draw(self.screen)
        self.update_rect.extend(rects)
        for group in [self.pulses, self.charges, self.data, self.bots, self.avatars]:
            group.update()
            rects = group.draw(self.screen)
            self.update_rect.extend(rects)
        self.control.panel.update()
        rects = self.control.panel.draw(self.screen)
        self.update_rect.extend(rects)
        self.data_status()
        self.control.update()

