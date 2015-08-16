from __future__ import division
import env
engine = env.engine
from node import Node
from avatar import Avatar
from util import load_sound


class Core(Node):

    def __init__(self, matrix, x, y, identity):
        Node.__init__(self, matrix, x, y, identity)
        self.name = 'Nexus'
        self.images['operational'] = self.images['node_operational']
        self.images['damaged'] = self.images['node_damaged']
        self.images['failed'] = self.images['node_failed']
        self.image = self.images['operational']
        self.rect = self.image.get_rect(center=(int(self.x),int(self.y)))
        self.radius = (self.image.get_width()//2)
        self.sound = {}
        self.sound['bootup'] = load_sound('powerup.wav')
        self.sound['bootup'].set_volume(0.3)
        self.matrix.node_update(self)
        self.initiation = False
        self.initiate = False
        self.init_count = 3
        self.aware = False     ###
        self.data_type = ['noncorrupt','corrupt']
        self.data_process = 0
        self.data_corruption = 0
        self.data_integration = 0
        self.data_integration_top = 0       ###
        self.integrity_high_color = engine.Color(80,100,220)
        self.integrity_low_color = engine.Color(180,50,50)
        self.integrity_loss = -0.001    ###
        self.integrity = 1.0
        self.count = 10      ###

    def init(self):
        if not self.initiate:
            if self.init_count == 3:
                self.system_bootup()
            engine.event.clear()
            if not self.matrix.avatar.moving:
                self.matrix.avatar.set_control('u', True)
                self.matrix.avatar.set_control('u', False)
                self.init_count -= 1
                if not self.init_count:
                    self.matrix.init()
                    self.initiation = False
                    self.initiate = True
                    self.aware = True      ###

    def initiation_activate(self):
        if not self.initiate:
            self.init_count = 3     ###
            self.initiation = True

    def node_power_transfer(self):      ###
        pass
        #transfer power to node if not node.shutdown
        #node lose power with data transfer, shutdown when low power

    def communicate(self, datum):
        self.data_processing(datum)
        return self.node_port_direction

    def data_processing(self, datum):
        if datum.dtype == 'noncorrupt':
            self.data_process += 1
        elif datum.dtype == 'corrupt':
            self.data_corruption += 1
        self.matrix.data.remove(datum)
        self.matrix.data_construct.append(datum)
        self.matrix.data_count -= 1

    def data_loss(self, datum):
        self.matrix.data.remove(datum)
        self.matrix.data_construct.append(datum)
        self.matrix.data_count -= 1

    def system_integrity(self):
        data_processed = (self.data_process/25.0) + (-self.data_corruption/5.0)      ###
        self.integrity += (self.integrity_loss + data_processed)
#        self.integrity += ( (self.integrity_loss) + (self.data_process/50.0) + (-self.data_corruption/10.0) )
        self.data_integration += data_processed
        if self.integrity > 1.0:
            self.integrity = 1.0
        self.data_process = 0
        self.data_corruption = 0
        if self.integrity > 0.0:
            self.matrix.control.interface.set_data_processed(int(self.data_integration*10))     ###
            return True
        else:
            if self.data_integration > self.data_integration_top:
                self.data_integration_top = self.data_integration
            self.matrix.control.interface.set_data_processed(int(self.data_integration*10))     ###
            self.matrix.control.interface.set_data_processed_top(int(self.data_integration_top*10))     ###
            return False

    def system_awaken(self):       ###
        if self.init_count == 3:
            self.reboot()
            self.system_bootup()
        engine.event.clear()
        self.init_count -= 1
        if not self.init_count:
            self.matrix.init()
            self.initiation = False
            self.initiate = True

    def reboot(self):
#        self.initiation = False     ###
        self.initiate = False
#        self.init_count = 3
        self.data_process = 0
        self.data_corruption = 0
        self.data_integration = 0
        self.integrity = 1.0
        self.count = 10
        self.matrix.level = 1
        self.matrix.bots.empty()
        self.matrix.data_count = 0
        self.matrix.avatar.pulse_charge = 1.0
        self.matrix.avatar.integrity = 1.0
#        self.matrix.network_node.empty()   ###?

    def system_bootup(self):
        if not env.debug:   ###
            self.sound['bootup'].play()
        self.transmit(self.id, 'bootup')

    def system_failure(self):
        if not self.shutdown:
            self.matrix.shutdown()
            self.initiate = False       ###
            self.transmit(self.id, 'shutdown')

    def update(self):
        Node.update(self)
        if self.initiation:
            if self.aware:
                self.system_awaken()
            else:
                self.init()
        if not self.initiate:
            return
        integrity = self.system_integrity()
        if not integrity:
            self.system_failure()

