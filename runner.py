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
    pRight = 1./20
    pUp = 1./20
    pLeft = 1./20
    pDown = 1./20
    routeRight = ['rightUp', 'rightLeft', 'rightDown']
    prouteRight = [1./6, 2./3, 1./6]
    routeUp = ['upRight', 'upLeft', 'upDown']
    prouteUp = [1./6, 1./6, 2./3]
    routeLeft = ['leftRight', 'leftUp', 'leftDown']
    prouteLeft = [2./3, 1./6, 1./6]
    routeDown = ['downRight', 'downUp', 'downLeft']
    prouteDown = [1./6, 2./3, 1./6]

    with open("data/cross.rou.xml", "w") as routes:
        print("""<routes>
                <vType id="type" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" \
        guiShape="passenger"/>
                
                <route id="rightUp" edges="51i 1i 2o 52o" />
                <route id="rightLeft" edges="51i 1i 3o 53o" />
                <route id="rightDown" edges="51i 1i 4o 54o" />
                <route id="upRight" edges="52i 2i 1o 51o" />
                <route id="upLeft" edges="52i 2i 3o 53o" />
                <route id="upDown" edges="52i 2i 4o 54o" />                
                <route id="leftRight" edges="53i 3i 1o 51o" />
                <route id="leftUp" edges="53i 3i 2o 52o" />
                <route id="leftDown" edges="53i 3i 4o 54o" />
                <route id="downRight" edges="54i 4i 1o 51o" />
                <route id="downUp" edges="54i 4i 2o 52o" />
                <route id="downLeft" edges="54i 4i 3o 53o" />""", file=routes)
        vehicleNumber = 0

        for i in range(N):
            if random.uniform(0, 1) < pRight:
                print('    <vehicle id="v_%i" type="type" route="%s" depart="%i" />' % (
                    vehicleNumber, *random.choices(routeRight, prouteRight), i), file=routes)
                vehicleNumber += 1
            if random.uniform(0, 1) < pUp:
                print('    <vehicle id="v_%i" type="type" route="%s" depart="%i" />' % (
                    vehicleNumber, *random.choices(routeUp, prouteUp), i), file=routes)
                vehicleNumber += 1
            if random.uniform(0, 1) < pLeft:
                print('    <vehicle id="v_%i" type="type" route="%s" depart="%i" />' % (
                    vehicleNumber, *random.choices(routeLeft, prouteLeft), i), file=routes)
                vehicleNumber += 1
            if random.uniform(0, 1) < pDown:
                print('    <vehicle id="v_%i" type="type" route="%s" depart="%i" />' % (
                    vehicleNumber, *random.choices(routeDown, prouteDown), i), file=routes)
                vehicleNumber += 1
        print("</routes>", file=routes)
        global vehicles
        vehicles = vehicleNumber


def run():
    """execute the TraCI control loop"""
    step = 0
    delta = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        state = [
            traci.lanearea.getLastStepVehicleNumber("1"),
            traci.lanearea.getLastStepVehicleNumber("2"),
            traci.lanearea.getLastStepVehicleNumber("3"),
            traci.lanearea.getLastStepVehicleNumber("4"),
            traci.trafficlight.getPhase("0")
        ]
        action = agent.get_action(state, step, delta)
        if action:
            traci.trafficlight.setPhase("0", action)
            delta = -1
        step += 1
        delta += 1
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
