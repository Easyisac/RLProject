import os
import sys

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

from multi_route_generator import generate_routefile
from sumo_rl import SumoEnvironment
from agents.ql_agent import QLAgent
from exploration.epsilon_greedy import EpsilonGreedy


def run(use_gui=True, runs=1, steps=100000):
    name = 'multi_cross'
    generate_routefile(steps, name)
    bins = 10
    out_csv = 'outputs/qlearn/multi_ql'
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
    ql_agents = {ts: QLAgent(starting_state=env.encode(initial_state[ts], ts, bins),
                             state_space=env.observation_space,
                             action_space=env.action_space,
                             alpha=0.1,
                             gamma=0.95,
                             exploration_strategy=EpsilonGreedy(initial_epsilon=0.05, min_epsilon=0.005, decay=1.0)) for ts in env.ts_ids}

    for eps in range(1, runs + 1):

        if eps != 1:
            initial_states = env.reset()
            for ts in initial_states.keys():
                ql_agents[ts].state = env.encode(initial_states[ts], ts, bins)

        info = []

        done = {'__all__': False}
        if fixed_ts:
            while not done['__all__']:
                _, _, done, _ = env.step(None)
        else:
            while not done['__all__']:
                actions = {ts: ql_agents[ts].act() for ts in ql_agents.keys()}
                s, r, done, info = env.step(action=actions)
                for agent_id in ql_agents.keys():
                    ql_agents[agent_id].learn(next_state=env.encode(s[agent_id], agent_id, bins), reward=r[agent_id])

        env.save_csv(out_csv, eps)


if __name__ == '__main__':
    run(steps=100000)
