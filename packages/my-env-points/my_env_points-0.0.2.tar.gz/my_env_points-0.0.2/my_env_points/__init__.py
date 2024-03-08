from gymnasium.envs.registration import register

register(
     id="my_env_points/MyGymPoints",
     entry_point="my_env_points.envs:MyGymPointsEnv",
     max_episode_steps=300,
)