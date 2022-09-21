import gym
from stable_baselines3.dqn.dqn import DQN
import os
import sys
from route_generator import generate_routefile
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")
from sumo_rl import SumoEnvironment
import traci


if __name__ == '__main__':
    steps = 100000
    generate_routefile(steps)
    env = SumoEnvironment(net_file='data/cross.net.xml',
                          route_file='data/cross.rou.xml',
                          out_csv_name='outputs/dqnlib/dqn',
                          single_agent=True,
                          use_gui=True,
                          num_seconds=steps)

    model = DQN(
        env=env,
        policy="MlpPolicy",
        learning_rate=0.001,
        learning_starts=0,
        train_freq=1,
        target_update_interval=500,
        exploration_initial_eps=0.05,
        exploration_final_eps=0.01,
        verbose=1
    )
    model.learn(total_timesteps=steps)