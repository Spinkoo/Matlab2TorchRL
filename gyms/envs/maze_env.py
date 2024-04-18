import gym
from gym import spaces
import numpy as np
from Matlab2Py.mat_engine import Engine
import keyboard



class MazeMatlabEnv(gym.Env):
    metadata = {"render_modes": ["accelerator", "rapid-accelerator"]}

    def __init__(self, display_block : list ,render_mode=None, step_size=1, obs_dimension = 5):


        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.step_size = step_size

        self.display_blocks = display_block

        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(0, 1, shape=(2,), dtype=int),
                "target": spaces.Box(0, 1, shape=(2,), dtype=int),
            }
        )

        # We have 4 actions, corresponding to "left", "right", "forward", 
        self.action_space = spaces.Discrete(3)

        """
        The following dictionary maps abstract actions from `self.action_space` to 
        the direction we will walk in if that action is taken.
        I.e. 0 corresponds to "right", 1 to "up" etc.
        """
        self._action_to_direction = {
            0: np.array([ .0, .1]),
            1: np.array([ .0, -.1]),
            2: np.array([.1, .1]),
            #3: np.array([-.5, -.5]),
        }
        self.last_state = None
        self.obs_dim = obs_dimension

        self.reset_flags()
        self.reset_obj_params()
        self.termination_rewards = [-.5, 0 ,10]
        self.max_stucking_steps = 400


    def init_matlab_engine(self, model_path, simulation_path, model_name, simulation_type = 'sparsesbs', init_script = 'setup', max_iter = 20000):

        self.eng = Engine(model_path = model_path, sim_path = simulation_path, model_name = model_name, simulation_type=simulation_type)
        self.eng.load_engine()
        self.eng.run_engine_script(init_script)
        self.eng.set_simulation_mode(self.render_mode)
        self.eng.set_step_size(self.step_size)

        self.max_time = max_iter
        self.eng.set_max_steps(max_iter,)

    def extract_values(self):
        return { k : self.eng.get_runtime_attribute(k, '') for k in self.display_blocks}
    
    def _get_obs(self):
        return self.eng.get_robots_readings()[0]

    def _get_info(self):
        return {
            "distance": np.linalg.norm(
                self._agent_location - self._target_location, ord=1
            )
        }

    def calculate_reward(self, readings):
        t = self.extract_values()['time1']
        r = np.sum(readings) / (20 * 5)

        #favor no obstacles readings

        if r == 1:
            r = 5

        time_reward = (self.max_time - t) / self.max_time

        return (r + time_reward) / 2




    def reset_obj_params(self):
        self.last_x, self.last_y = -1, -1
        self.number_of_stops = 0

    def reset_flags(self):
        self.first_start = True
        self.is_moving = True

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random

        self.reset_flags()
        self.reset_obj_params()


        observation = np.zeros((self.obs_dim,))
        self.last_state = observation, 0, False
        return *self.last_state, 'stopped'

    def step(self, action):

        while True:
            sim_op = self.simulation_loop(action)
            status = sim_op[-1]
            if status == 'running':
                
                continue
            return sim_op

    def distance(self, x1, y1, x2, y2):
        return (x1 - x2) ** 2 + (y1 - y2) ** 2
    
    def has_moved(self, x, y, threshold = 2):
        return self.distance(x, y, self.last_x, self.last_y) > threshold


    def simulation_loop(self, action):
        action = int(action)
        vd, vg = self._action_to_direction[action]

        if not self.is_moving:
            self.eng.stop_simulation()

        status = self.eng.get_simulation_status()

        if not self.first_start:
            if status == 'stopped':
                # 0 is passing max iter threshold, 1 for hitting a wall and 2 for arriving succesfully 
                termination_reason = self.eng.get_simout()
                obs =  self._get_obs()
                return obs, self.termination_rewards[termination_reason], True, status
                


        if status == 'running' and self.eng.sim_type == 'sparsesbs':
            return self.last_state, 'running'
        
        
        self.eng.set_param('Vd', vd)
        self.eng.set_param('Vg', vg)
        
        

        if self.first_start:
            self.eng.start_pause_simulation()
            self.first_start = False 
            print('started')
            return self.last_state, 'running'
        
        current_x = self.eng.get_runtime_attribute('x','')
        current_y = self.eng.get_runtime_attribute('y','')

        if self.last_x != -1:

            if self.has_moved(current_x, current_y):
                self.number_of_stops = 0
                self.is_moving = True
            else:
                self.number_of_stops +=1
            
            #if the object is not moving stop the simulation
            if self.number_of_stops > self.max_stucking_steps:
                self.is_moving = False
        
        self.last_x = current_x
        self.last_y = current_y


        

        


        observation = self._get_obs()

        reward =  self.calculate_reward(observation)

        self.last_state = observation,reward, False
        self.eng.step_forward()
        
        return observation, reward, False, 'stepped'

    def render(self):
        pass



    def close(self):
        self.eng.end_simulation()


if __name__ == '__main__':

    SIMULATION_PATH = 'gyms/envs/maze/'
    MODEL_PATH = f"{SIMULATION_PATH}Simulation_2_Wall_Follower_v1.slx"
    model_name = 'Simulation_2_Wall_Follower_v1'
    env = MazeMatlabEnv(display_block=['time1'], render_mode='accelerator')
    env.init_matlab_engine(model_path = MODEL_PATH, simulation_path = SIMULATION_PATH, model_name = model_name, simulation_type='sparsesbs')

    env.reset()

    while True:

        action = env.action_space.sample()
        o, r , done, status = env.step(action)
        #print(action, r, done, status)
        if done:
            env.reset()
        if keyboard.is_pressed('q'):
            env.close()
            print('Existing simulation')
            exit()