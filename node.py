from __future__ import division
import random
import env
engine = env.engine


class Node(engine.sprite.Sprite):
    images = None
    radius = None
    sound = None

    def __init__(self, matrix, x, y, identity):
        engine.sprite.Sprite.__init__(self)
        self.id = identity
        self.matrix = matrix
        self.x = x
        self.y = y
        if not self.images:
            self.images = {}
            image = engine.Surface((50,50), engine.SRCALPHA)
            points = [(p[0]*5,p[1]*5) for p in [(5,0),(9,1),(10,5),(9,9),(5,10),(1,9),(0,5),(1,1)]]
            color1 = (50,80,100)
            color2 = (8,10,120)
            engine.draw.polygon(image, color1, points, 0)
            engine.draw.aalines(image, color2, True, points, 1)
            pts = [points[i] for i in range(0,len(points),2)]
            engine.draw.lines(image, color2, True, pts, 1)
            pts = [points[i] for i in range(1,len(points),2)]
            engine.draw.lines(image, color2, True, pts, 1)
            pts = [points[i] for i in range(0,len(points),4)]
            engine.draw.lines(image, color2, False, pts, 1)
            pts = [points[i] for i in range(2,len(points),4)]
            engine.draw.lines(image, color2, False, pts, 1)
            self.images['node_operational'] = image
            image = engine.Surface((50,50), engine.SRCALPHA)
            color1 = (50,0,0)
            color2 = (20,40,60)
            engine.draw.polygon(image, color1, points, 0)
            engine.draw.aalines(image, color2, True, points, 1)
            pts = [points[i] for i in range(0,len(points),2)]
            engine.draw.lines(image, color2, True, pts, 1)
            pts = [points[i] for i in range(1,len(points),2)]
            engine.draw.lines(image, color2, True, pts, 1)
            pts = [points[i] for i in range(0,len(points),4)]
            engine.draw.lines(image, color2, False, pts, 1)
            pts = [points[i] for i in range(2,len(points),4)]
            engine.draw.lines(image, color2, False, pts, 1)
            self.images['node_damaged'] = image
            image = engine.Surface((50,50), engine.SRCALPHA)
            color1 = (255,0,0)
            color2 = (20,40,60)
            engine.draw.polygon(image, color1, points, 0)
            engine.draw.aalines(image, color2, True, points, 1)
            pts = [points[i] for i in range(0,len(points),2)]
            engine.draw.lines(image, color2, True, pts, 1)
            pts = [points[i] for i in range(1,len(points),2)]
            engine.draw.lines(image, color2, True, pts, 1)
            pts = [points[i] for i in range(0,len(points),4)]
            engine.draw.lines(image, color2, False, pts, 1)
            pts = [points[i] for i in range(2,len(points),4)]
            engine.draw.lines(image, color2, False, pts, 1)
            self.images['node_failed'] = image
            self.images['operational'] = engine.transform.smoothscale(self.images['node_operational'], (9,9))
            self.images['damaged'] = engine.transform.smoothscale(self.images['node_damaged'], (9,9))
            self.images['failed'] = engine.transform.smoothscale(self.images['node_failed'], (9,9))
            self.radius = (image.get_width()//2)
        self.image = self.images['operational']
        self.current_image = 'operational'
        self.image_timer = 2
        self.rect = self.image.get_rect(center=(int(self.x),int(self.y)))
        self.return_value = [0,0]
        self.node_thread = self.id[0]
        self.node_port = None
        self.node_net, self.node_priority = self.node_connection()
        self.node_port, self.node_port_direction = self.set_node_port()
        self.power = 1.0
        self.integrity = 1.0
        self.offline = False
        self.shutdown = False
        self.delayed_message = 0
        self.delayed_message_mode = None

    def node_connection(self):
        nodes = {}
        for x,y in [(0,1),(-1,0),(1,0),(0,-1)]:
            id = self.id[0]+x,self.id[1]+y
            if id in self.matrix.node_id:
                nodes[id] = True
        node_priority = []
        port = [(0,1)]
        port.extend( random.choice([ [(-1,0),(1,0)],[(1,0),(-1,0)] ]) )
        for x,y in port:
            id = self.id[0]+x,self.id[1]+y
            if id in nodes:
                node_priority.append(id)
        self.return_value[0] = nodes
        self.return_value[1] = node_priority
        return self.return_value

    def set_node_port(self):
        for node in self.node_priority:
            if self.node_net[node]:
                if self.node_port != node:
                    self.node_port = node
                    break
        if self.node_port:
            if self.node_port[1] > self.id[1]:
                self.node_port_direction = 'd'
            else:
                if self.node_port[0] < self.id[0]:
                    self.node_port_direction = 'l'
                else:
                    self.node_port_direction = 'r'
        else:
            self.node_port = self.id[0],self.id[1]+1
            self.node_port_direction = 'd'
        self.return_value[0] = self.node_port
        self.return_value[1] = self.node_port_direction
        return self.return_value

    def communicate(self, datum):
        if not self.offline:
            if self.node_port == datum.node_previous:
                self.set_node_port()
            if self.node_port:
                return self.node_port_direction
            else:
                return None
        else:
            return None

    def transmit(self, node_id=None, message=None):
        if not node_id:
            for node in self.node_net:
                if not self.offline:
                    self.matrix.node[node].transmit(self.id, 'online')
                else:
                    self.matrix.node[node].transmit(self.id, 'offline')
        else:
            self.message_process(node_id, message)

    def message_process(self, node_id, message):
        if message == 'online':
            if node_id in self.node_net:
                self.node_net[node_id] = True
                self.node_port = None
                self.set_node_port()
        elif message == 'offline':
            if node_id in self.node_net:
                self.node_net[node_id] = False
                self.node_port = None
                self.set_node_port()
        elif message == 'bootup':
            if self.shutdown:
                self.shutdown = False
                self.offline = False
                self.image = self.images['operational']
                self.current_image = 'operational'
                for node in self.node_net:
                    self.node_net[node] = True
                self.node_port = None
                self.set_node_port()
                self.power = 1.0
                self.integrity = 1.0
                self.matrix.node_update(self)
                self.delayed_message = 3
                self.delayed_message_mode = 'bootup'
        elif message == 'shutdown':
            if not self.shutdown:
                self.shutdown = True
                self.offline = True
                self.image = self.images['damaged']
                self.current_image = 'damaged'
                self.matrix.node_update(self)
                self.delayed_message = 3
                self.delayed_message_mode = 'shutdown'

    def send_message(self):
        for node in self.node_net:
           self.matrix.node[node].transmit(self.id, self.delayed_message_mode)

    def disable(self):
        self.offline = True
        self.transmit()
        self.image = self.images['damaged']
        self.current_image = 'damaged'
        self.matrix.node_update(self)

    def enable(self):
        self.offline = False
        self.transmit()
        self.image = self.images['operational']
        self.current_image = 'operational'
        self.matrix.node_update(self, False)

    def damage(self, level):
        self.integrity -= level
        if self.integrity < 0.0:
            self.integrity = 0.0
        if not self.offline:
            if self.integrity <= 0.0:
                self.disable()

    def repair(self, level):
        self.integrity += level
        if self.integrity > 1.0:
            self.integrity = 1.0
        if self.offline:
            if self.integrity >= 1.0:
                self.enable()
        return self.offline

    def update(self):
        if self.delayed_message:
            self.delayed_message -= 1
            if self.delayed_message <= 0:
                self.send_message()
                self.delayed_message = 0
        self.image_timer -= 1
        if not self.image_timer:
            if self.current_image == 'damaged':
                self.image = self.images['failed']
                self.current_image = 'failed'
            elif self.current_image == 'failed':
                self.image = self.images['damaged']
                self.current_image = 'damaged'
            self.image_timer = 2

