import os
import sys

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

from sumo_rl import SumoEnvironment
from agents import QLAgent
from sumo_rl.exploration import EpsilonGreedy


def run(use_gui=False, runs=100):
    out_csv = 'outputs/test/test'
    fixed_ts = False
    env = SumoEnvironment(net_file='data/cross.net.xml',
                          single_agent=False,
                          route_file='data/cross.rou.xml',
                          out_csv_name=out_csv,
                          use_gui=use_gui,
                          num_seconds=100000,
                          yellow_time=3,
                          min_green=5,
                          max_green=60,
                          fixed_ts=fixed_ts,
                          add_system_info=True)
    initial_state = env.reset()
    ql_agents = {ts: QLAgent(starting_state=env.encode(initial_state[ts], ts),
                             state_space=env.observation_space,
                             action_space=env.action_space,
                             alpha=0.1,
                             gamma=1,
                             exploration_strategy=EpsilonGreedy(initial_epsilon=0.05, min_epsilon=0.005, decay=1.0)) for ts in env.ts_ids}
    for eps in range(1, runs + 1):

        if run != 1:
            initial_states = env.reset()
            for ts in initial_states.keys():
                ql_agents[ts].state = env.encode(initial_states[ts], ts)

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
                    ql_agents[agent_id].learn(next_state=env.encode(s[agent_id], agent_id), reward=r[agent_id])
        env.save_csv(out_csv, eps)
        print('\n\n' + str(eps) +'\n\n')


if __name__ == '__main__':
    run()
