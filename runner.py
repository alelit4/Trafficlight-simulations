#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random

import sumolib
import traci


def init():
    SUMO_HOME = os.environ.get('SUMO_HOME',
                           os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
    sys.path.append(os.path.join(SUMO_HOME, 'tools'))


def getFileDefinition():
    return """<routes>
        <vType id="westToEast" vClass="passenger" accel="1.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="50.67" \
guiShape="passenger"/>
        <vType id="eastToWest" vClass="passenger" accel="1.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="50.67" \
guiShape="passenger"/>
        <vType id="northToSouth" accel="1.8" decel="4.5" sigma="0.5" length="5" minGap="3" maxSpeed="60" 
        jmDriveAfterRedTime="10000" />

        <route id="right" edges="51o 1i 2o 52i" />
        <route id="left" edges="52o 2i 1o 51i" />
        <route id="down" edges="54o 4i 3o 53i" />"""

def routeFileGenerator():
    random.seed(42)  # make tests reproducible
    VehiclesGenerated = 1000 # number of generated vehicles
    # Probabilities for the creation of vehicles  
    probWestToEast = 1. / 10
    probEastToWest = 1. / 11
    probNorthToSouth = 1. / 10
    with open("data/cross.rou.xml", "w") as routes:
        print(getFileDefinition(), file=routes)
        vehicleNumber = 0
        for i in range(VehiclesGenerated):
            if random.uniform(0, 1) < probWestToEast:
                print('    <vehicle id="right_%i" type="westToEast" route="right" depart="%i" />' % (
                    vehicleNumber, i), file=routes)
                vehicleNumber += 1
            if random.uniform(0, 1) < probEastToWest:
                print('    <vehicle id="left_%i" type="eastToWest" route="left" depart="%i" />' % (
                    vehicleNumber, i), file=routes)
                vehicleNumber += 1
            if random.uniform(0, 1) < probNorthToSouth: #DEPRECATED 
                print('''    <vehicle id="down_%i" type="northToSouth" route="down" depart="%i"  color="1,0,0" >  
                                <param key="has.driverstate.device" value="true"/>
                            </vehicle>            ''' % (vehicleNumber, i), file=routes)
                vehicleNumber += 1
        print("</routes>", file=routes)

def run():
    """execute the TraCI control loop"""
    step = 0
    # we start with phase 2 where EW has green
    traci.trafficlight.setPhase("0", 2)
    while traci.simulation.getMinExpectedNumber() > 0:
        # print("-->" + str(traci.getIDList()))
        traci.simulationStep()
        step += 1
    traci.close()
    sys.stdout.flush()


def getOptions():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == "__main__":
    init()
    options = getOptions()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = sumolib.checkBinary('sumo')
    else:
        sumoBinary = sumolib.checkBinary('sumo-gui')
    # first, generate the route file for this simulation
    routeFileGenerator()

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    # Other options
    # "--tripinfo-output", "tripinfo.xml",
    # "--netstate-dump", "dumpeo.xml"
    # FULL Data options >> "--full-output", "fulldata.xml",
    # FCD options >>  "--fcd-output", "sumofcdoutput.xml", "--step-length", "0.025", "--device.fcd.period", "0.01"
    traci.start([sumoBinary, "-c", "data/cross.sumocfg",
                  "--fcd-output", "sumofcdoutput.xml", "--step-length", "0.01", "--device.fcd.period", "0.01" ])


    run()

