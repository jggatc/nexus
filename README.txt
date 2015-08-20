Nexus - Data Processor Construct

Project site:
http://gatc.ca/projects/nexus/

PyWeek 20 entry:
https://www.pyweek.org/e/Nexus/


Dependencies:
Python 2.7+ (https://www.python.org/)
Pygame 1.9.1 (http://www.pygame.org/)

Usage:
Interphase 0.87 (http://gatc.ca/projects/interphase/)
>GUI interface module.
PyJ2D 0.27 (http://gatc.ca/projects/pyj2d/) / Jython 2.2.1+ (http://www.jython.org/)
>Optional to port Pygame app to Java environment of JVM 6.0+.
Pyjsdl 0.21 (http://gatc.ca/projects/pyjsdl/) / Pyjs 0.8.1_dev (http://www.pyjs.org/)
>Optional to port Pygame app to JS environment of Web browser.

Development tools:
cxFreeze
Bfxr


Nexus Guide:
Protect the integrity of Nexus by maintaining data flow through the node network.

Nexus's virtual presence is supported by its data processing and integration. As Nexus's gatekeeper, guard the data flow to Nexus while removing flashing corrupt data. Ensure data transmission by confronting the infiltrating bots and repair the nodes damaged by their energy charges. To sustain the responsibility, manage power reserves used by energy pulses and node repair, the network current restores power and energy surges provide power boost while energy spikes drain power. Nexus's integrity depends on the data, if Nexus senses a threat of system failure it will initiate network shutdown.

Controls
Bot forward (UP/KP8/w)
Bot reverse (DOWN/KP2/s)
Bot left (LEFT/KP4/a)
Bot right (RIGHT/KP6/d)
Bot shoot (SPACE/KP0/z/LMouse)
--directional (CTRL)
Node repair (x)
--directional (SHIFT)
Start/pause (Escape/r)
Sound toggle (o)
Panel toggle (p)

Status indicators
-Nexus integrity (grey)
-Bot power (blue)
-Data integration (green)


Instructions:
Nexus runs with Python2.7+ and the Pygame library. Alternatively, the app can run in the Java environment (http://www.java.com/getjava/) using Jython 2.2.1+ with the PyJ2D library. Obtain Jython (http://www.jython.org/) and install or put the standalone interpreter in or on the path of the app folder. Obtain PyJ2D from its project site (http://gatc.ca/projects/pyj2d/) or Github repository (https://github.com/jggatc/pyj2d/) and unpack the library in or on the path of the app folder. Run using the command ‘jython nexus.py’ or ‘java -jar jython.jar nexus.py’. Nexus 1.0 runs as a PyJ2D app with minor issues, which are fixed in Nexus 1.1 on the Github repository (https://github.com/jggatc/nexus/releases/). The app can also run in the JavaScript environment following Pyjs compilation with the Pyjsdl library, though there are issues with Nexus 1.0 that are partly addressed in Nexus 1.1, see Nexus project site for further information.


Released under the GPL3 license (http://www.gnu.org/licenses/gpl.html).

