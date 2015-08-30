#!/usr/bin/env python

#Nexus - Data Processor Construct

#Copyright (C) 2015 James Garnon <http://gatc.ca/>
#Released under the GPL3 License <http://www.gnu.org/licenses/>

from __future__ import division
import os, sys
if os.name in ('posix', 'nt', 'os2', 'ce', 'riscos'):
    import pygame as engine
    platform = 'pc'
elif os.name == 'java':
    import pyj2d as engine
    platform = 'jvm'
else:
    import pyjsdl as engine
    platform = 'js'
import env
env.engine = engine
env.platform = platform
from matrix import Matrix


def setup(width, height):
    engine.init()
    engine.display.set_mode((width,height))
    engine.event.set_blocked(engine.MOUSEMOTION)
    engine.mixer.init(11025, size=-16, channels=2, buffer=4096)
    if engine.mixer and not engine.mixer.get_init():
        print ('Warning, no sound')
        engine.mixer = None


matrix = None
def run_js():
    matrix.update()
    engine.display.update(matrix.update_rect)
    matrix.control.clock.tick(30)

def prerun_js():
    global matrix
    matrix = Matrix()
    engine.display.update(matrix.update_rect)
    engine.display.setup(run_js)

def main_js():
    setup(500,500)
    engine.display.setup(prerun_js)


def run():
    while not matrix.quit:
        matrix.update()
        engine.display.update(matrix.update_rect)
        matrix.control.clock.tick(30)
    matrix.shutdown()
    engine.quit()

def prerun():
    global matrix
    matrix = Matrix()
    engine.display.update(matrix.update_rect)
    run()

def main():
    setup(500,500)
    prerun()

if __name__ == '__main__':
    if platform in ('pc','jvm'):
        main()
    elif platform == 'js':
        main_js()

