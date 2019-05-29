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


# To have bad behavoiur -> jmDriveAfterRedTime="10000"
def getfileDefinition(filename, jmDriveAfterRedTime = 0):
    print( """<routes>
        <vType id="westToEast" vClass="passenger" accel="1.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="50.67" \
guiShape="passenger"/>
        <vType id="eastToWest" vClass="passenger" accel="1.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="50.67" \
guiShape="passenger"/>
        <vType id="northToSouth" accel="1.8" decel="4.5" sigma="0.5" length="5" minGap="3" maxSpeed="60" jmDriveAfterRedTime="%d"
         />

        <route id="right" edges="51o 1i 2o 52i" />
        <route id="left" edges="52o 2i 1o 51i" />
        <route id="down" edges="54o 4i 3o 53i" />""" % jmDriveAfterRedTime, file=filename )

def routeGeneratorBadBehaviour( vehiclesGenerated = 100):
    # Probabilities for the creation of vehicles
    probWestToEast = 1. / 7
    probEastToWest = 1. / 7
    probNorthToSouth = 1. / 11
    with open("data/cross.rou.xml", "w") as routes:
        getfileDefinition(routes, 100000000)
        vehicleNumber = 0
        for i in range(vehiclesGenerated):
            if random.uniform(0, 1) < probWestToEast:
                print('    <vehicle id="right_%i" type="westToEast" route="right" depart="%i" />' % (
                    vehicleNumber, i), file=routes)
                vehicleNumber += 1
            if random.uniform(0, 1) < probEastToWest:
                print('    <vehicle id="left_%i" type="eastToWest" route="left" depart="%i" />' % (
                    vehicleNumber, i), file=routes)
                vehicleNumber += 1
            if random.uniform(0, 1) < probNorthToSouth:
                print('''    <vehicle id="down_%i" type="northToSouth" route="down" depart="%i"  color="1,0,0" >  
                                 key="has.driverstate.device" value="true"/>
                            </vehicle>            ''' % (vehicleNumber, i), file=routes)
                vehicleNumber += 1
        print("</routes>", file=routes)

def routeGeneratorGoodBehaviour( vehiclesGenerated = 100):
    with open("data/cross.rou.xml", "w") as routes:
        getfileDefinition(routes)
        vehicleNumber = 0
        for i in range(vehiclesGenerated):
             print('''    <vehicle id="down_%i" type="northToSouth" route="down" depart="%i"  color="1,0,0" >  
                                <param key="has.driverstate.device" value="true"/>
                            </vehicle>            ''' % (vehicleNumber, i), file=routes)
             vehicleNumber += 1
        print("</routes>", file=routes)

# Bad behaviour is based on FCD options
# "--tripinfo-output", "tripinfo.xml",
# "--netstate-dump", "simulations/dumpeo.xml"
def badBehaviourSimulation(sumoBinary, iteration):
    vehiclesGenerated = 10000
    routeGeneratorBadBehaviour(vehiclesGenerated)
    traci.start([sumoBinary, "-c", "data/crossbad.sumocfg",
                  "--fcd-output", "simulations/sumofcdoutput1000_%s.xml" % iteration, "--step-length", "0.025", "--device.fcd.period", "0.01" ])
    run()

# Good behaviour is based on  FULL Data options
def goodBehaviourSimulation(sumoBinary, iteration):
    vehiclesGenerated = 1000
    routeGeneratorGoodBehaviour(vehiclesGenerated)
    traci.start([sumoBinary, "-c", "data/cross.sumocfg",
                  "--full-output", "simulations/fulldata1000_%s.xml"% iteration,  "--max-num-vehicles", "1" ])
    run()

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

# this script has been called from the command line. It will start sumo as a
# server, then connect and run
def getOptions():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    if options.nogui:
        return sumolib.checkBinary('sumo')
    else:
        return sumolib.checkBinary('sumo-gui')

# this is the main entry point of this script
if __name__ == "__main__":
    init()
    sumoBinary = getOptions()
    for i in range(1, 11):
        random.seed(i*42)  # 42 make tests reproducible
        badBehaviourSimulation(sumoBinary, i)
        goodBehaviourSimulation(sumoBinary, i)
