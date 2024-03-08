import array
from typing import List
from gymnasium import spaces
import gymnasium as gym
import numpy as np


class MyGymPointsEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
    max_size = 512
    
    def __init__(self, a : int = 10, b: int = 10):
        self.points : np.ndarray = np.zeros((512, 4), dtype=np.float32)
        self.observation_space = spaces.Dict(
            {
                "coords_x": spaces.Box(0, a, shape=(512,), dtype=np.float32),
                "coords_y": spaces.Box(0, b, shape=(512,), dtype=np.float32),
                "velocity": spaces.Box(0, max(a, b), shape=(512,), dtype=np.float32),
                "angle": spaces.Box(0, 360.0, shape=(512,), dtype=np.float32),
            }
        )
        self.action_space = spaces.Dict({
            "target": spaces.Discrete(self.max_size),
            "change_angle": spaces.Box(0, 360, shape=(1,), dtype=np.int32),
            "change_velocity": spaces.Box(-max(a, b), max(a, b), shape=(1,), dtype=np.float32),
        }) 
    
    def step(self, action):
        #observation, reward, terminated, False, info
        # Action 0 = move, 
        target = action["target"]
        change_angle = action["change_angle"]
        change_velocity = action["change_velocity"]
        new_angle = (int(self.points[target][3]) + int(change_angle)) % 360
        new_velocity = (self.points[target][2] + change_velocity)
        self.points[target][3] = new_angle
        self.points[target][2] = new_velocity
        # 
        self.points[target][0] = (self.points[target][0] + np.cos(new_angle * np.pi / 180.0) * new_velocity)
        self.points[target][1] = (self.points[target][1] + np.sin(new_angle * np.pi / 180.0) * new_velocity)
        return self._get_obs()
    
    def _get_obs(self):
        return {
            "coords_x": self.points[:, 0],
            "coords_y": self.points[:, 1],
            "velocity": self.points[:, 2],
            "angle":    self.points[:, 3],
        }
        
    def _get_info(self):
        return
        
    def _get_reward(self):
        return 
    
    def reset(self, seed = None, options = None):
        super().reset(seed=seed)
        self.points = np.zeros(self.points.shape, dtype=np.float32)
        observation = self._get_obs()
        info = self._get_info()
        
        return observation, info