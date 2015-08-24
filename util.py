from __future__ import division
import os
import env
engine = env.engine
try:
    from threading import Timer
except ImportError:
    pass


def load_image(file_name):
    full_name = os.path.join('data', file_name)
    image = engine.image.load(full_name)
    return image


def load_sound(file_name):
    class No_Sound:
        def play(self): pass
    if not engine.mixer or not engine.mixer.get_init():
        return No_Sound()
    full_name = os.path.join('data', file_name)
    if env.platform != 'js':
        if os.path.exists(full_name):
            sound = engine.mixer.Sound(full_name)
        else:
            msg = 'File does not exist: '+full_name
            print(msg)
            return No_Sound
    else:
        sound = engine.mixer.Sound(full_name.split('.')[0] + '.mp3')
    return sound


timers = {}

class EventTimer:

    def __init__(self, eventid, time):
        self.eventid = eventid
        self.time = time
        self.timer = None
        self.repeat = True

    def run(self):
        engine.event.post( engine.event.Event(self.eventid) )
        if self.repeat:
            self.start()

    def start(self):
        self.repeat = True
        self.timer = Timer(self.time/1000.0, self.run, ([]))
        self.timer.start()

    def cancel(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None
        self.repeat = False

def set_timer(eventid, milliseconds):
    if eventid not in timers:
        timers[eventid] = EventTimer(eventid, milliseconds)
    if milliseconds:
        timers[eventid].start()
    else:
        timers[eventid].cancel()


class EventTimerJS:

    def __init__(self, eventid, time):
        self.eventid = eventid
        self.time = time
        self.repeat = True

    def run(self):
        engine.event.post( engine.event.Event(self.eventid) )
        if self.repeat:
            self.start()

    def start(self):
        self.repeat = True
        engine.time.timeout(self.time, self)

    def cancel(self):
        self.repeat = False

def set_timer_js(eventid, milliseconds):
    if eventid not in timers:
        timers[eventid] = EventTimerJS(eventid, milliseconds)
    timers[eventid].start()

if env.platform == 'js':
    set_timer = set_timer_js

