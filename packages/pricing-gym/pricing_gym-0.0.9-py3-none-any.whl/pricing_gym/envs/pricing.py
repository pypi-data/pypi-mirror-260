import yaml
import numpy as np
import networkx as nx
import gymnasium as gym

# from gymnasium import spaces
from gymnasium import spaces
from scipy import stats
from scipy.special import expit

class NormalKernel:
    def __init__(self, dependencies = None):
        self.dependencies = dependencies

    def predict(self, observation):
        return np.array([stats.norm.rvs(0, 1)], dtype = float)

    def sample(self):
        return np.array([stats.norm.rvs(0, 1)], dtype = float)

class BinomialKernel:
    def __init__(self, dependencies, num_actions):
        self.dependencies = dependencies
        self.num_actions = num_actions

    def predict(self, observation):
        probs = self._get_p(observation)
        return stats.binom.rvs(n = self.num_actions - 1, p = probs)

    def _get_p(self, observation):
        prod = 0
        for lag in self.dependencies:
            for parent, value in self.dependencies[lag].items():
                prod += value["p"] * observation[parent]

        return expit(prod)

    def sample(self):
        return np.random.choice(self.num_actions)

class MixedPoissonKernel:
    def __init__(self, dependencies, capacity_stop):
        self.dependencies = dependencies
        self.capacity_stop = capacity_stop
        self.d0 = 540.0
        self.d0_low = 8
        self.p0 = 43.904
        self.beta_low = 0

    def predict(self, observation):
        # Normalise
        d = self._get_expected_demand(observation)
        p = self._get_prob_of_rejection(observation)

        lam = stats.gamma.rvs(a = p / (1 - p) * d, scale = (1 - p) / p)

        l = stats.poisson.rvs(lam)

        # TODO: This won't work if we let L_1 depend on itself!!
        if "L_1" in list(observation.keys()):
            l1 = observation["L_1"]
            if l1 + l > self.capacity_stop:
                return max(self.capacity_stop - 1 - l1, 0) #np.array([], dtype = int)

        return min(self.capacity_stop - 1, l)

    def _get_expected_demand(self, observation):
        prod = 0
        if stats.bernoulli.rvs(0.5):
            for lag in self.dependencies:
                for parent, params in self.dependencies[lag].items():
                    prod += params["d"] * observation[parent]

            d = self.d0 * np.exp(prod)
        else:
            d = self.d0_low

        return d

    def _get_prob_of_rejection(self, observation):
        prod = 0
        for lag in self.dependencies:
            for parent, params in self.dependencies[lag].items():
                prod += params["p"] * observation[parent]

        p = 1 / (1 + self.p0 * np.exp(prod))

        return p
    
    def sample(self):
        return np.random.choice(self.capacity_stop)


