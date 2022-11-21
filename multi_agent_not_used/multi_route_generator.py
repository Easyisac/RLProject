import os
import sys
import random



def generate_routefile(N, name):
    random.seed(42)  # make tests reproducible

    traj = [['4-5', '4-6', '4-7', '4-8a', '4-8b', '4-9a', '4-9b', '4-10', '4-11', '4-4'],
            ['5-6', '5-7', '5-8a', '5-8b', '5-9a', '5-9b', '5-10', '5-11', '5-4', '5-5'],
            ['6-7', '6-8', '6-9', '6-10a', '6-10b', '6-11a', '6-11b', '6-4', '6-5', '6-6'],
            ['7-8', '7-9', '7-10a', '7-10b', '7-11a', '7-11b', '7-4', '7-5', '7-6', '7-7'],
            ['8-9', '8-10', '8-11', '8-4a', '8-4b', '8-5a', '8-5b', '8-6', '8-7', '8-8'],
            ['9-10', '9-11', '9-4a', '9-4b', '9-5a', '9-5b', '9-6', '9-7', '9-8', '9-9'],
            ['10-11', '10-4', '10-5', '10-6a', '10-6b', '10-7a', '10-7b', '10-8', '10-9', '10-10'],
            ['11-4', '11-5', '11-6a', '11-6b', '11-7a', '11-7b', '11-8', '11-9', '11-10', '11-11']]

    with open("data/{}/{}.rou.xml".format(name, name), "w") as routes:
        print("""<routes>
                <vType id="type" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" \
        guiShape="passenger"/>
                
                <route id="4-5" edges="4t0 0t5" />
                <route id="4-6" edges="4t0 0t1 1t6" />
                <route id="4-7" edges="4t0 0t1 1t7" />
                <route id="4-8a" edges="4t0 0t1 1t2 2t8" />
                <route id="4-8b" edges="4t0 0t3 3t2 2t8" />
                <route id="4-9a" edges="4t0 0t1 1t2 2t9" />
                <route id="4-9b" edges="4t0 0t3 3t2 2t9" />
                <route id="4-10" edges="4t0 0t3 3t10" />
                <route id="4-11" edges="4t0 0t3 3t11" />
                <route id="4-4" edges="4t0 0t1 1t2 2t3 3t0 0t4" />
                <route id="5-6" edges="5t0 0t1 1t6" />
                <route id="5-7" edges="5t0 0t1 1t7" />
                <route id="5-8a" edges="5t0 0t1 1t2 2t8" />
                <route id="5-8b" edges="5t0 0t3 3t2 2t8" />
                <route id="5-9a" edges="5t0 0t1 1t2 2t9" />
                <route id="5-9b" edges="5t0 0t3 3t2 2t9" />
                <route id="5-10" edges="5t0 0t3 3t10" />
                <route id="5-11" edges="5t0 0t3 3t11" />
                <route id="5-4" edges="5t0 0t4" />
                <route id="5-5" edges="5t0 0t1 1t2 2t3 3t0 0t5" />                
                <route id="6-7" edges="6t1 1t7" />
                <route id="6-8" edges="6t1 1t2 2t8" />
                <route id="6-9" edges="6t1 1t2 2t9" />
                <route id="6-10a" edges="6t1 1t2 2t3 3t10" />
                <route id="6-10b" edges="6t1 1t0 0t3 3t10" />
                <route id="6-11a" edges="6t1 1t2 2t3 3t11" />
                <route id="6-11b" edges="6t1 1t0 0t3 3t11" />
                <route id="6-4" edges="6t1 1t0 0t4" />
                <route id="6-5" edges="6t1 1t0 0t5" />
                <route id="6-6" edges="6t1 1t2 2t3 3t0 0t1 1t6" />     
                <route id="7-8" edges="7t1 1t2 2t8" />
                <route id="7-9" edges="7t1 1t2 2t9" />
                <route id="7-10a" edges="7t1 1t2 2t3 3t10" />
                <route id="7-10b" edges="7t1 1t0 0t3 3t10" />
                <route id="7-11a" edges="7t1 1t2 2t3 3t11" />
                <route id="7-11b" edges="7t1 1t0 0t3 3t11" />
                <route id="7-4" edges="7t1 1t0 0t4" />
                <route id="7-5" edges="7t1 1t0 0t5" />
                <route id="7-6" edges="7t1 1t6" />
                <route id="7-7" edges="7t1 1t2 2t3 3t0 0t1 1t7" />                
                <route id="8-9" edges="8t2 2t9" />
                <route id="8-10" edges="8t2 2t3 3t10" />
                <route id="8-11" edges="8t2 2t3 3t11" />
                <route id="8-4a" edges="8t2 2t3 3t0 0t4" />
                <route id="8-4b" edges="8t2 2t1 1t0 0t4" />
                <route id="8-5a" edges="8t2 2t3 3t0 0t5" />
                <route id="8-5b" edges="8t2 2t1 1t0 0t5" />
                <route id="8-6" edges="8t2 2t1 1t6" />
                <route id="8-7" edges="8t2 2t1 1t7" />
                <route id="8-8" edges="8t2 2t3 3t0 0t1 1t2 2t8" />                
                <route id="9-10" edges="9t2 2t3 3t10" />
                <route id="9-11" edges="9t2 2t3 3t11" />
                <route id="9-4a" edges="9t2 2t3 3t0 0t4" />
                <route id="9-4b" edges="9t2 2t1 1t0 0t4" />
                <route id="9-5a" edges="9t2 2t3 3t0 0t5" />
                <route id="9-5b" edges="9t2 2t1 1t0 0t5" />
                <route id="9-6" edges="9t2 2t1 1t6" />
                <route id="9-7" edges="9t2 2t1 1t7" />
                <route id="9-8" edges="9t2 2t8" />
                <route id="9-9" edges="9t2 2t3 3t0 0t1 1t2 2t9" />                
                <route id="10-11" edges="10t3 3t11" />
                <route id="10-4" edges="10t3 3t0 0t4" />
                <route id="10-5" edges="10t3 3t0 0t5" />
                <route id="10-6a" edges="10t3 3t0 0t1 1t6" />
                <route id="10-6b" edges="10t3 3t2 2t1 1t6" />
                <route id="10-7a" edges="10t3 3t0 0t1 1t7" />
                <route id="10-7b" edges="10t3 3t2 2t1 1t7" />
                <route id="10-8" edges="10t3 3t2 2t8" />
                <route id="10-9" edges="10t3 3t2 2t9" />
                <route id="10-10" edges="10t3 3t0 0t1 1t2 2t3 3t10" />                                
                <route id="11-4" edges="11t3 3t0 0t4" />
                <route id="11-5" edges="11t3 3t0 0t5" />
                <route id="11-6a" edges="11t3 3t0 0t1 1t6" />
                <route id="11-6b" edges="11t3 3t2 2t1 1t6" />
                <route id="11-7a" edges="11t3 3t0 0t1 1t7" />
                <route id="11-7b" edges="11t3 3t2 2t1 1t7" />
                <route id="11-8" edges="11t3 3t2 2t8" />
                <route id="11-9" edges="11t3 3t2 2t9" />
                <route id="11-10" edges="11t3 3t10" />
                <route id="11-11" edges="11t3 3t0 0t1 1t2 2t3 3t11" />""", file=routes)

        vehicleNumber = 0

        prob = 1./20

        for i in range(N):
            for j in range(8):
                if random.uniform(0, 1) < prob:
                    print('    <vehicle id="v_%i" type="type" route="%s" depart="%i" />' % (
                        vehicleNumber, *random.choices(traj[j]), i), file=routes)
                    vehicleNumber += 1

        print("</routes>", file=routes)
        print(vehicleNumber)


if __name__ == "__main__":
    generate_routefile(500000)

