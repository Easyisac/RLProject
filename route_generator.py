import os
import sys
import random



def generate_routefile():
    random.seed(42)  # make tests reproducible
    N = 100000  # number of time steps
    pRight = 1./10
    pUp = 1./10
    pLeft = 1./10
    pDown = 1./10
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
        print(vehicleNumber)


if __name__ == "__main__":
    generate_routefile()

