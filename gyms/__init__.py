from gym.envs.registration import register


register(
    id='MatlabMaze-v0',
    entry_point='gyms.envs:MazeMatlabEnv',
)