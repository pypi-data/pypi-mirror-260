import itertools
import numpy as np
import gymnasium as gym

from gymnasium import spaces
from scipy import stats
from scipy.special import expit

class ToyPricing(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None, state_vals = 5, state_dim = 2, p = None):
        self.state_vals = state_vals
        self.actions = list(range(2))
        self.state_dim = state_dim
        self.state_range = state_vals**state_dim

        if p is None:
            if self.state_dim == 1:
                self.p = np.array([-0.3, 0.5], dtype = float)
            elif self.state_dim == 2:
                self.p = np.array([0.2, -0.3, 0.5], dtype = float)
            else:
                print("State dim not implemented yet.")

        self.window_size = 512  # The size of the PyGame window

        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        self.observation_space = spaces.Box(0, state_vals - 1, shape=(self.state_dim,), dtype=int)

        # We have 2 actions, corresponding "high", "low"
        self.action_space = spaces.Discrete(2)

    def _get_obs(self):
        return self._current_state
    
    def _get_info(self):
        return {"state": self._current_state}

    def _get_next_state(self, state, action):
        state = state / self.state_vals # Normalise state vector.
        s_a = np.concatenate((state.reshape(-1, self.state_dim), np.array([action]).reshape(-1, 1)), axis = 1)
        next_state_idx = stats.binom.rvs(self.state_range - 1, expit(s_a @ self.p))

        print(f"Sampling {next_state_idx=}")


        if self.state_dim == 1:
            return np.array(next_state_idx)
        elif self.state_dim == 2:
            next_state = np.array((int((next_state_idx - next_state_idx%self.state_vals) / self.state_vals), next_state_idx%self.state_vals))
            print(f"Next state {next_state=}")
            return next_state
        else:
            print("State dim not implemented yet.")

    def transition_pmf(self, state, action, next_state):
        state = state / self.state_vals # Normalise state vector.
        s_a = np.concatenate((state.reshape(-1, self.state_dim), np.array([action]).reshape(-1, 1)), axis = 1)

        if self.state_dim == 1:
            next_state_idx = next_state
        elif self.state_dim == 2:
            next_state_idx = next_state[:, 0] * self.state_vals + next_state[:, 1]
        else:
            print("State dim not implemented yet.")

        return np.array([stats.binom.pmf(next_state_idx, self.state_range - 1, expit(s_a @ self.p))], dtype = float)

    def init_pmf(self, state):
        return np.array([stats.binom.pmf(state, self.state_range, 0)], dtype = float)

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        # Always start at first state
        self._current_state = np.array([0 for i in range(self.state_dim)], dtype=int)

        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action):
        """will use TimeLimit wrapper for truncation..."""
        observation = self._get_obs()
        self._current_state = self._get_next_state(observation, action)

        # Reward
        reward = (np.sum(self._current_state.flatten() / self.state_vals).item() + action)**2

        next_observation = self._get_obs()
        info = self._get_info()
        terminated = False

        return next_observation, reward, terminated, False, info

    def render(self):
        pass

    def _render_frame(self):
        pass

    def close(self):
        pass