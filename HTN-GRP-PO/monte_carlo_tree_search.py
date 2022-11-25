"""
A minimal implementation of Monte Carlo tree search (MCTS) in Python 3
Luke Harold Miles, July 2019, Public Domain Dedication
See also https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
"""
from abc import ABC, abstractmethod
from collections import defaultdict
import math
import copy
import itertools
from pathlib import Path

from Simulator import *
from config import *


# vnode (observation node)
# vnode child action node (qnode)

class MCTS:
    "Monte Carlo tree searcher. First rollout the tree then choose a move."

    def __init__(
            self,
            output_folder,
            output_filename,
            sim_num=10,
            exploration_weight=1,
            db=None,
            trial=0):
        # self.Q = defaultdict(defaultdict)  # total reward of each node Q[statei][actioni] -> scaler
        # self.N = defaultdict(tuple)  # total visit count for each node N[state,action]
        # self.children = dict()  # children of each node childre[statei]->
        # [(statei+1,actioni)]
        # total reward of each node Q[statei][actioni] -> scaler
        self.Q = defaultdict(int)
        # total visit count for each node N[state,action]
        self.N = defaultdict(int)
        self.children = dict()
        self.exploration_weight = exploration_weight
        self.sim_num = sim_num
        self.db = db
        self.output_folder = output_folder
        self.output_filename = self.output_folder + "mcts_" + output_filename
        self.reward_filename = Path(
            self.output_folder +
            "mcts_Reward_" +
            output_filename).with_suffix('.csv')
        self.depth = 25
        self.trial = trial

    def choose(self, node):
        "Choose the best successor of node. (Choose a move in the game)"
        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            return node.find_random_child()

        def score(n):
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            return self.Q[n] / self.N[n]  # average reward

        return max(self.children[node], key=score)

    def rollout_loop(self, node, step):
        # node.pending_actions = set([action[0] for action in node.sampled_explanation._pendingSet])
        # node.execute_sequences = [taskNet._execute_sequence for taskNet in node.sampled_explanation._forest]
        # flattened_execute_sequences = itertools.chain(*node.execute_sequences)
        # node.counter_execute_sequences = node.extract_execute_sequence(flattened_execute_sequences)
        # # for i in range(monte_carlo_tree.sim_num):

        for i in range(1):
            root_node = copy.deepcopy(node)
            root_node.sample()

            pipeline = [{"$match": {}},
                        {"$out": "state"},
                        ]
            self.db._backup_state.aggregate(pipeline)

            pipeline = [{"$match": {}},
                        {"$out": "sensor"},
                        ]
            self.db._backup_sensor.aggregate(pipeline)

            with open(self.output_filename, 'a') as f:
                f.write("\n==========Trial #" + str(self.trial) +
                        " Rollout #" + str(i) + " , " + step + "==============\n")

            if config.RANDOM_BASELINE:
                with open("mcts_debugrandom_no.txt", 'a') as f:
                    f.write("\n==========Trial #" +
                            str(self.trial) +
                            " Rollout #" +
                            str(i) +
                            " , " +
                            step +
                            "==============\n")
            else:
                with open("mcts_random_no.txt", 'a') as f:
                    f.write("\n==========Trial #" +
                            str(self.trial) +
                            " Rollout #" +
                            str(i) +
                            " , " +
                            step +
                            "==============\n")
            self.do_rollout(root_node)

        # return monte_carlo_tree.choose(self)
        return None

    def do_rollout(self, node):
        "Make the tree one layer better. (Train for one iteration.)"
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._simulate(leaf)
        # self._backpropagate(path, reward)

    def _select(self, node):
        "Find an unexplored descendent of `node`"
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper

    def _expand(self, node):
        "Update the `children` dict with the children of `node`"
        if node in self.children:
            return  # already expanded
        children = node.find_children()
        self.children[node] = children  # state acction

    def _simulate(self, rootnode):
        "Returns the reward for a random simulation (to completion) of `node`"
        "one simulation till the end"
        node = copy.deepcopy(rootnode)
        # num_goals = 1
        # invert_reward = True
        # while True:
        #     if node.is_terminal():
        #         reward = node.reward()
        #         return 1 - reward if invert_reward else reward
        #     node = node.find_random_child()
        #     invert_reward = not invert_reward
        # https://www.geeksforgeeks.org/print-all-interleavings-of-given-two-strings/
        step_num = 0
        children = self.children[node]
        while children and step_num < self.depth:
            # if not node.successor_explanations:
            #     node.find_children()
            '''node.explaset._explaset = node.successor_explanations
            pending_set = node.explaset.pendingset_generate()'''
            inverse_pending_dict = defaultdict(list)
            current_explaset = children[0].explaset
            current_pending_set, inverse_pending_dict = current_explaset.pendingset_generate(
                inverse_pending_dict)

            if not list(current_pending_set):
                print(node.children)
                print("here")
            next_human_action = np.random.choice(
                current_pending_set[:, 0], p=current_pending_set[:, 1].astype(float))
            # TODO: maybe weighted sampled explanation
            next_sampled_explanation_index = np.random.choice(
                inverse_pending_dict[next_human_action])
            if next_human_action == "dry_hand":
                print("here")

            # move to next agent state node with sampled_explanation
            node = children[next_sampled_explanation_index]
            sensor_notification = copy.deepcopy(
                realStateANDSensorUpdate(
                    next_human_action,
                    self.output_filename,
                    real_step=False))
            node.explaset.setSensorNotification(sensor_notification)

            # update the action posterior

            node.explaset.action_posterior(real_step = False,  mcts_filename = self.output_filename)
            # update the explaset and pending set to be used for next iteration
            children = node.find_children()
            step_num += 1
            # TODO: keep track of goal change and 0,0,0
            # keep track of wrong step
            # some human action should be chosen from pending set

            # thisTree = copy.deepcopy(temp_forest.popleft())
            # tag = thisTree[0].get_node(thisTree[0].root).tag
            # parents = db.get_parent_list(tag)

    def _backpropagate(self, path, reward):
        "Send the reward back up to the ancestors of the leaf"
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward
            reward = 1 - reward  # 1 for me is 0 for my enemy, and vice versa

    def _uct_select(self, node):
        "Select a child of node, balancing exploration & exploitation"

        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            "Upper confidence bound for trees"
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=uct)

    def sample(belief_state):
        'explaset is belief state'


class MCNode(ABC):
    """
    A representation of a single board state.
    MCTS works by constructing a tree of these Nodes.
    Could be e.g. a chess or checkers board state.
    """

    @abstractmethod
    def find_children(self):
        "All possible successors of this board state"
        return set()

    @abstractmethod
    def find_random_child(self):
        "Random successor of this board state (for more efficient simulation)"
        return None

    @abstractmethod
    def is_terminal(self):
        "Returns True if the node has no children"
        return True

    @abstractmethod
    def reward(self):
        "Assumes `self` is terminal node. 1=win, 0=loss, .5=tie, etc"
        return 0

    @abstractmethod
    def __hash__(self):
        "Nodes must be hashable"
        return 123456789

    @abstractmethod
    def __eq__(node1, node2):
        "Nodes must be comparable"
        return True
