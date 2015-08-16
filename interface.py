from __future__ import division
import env
engine = env.engine

import interphase
interphase.init(engine)


class MatrixInterface(interphase.Interface):

    def __init__(self, identity, matrix, control):
        self.matrix = matrix
        self.control = control
        interphase.Interface.__init__(self, identity, position=(self.matrix.width//2,self.matrix.height-50), color=(15,30,50), size=(200,100), control_minsize=(35,35), control_size='auto', control_response=100, moveable=False, position_offset=(0,98), font_color=(50,150,200), scroll_button='vertical')
        self.get_control('Activate').set_active(False)

    def add_controls(self):
        self.add(
            identity = 'Control',
            control_type = 'function_toggle',
            position = (100,90),
            size = 'auto_width',
            font_color = (125,175,200),
            control_list = ['Help','Main'],
            link = [['Bootup'],['Guide']],
            link_activated = True,
            control_outline = True)     ###link = [['Bootup','Activate'],['Guide']],
        self.add(
            identity = 'Bootup',
            control_type = 'control_toggle',
            position = (100,50),
            size = 'auto',
            font_color = (125,175,200),
            control_list = ['Bootup'],
            tip_list = ['Nexus activate'])
        self.add(
            identity = 'Activate',
            control_type = 'control_toggle',
            position = (100,50),
            size = 'auto',
            font_color = (125,175,200),
            control_list = ['Pause','Activate'],
            tip_list = ['Nexus pause','Nexus activate'])
        self.add(
            identity = 'DataProcessedTop',
            control_type = 'label',
            position = (60,44),
            size = (40,20),
            font_color = (125,175,200),
            control_list = ['0'],
            tip_list = ['Nexus Data Integration'])
        self.add(
            identity = 'DataProcessed',
            control_type = 'label',
            position = (60,84),
            size = (40,20),
            font_color = (125,175,200),
            control_list = ['0'],
            tip_list = ['Nexus Data Integration'])
        self.add(
            identity = 'DataProcessedTopLabel',
            control_type = 'label',
            position = (60,24),
            size = (40,20),
            font_color = (125,175,200),
            control_list = ['Top'],
            tip_list = ['Nexus Data Integration'])
        self.add(
            identity = 'DataProcessedLabel',
            control_type = 'label',
            position = (60,64),
            size = (40,20),
            font_color = (125,175,200),
            control_list = ['Current'],
            tip_list = ['Nexus Data Integration'])
        self.add(
            identity = 'Guide',
            control_type = 'textbox',
            position = (100,50),
            size = (170,70),
            color = (49,57,65),
            font_color = (125,175,200),
            font_size = 10,
            font_type = 'arial',
            control_list = [self.control.guide],
            label_display = False)

    def set_data_processed(self, dataprocessed):
        self.get_control('DataProcessed').set_value(str(dataprocessed))

    def set_data_processed_top(self, dataprocessed):
        self.get_control('DataProcessedTop').set_value(str(dataprocessed))

    def reset(self):
        self.control.set_panel_display()
        self.get_control('Activate').set_active(False)
        self.get_control('Bootup').set_active(True)

    def update(self):
        state = interphase.Interface.update(self)
        if state.control:
            if state.control == 'Bootup':
                self.control.set_panel_display()
                state.controls['Bootup'].set_active(False)
                state.controls['Activate'].set_active(True)
                self.matrix.nexus.initiation_activate()
            elif state.control == 'Activate':
                if state.value == 'Pause':
                    self.matrix.set_active(True)
                elif state.value == 'Activate':
                    self.matrix.set_active(False)

