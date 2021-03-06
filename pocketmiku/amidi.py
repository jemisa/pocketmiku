#!/usr/bin/env python
# coding: utf-8
"""
Module to handle interaction with amidi.
"""

from subprocess import call, check_output

hardware_port = None

def detectHardwarePort():
    """Automatically detect the NSX-39 port."""
    global hardware_port
    devices = check_output(['amidi', '-l'])
    for line in devices.split('\n'):
        if line.startswith('IO') and "NSX-39" in line:
            hw = line[line.index('hw'):]
            hw = hw[:hw.index(' ')]
            hardware_port = hw
            return
    raise ValueError("Couldn't find an NSX-39 T-T")

def send(s):
    """Send a raw MIDI string to the NSX-39."""
    if not hardware_port:
        detectHardwarePort()
    call(['amidi', '-p', hardware_port, '-S', s])

def read():
    """Reads from the device for one second and returns any data received."""
    if not hardware_port:
        detectHardwarePort()
    return check_output(['amidi', '-p', hardware_port, '-d', '-t', '1'])

def sendAndGetResponse(s):
    """Sends a string and then waits one second to get a response."""
    if not hardware_port:
        detectHardwarePort()
    # This is really ugly and I need to find a way to talk midi directly instead of this...
    cmd = "amidi -p '%s' -d -t 1 & amidi -p '%s' -S '%s' && wait $(jobs -p)" % (hardware_port, hardware_port, s)
    return check_output(cmd, shell=True)

