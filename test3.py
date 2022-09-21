import os
import sys
from datetime import datetime

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

from route_generator import generate_routefile
from sumo_rl import SumoEnvironment
from agents.sarsaANN_agent import SarsaANNagent
from exploration.epsilon_greedy import EpsilonGreedy


def run(use_gui=True, runs=1, steps=100000):
    generate_routefile(steps)
    bins = 10
    out_csv = 'outputs/sarsaANN/sarsaANN'
    fixed_ts = False
    env = SumoEnvironment(net_file='data/cross.net.xml',
                          single_agent=False,
                          route_file='data/cross.rou.xml',
                          out_csv_name=out_csv,
                          use_gui=use_gui,
                          num_seconds=steps,
                          yellow_time=3,
                          min_green=5,
                          max_green=60,
                          fixed_ts=fixed_ts,
                          add_system_info=True)

    initial_state = env.reset()
    sarsa_agents = {ts: SarsaANNagent(starting_state=initial_state[ts],
                                      state_space=env.observation_space,
                                      action_space=env.action_space,
                                      gamma=0.95,
                                      learning_rate=0.01,
                                      exploration_strategy=EpsilonGreedy(initial_epsilon=0.05, min_epsilon=0.005,
                                                                         decay=1.0)) for ts in env.ts_ids}

    for eps in range(1, runs + 1):

        if eps != 1:
            initial_states = env.reset()
            for ts in initial_states.keys():
                sarsa_agents[ts].state = initial_states[ts]

        info = []

        done = {'__all__': False}
        if fixed_ts:
            while not done['__all__']:
                _, _, done, _ = env.step(None)
        else:
            actions = {ts: sarsa_agents[ts].first_act() for ts in sarsa_agents.keys()}
            while not done['__all__']:
                s, r, done, info = env.step(action=actions)
                actions = {ts: sarsa_agents[ts].act() for ts in sarsa_agents.keys()}
                for agent_id in sarsa_agents.keys():
                    sarsa_agents[agent_id].learn(new_state=s[agent_id], reward=r[agent_id])

        env.save_csv(out_csv, eps)


if __name__ == '__main__':
    run(steps=100000)
