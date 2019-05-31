#!/usr/bin/env python
"""
@file    runner.py
@author  Lena Kalleske
@author  Daniel Krajzewicz
@author  Michael Behrisch
@author  Jakob Erdmann
@date    2009-03-26
@version $Id: runner.py 18096 2015-03-17 09:50:59Z behrisch $

Tutorial for traffic light control via the TraCI interface.

SUMO, Simulation of Urban MObility; see http://sumo.dlr.de/
Copyright (C) 2009-2015 DLR/TS, Germany

This file is part of SUMO.
SUMO is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

import os
import sys
import optparse
import subprocess
import random

import traci
# the port used for communicating with your sumo instance
PORT = 8873


def generate_routefile():
    random.seed(42)  # make tests reproducible
    N = 3600  # number of time steps
    # demand per second from different directions
    pWE = 1. / 10
    pEW = 1. / 11
    pNS = 1. / 30
    with open("cruce1.rou.xml", "w") as routes:
        print >> routes, """<?xml version="1.0" encoding="UTF-8"?>
                <routes>
                <vType accel="3.0" decel="6.0" id="CarA" length="5.0" minGap="2.5" maxSpeed="30.0" sigma="0.5" />
                <vType accel="2.0" decel="6.0" id="Emerg" length="7.5" minGap="2.5" maxSpeed="30.0" sigma="0.5" />
  
                <route id="route01" edges="L12 L24"/>
                <route id="route02" edges="L12 L23"/>
                <route id="route03" edges="L32 L21"/>
                <route id="route04" edges="L32 L24"/>
                <route id="route05" edges="L42 L23"/>
                <route id="route06" edges="L42 L21"/>"""
        lastVeh = 0
        vehNr = 0
        for i in range(N):
            if random.uniform(0, 1) < pWE:
                print >> routes, '    <vehicle id="veh%i" type="CarA" route="route01" depart="%i" />' % (
                    vehNr, i)
                vehNr += 1
                lastVeh = i
            if random.uniform(0, 1) < pEW:
                print >> routes, '    <vehicle id="left_%i" type="typeWE" route="left" depart="%i" />' % (
                    vehNr, i)
                vehNr += 1
                lastVeh = i
            if random.uniform(0, 1) < pNS:
                print >> routes, '    <vehicle id="down_%i" type="typeNS" route="down" depart="%i" color="1,0,0"/>' % (
                    vehNr, i)
                vehNr += 1
                lastVeh = i
        print >> routes, "</routes>"


# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    # first, generate the route file for this simulation
    generate_routefile()
