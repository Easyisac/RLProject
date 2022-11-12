import os
import sys

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

from route_generator import generate_routefile
from sumo_rl import SumoEnvironment
from agents.dqn_agent import DQNAgent
from exploration.epsilon_greedy import EpsilonGreedy


def run(use_gui=True, runs=1, steps=100000):
    # pRight = 1./2
    # pUp = 1./12
    # pLeft = 1./2
    # pDown = 1./12
    # prouteRight = [0., 1., 0.]
    # prouteUp = [0., 0., 1.]
    # prouteLeft = [1., 0., 0.]
    # prouteDown = [0., 1., 0.]
    # dist = (1./2, 1./12, 1./2, 1./12)
    # turndist = ([0., 1., 0.], [0., 0., 1.], [1., 0., 0.], [0., 1., 0.])

    dist = (1./2, 1./12, 1./2, 1./12)
    turndist = ([0., 1., 0.], [0., 0., 1.], [1., 0., 0.], [0., 1., 0.])
    name = 'cross'
    out_csv = 'outputs/dqnlearn/dqna2'
    # dist = (1./2, 1./12, 1./2, 1./12)
    # turndist = ([1./3, 1./3, 1./3], [1./3, 1./3, 1./3], [1./3, 1./3, 1./3], [1./3, 1./3, 1./3])
    # name = 'cross2'
    # out_csv = 'outputs/dqnlearn/dqn4'
    generate_routefile(steps, name, dist, turndist)
    fixed_ts = False
    env = SumoEnvironment(net_file='data/{}/{}.net.xml'.format(name, name),
                          single_agent=False,
                          route_file='data/{}/{}.rou.xml'.format(name, name),
                          out_csv_name=out_csv,
                          use_gui=use_gui,
                          num_seconds=steps,
                          yellow_time=3,
                          min_green=5,
                          max_green=60,
                          fixed_ts=fixed_ts,
                          add_system_info=True)
    initial_state = env.reset()
    dqn_agents = {ts: DQNAgent(starting_state=initial_state[ts],
                             state_space=env.observation_space,
                             action_space=env.action_space,
                             learning_rate=0.01,
                             gamma=0.95,
                             exploration_strategy=EpsilonGreedy(initial_epsilon=0.05, min_epsilon=0.005, decay=1.0)) for ts in env.ts_ids}

    for eps in range(1, runs + 1):

        if eps != 1:
            initial_states = env.reset()
            for ts in initial_states.keys():
                dqn_agents[ts].state = initial_states[ts]

        info = []
        step = 0
        update = 0
        done = {'__all__': False}
        if fixed_ts:
            while not done['__all__']:
                _, _, done, _ = env.step(None)
        else:
            while not done['__all__']:
                actions = {ts: dqn_agents[ts].act() for ts in dqn_agents.keys()}
                s, r, done, info = env.step(action=actions)
                for agent_id in dqn_agents.keys():
                    dqn_agents[agent_id].memorize((actions[agent_id], r[agent_id], s[agent_id], done[agent_id]))
                update += 1
                if (update % 4 == 0):
                    for agent_id in dqn_agents.keys():
                        dqn_agents[agent_id].learn()

                for ts in s.keys():
                    dqn_agents[ts].state = s[ts]

                if update >= 100:
                    for agent_id in dqn_agents.keys():
                        dqn_agents[agent_id].target_model.set_weights(dqn_agents[agent_id].model.get_weights())
        env.save_csv(out_csv, eps)


if __name__ == '__main__':
    run(steps=100000)
