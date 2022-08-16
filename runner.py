from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
import agent
import pandas as pd


if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary
import traci

def generate_routefile():
    random.seed(42)  # make tests reproducible
    N = 3600  # number of time steps
    p = 1./3
    with open("data/cross.rou.xml", "w") as routes:
        print("""<routes>
                <vType id="type" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" \
        guiShape="passenger"/>
        
                <route id="ul" edges="54i 4i 1o 51o" />
                <route id="ud" edges="54i 4i 1o 51o" />
                <route id="ur" edges="54i 4i 3o 53o" />
                <route id="ru" edges="52i 2i 4o 54o" />
                <route id="rl" edges="52i 2i 1o 51o" />
                <route id="rd" edges="52i 2i 3o 53o" />
                <route id="dr" edges="53i 3i 2o 52o" />
                <route id="du" edges="53i 3i 4o 54o" />
                <route id="dl" edges="53i 3i 1o 51o" />
                <route id="ld" edges="51i 1i 3o 53o" />
                <route id="lr" edges="51i 1i 2o 52o" />
                <route id="lu" edges="51i 1i 4o 54o" />""", file=routes)
        vehicleNumber = 0
        route = ['ul', 'ud', 'ur', 'ru', 'rl', 'rd', 'dr', 'du', 'dl', 'ld', 'lr', 'lu']
        for i in range(N):
            if random.uniform(0, 1) < p:
                print('    <vehicle id="v_%i" type="type" route="%s" depart="%i" />' % (
                    vehicleNumber, route[random.randint(0,11)], i), file=routes)
                vehicleNumber += 1
        print("</routes>", file=routes)
        global vehicles
        vehicles = vehicleNumber


def run():
    """execute the TraCI control loop"""
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        state = [
            traci.lanearea.getLastStepVehicleNumber("1"),
            traci.lanearea.getLastStepVehicleNumber("2"),
            traci.lanearea.getLastStepVehicleNumber("3"),
            traci.lanearea.getLastStepVehicleNumber("4"),
            traci.trafficlight.getPhase("0")
        ]
        action = agent.get_action(state, step)
        if action:
            traci.trafficlight.setPhase("0", action)
        step += 1
    traci.close()
    sys.stdout.flush()
    get_total_waiting_time()

def get_total_waiting_time():
    info = pd.read_xml('tripinfo.xml')
    print(sum(info['waitingTime'].values))


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
    generate_routefile()

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "data/cross.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()
