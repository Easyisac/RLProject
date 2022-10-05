import os
import sys
import random



def generate_routefile(N, name, dist, turndist):
    random.seed(42)  # make tests reproducible
    pRight, pUp, pLeft, pDown = dist
    # pRight = 1./2
    # pUp = 1./12
    # pLeft = 1./2
    # pDown = 1./12
    prouteRight, prouteUp, prouteLeft, prouteDown = turndist
    # prouteRight = [0., 1., 0.]
    # prouteUp = [0., 0., 1.]
    # prouteLeft = [1., 0., 0.]
    # prouteDown = [0., 1., 0.]
    routeRight = ['rightUp', 'rightLeft', 'rightDown']
    routeUp = ['upRight', 'upLeft', 'upDown']
    routeLeft = ['leftRight', 'leftUp', 'leftDown']
    routeDown = ['downRight', 'downUp', 'downLeft']

    with open("data/{}/{}.rou.xml".format(name, name), "w") as routes:
        print("""<routes>
                <vType id="type" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" \
        guiShape="passenger"/>
                
                <route id="rightUp" edges="1i 2o" />
                <route id="rightLeft" edges="1i 3o" />
                <route id="rightDown" edges="1i 4o" />
                <route id="upRight" edges="2i 1o" />
                <route id="upLeft" edges="2i 3o" />
                <route id="upDown" edges="2i 4o" />                
                <route id="leftRight" edges="3i 1o" />
                <route id="leftUp" edges="3i 2o" />
                <route id="leftDown" edges="3i 4o" />
                <route id="downRight" edges="4i 1o" />
                <route id="downUp" edges="4i 2o" />
                <route id="downLeft" edges="4i 3o" />""", file=routes)
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
    generate_routefile(500000)

