import keyboard
from DQN import *
import gym

from gyms.envs.maze_env import MazeMatlabEnv

SIMULATION_PATH = 'gyms/envs/maze/'
MODEL_PATH = f"{SIMULATION_PATH}Simulation_2_Wall_Follower_v1.slx"
model_name = 'Simulation_2_Wall_Follower_v1'
# Make a new continuous cartpole

def init_env():
    env = gym.make('MatlabMaze-v0', display_block=['time1'], render_mode='accelerator')
    return env

env = init_env()
env.init_matlab_engine(model_path = MODEL_PATH, simulation_path = SIMULATION_PATH, model_name = model_name, simulation_type='sparsesbs')

env.reset()



def main():
    
    print("The DQN is collecting experience...")
    
    
    env = init_env()
    env.init_matlab_engine(model_path = MODEL_PATH, simulation_path = SIMULATION_PATH, model_name = model_name, simulation_type='sparsesbs')
    net = Dqn(n_states=env.obs_dim)
    history = []
    for episode in range(EPISODES):
        state, _, _, _ = env.reset()
        step_counter_list = []
        step_counter = 0
        while True:
            
            step_counter +=1
            
            
            action = net.choose_action(state, env)
            
            next_state, reward, done, _ = env.step(action)
            

            net.store_trans(state, action, reward, next_state)  

            if net.memory_counter >= MEMORY_CAPACITY:
                net.learn()
                if done:
                    print(f"episode {episode}, the reward is {round(reward, 3)}")
            step_counter_list.append(reward)
            if done:
                history.append(np.mean(step_counter_list))

                
                net.plot(net.ax, history)
                break
            
            if keyboard.is_pressed('q'):
                env.close()
                print('Existing simulation')
                exit()
            state = next_state

if __name__ == '__main__':
    main()