class Pricing(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, config_path):
        self.num_actions = 10
        self.capacity_stop = 150
        self.d0 = 270
        self.p0 = 122
        self.time_step = 0

        # Set config
        with open(config_path, 'r') as file:
            self.dag_specs = yaml.safe_load(file)

        # Spaces
        #   NB: We cannot control order of dict here. So when we set the variables, we will use nx to determine topological order. 
        self.observation_space = spaces.Dict(
            {
                "X": spaces.Box(-np.inf, np.inf, shape=(1,), dtype=float),
                "L_1": spaces.Discrete(self.capacity_stop),
                "A_1": spaces.Discrete(self.num_actions),
                "A_2": spaces.Discrete(self.num_actions),
            }
        )

        self.action_space = spaces.Dict(
            {
                "A_1": spaces.Discrete(self.num_actions)
            }
        )

        self.non_action_variables = self._get_non_action_variables()

        # Functional relationships        
        self.kernels = {}
        for var_name in self.dag_specs.keys():
            self.kernels[var_name] = self._get_kernel(self.dag_specs[var_name])
    
    def _get_kernel(self, params):
        if params["type"] == "exogenous":
            return NormalKernel(params["dependencies"])            
        elif params["type"] == "price":
            return BinomialKernel(params["dependencies"], self.num_actions)
        elif params["type"] == "bookings":
            return MixedPoissonKernel(params["dependencies"], self.capacity_stop)

    def _get_non_action_variables(self):
        return [i for i in self.dag_specs.keys() if i not in list(self.action_space.keys())]

    def _extend_graph(self):
        for var_name in self.topological_order:
            node_name = f"{var_name}_{self.time_step + 1}"
            self._add_variable(var_name, self.time_step + 1)
            self.G.add_edges_from([(parent_node, node_name) for parent_node in self._get_parent_nodes(var_name, self.time_step + 1)])

    def get_parent_values(self, child_node: str):
        var_name = self.G.nodes[child_node]["var_name"]
        if self.dag_specs[var_name]["dependencies"] is None:
            return np.array([])

        # Make dict with vals
        parent_values = {}
        for graph_parent in self.G.predecessors(child_node):
            parent_var_name = self.G.nodes[graph_parent]["var_name"]
            parent_values[parent_var_name] = self.G.nodes[graph_parent]["value"]

        return parent_values

    def _add_variable(self, var_name, time_step):
        node_name = var_name + f"_{time_step}"
        node_offset = self.dag_specs[var_name]["level_offset"]

        self.G.add_node(node_name, level = time_step + node_offset, var_name = var_name, time = time_step)

    def _get_parent_nodes(self, var_name, time_step):
        if self.dag_specs[var_name]["dependencies"] is None:
            return []

        parent_nodes = []
        for lag in self.dag_specs[var_name]["dependencies"].keys():
            for parent_var_name in self.dag_specs[var_name]["dependencies"][lag].keys():
                t_append = time_step - int(lag)
                parent_name = parent_var_name + f"_{str(t_append)}"
                if parent_name in self.G.nodes:
                    parent_nodes.append(parent_name)

        return parent_nodes

    def _current_observation(self):
        observation = {}
        for var_name in self.observation_space.keys():
            if var_name in list(self.action_space.keys()):
                node_name = f"{var_name}_{self.time_step - 1}"
            else:
                node_name = f"{var_name}_{self.time_step}"

            observation[var_name] = self.G.nodes[node_name]["value"]

        return observation

    def _get_reward(self):
        return \
            float(self.G.nodes[f"A_2_{self.time_step - 1}"]["value"] * self.G.nodes[f"L_2_{self.time_step}"]["value"] + \
                  self.G.nodes[f"A_1_{self.time_step - 1}"]["value"] * self.G.nodes[f"L_1_{self.time_step}"]["value"])

    def _set_action_values(self, action):
        # - Action Variables
        for var_name, value in zip(list(self.action_space.keys()), [action]):
            node_name = f"{var_name}_{self.time_step}"
            self.G.nodes[node_name]['value'] = value

    def _set_non_action_values(self):
        # 2. Set values
        for var_name in self.non_action_variables:
            node_name = f"{var_name}_{self.time_step + 1}"
            parent_values = self.get_parent_values(node_name)
            self.G.nodes[node_name]['value'] = self.kernels[var_name].predict(parent_values)

    def step(self, action):
        """will use TimeLimit wrapper for truncation..."""
        # Set action node value at current time-step
        self._set_action_values(action)

        # Extend Graph (build all next time-step variables)
        self._extend_graph()

        # Set non-action node values at next time-step
        self._set_non_action_values()

        # Move one time-step
        self.time_step += 1

        reward = self._get_reward()

        next_observation = self._current_observation()

        info = self._get_info()

        # Clean-up graph (remove all non-dependencies)
        self._clean_up_graph()

        return next_observation, reward, False, False, info

    def _clean_up_graph(self):
        relevant_nodes = []
        # Add current variables and dependencies
        for var_name in self.non_action_variables + list(self.action_space.keys()):
            node_name = f"{var_name}_{self.time_step}"
            relevant_nodes.append(node_name)
            relevant_nodes.append(self.G.predecessors(node_name))
        
        redundant_nodes = []
        for node_name in self.G.nodes:
            if node_name not in relevant_nodes:
                redundant_nodes.append(node_name)
        
        for node_name in redundant_nodes:
            self.G.remove_node(node_name)

    def _get_info(self):
        return {
            "observation": self._current_observation(),
            "time_step": self.time_step}

    def _init_graph(self):
        # Init values
        for time_step in range(2):
            for var_name in self.non_action_variables + list(self.action_space.keys()):
                node_name = f"{var_name}_{time_step}"
                self._add_variable(var_name, time_step)
                self.G.nodes[node_name]["value"] = self.kernels[var_name].sample()

        # Init edges
        for time_step in range(2):
            for var_name in self.non_action_variables + list(self.action_space.keys()):
                node_name = f"{var_name}_{time_step}"            
                self.G.add_edges_from([(parent_node, node_name) for parent_node in self._get_parent_nodes(var_name, 0)])

        self.time_step = 1

    def _get_topological_order(self):
        topological_order = [i.split("_")[0] + "_" + i.split("_")[1] for i in list(nx.topological_sort(self.G)) if i.split("_")[-1] == "1"]
        for i, var in enumerate(topological_order):
            if var[0] == "X":
                topological_order[i] = "X"

        return topological_order

    def reset(self, options=None, seed=None):
        # We need the following line to seed self.np_random
        super().reset()

        self.G = nx.DiGraph()

        # Set init values
        self._init_graph()

        # Set topological order among variables
        self.topological_order = self._get_topological_order()

        observation = self._current_observation()

        info = self._get_info()

        return observation, info

    def render(self):
        pass

    def _render_frame(self):
        pass

    def close(self):
        pass