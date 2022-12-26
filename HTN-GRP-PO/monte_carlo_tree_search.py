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

from sortedcontainers import SortedSet

from Simulator import *
from config import *


# vnode (observation node)
# vnode child action node (qnode)

STEP_DICT = {
    "wash_hand":["turn_on_faucet_1",
"use_soap",
"rinse_hand",
"turn_off_faucet_1",
"dry_hand"],
"make_tea":["turn_on_faucet_1",
"add_water_kettle_1",
"turn_off_faucet_1",
"switch_on_kettle_1",
"switch_off_kettle_1",
"get_cup_1",
"open_tea_box_1",
"add_tea_cup_1",
"close_tea_box_1",
"add_water_cup_1",
"drink"
],
"make_coffee":["turn_on_faucet_1",
"add_water_kettle_1",
"turn_off_faucet_1",
"switch_on_kettle_1",
"switch_off_kettle_1",
"get_cup_1",
"open_coffee_box_1",
"add_coffee_cup_1",
"close_tea_box_1",
"add_water_cup_1",
"drink"
]
}
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
        # self._expand(node)
        # agent_action_node = self._uct_select(node)
        #####
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._simulate(leaf)
        # self._backpropagate(path, reward)

    def _select(self, node):
        '''Find an unexplored descendent of `node` -
        find unexplored agent's move'''
        path = []
        # human_turn =  True
        while True:
            # node is always observation
            path.append(node)

            if not node.turn_information.action_node and node not in self.children or not self.children[
                    node]:
                # node is either unexplored or terminal
                return path

            # for action node
            if not node.turn_information.action_node:
                unexplored = self.children[node] - self.children.keys()
                if unexplored:
                    n = unexplored.pop()
                    path.append(n)
                    # return path
                # descend a layer deeper get action node
                node = self._uct_select(node)
            else:
                children = node.find_children()  # generate explasets
                inverse_pending_dict = defaultdict(list)
                current_explaset = node.explaset
                current_pending_set, inverse_pending_dict = current_explaset.pendingset_generate(
                    inverse_pending_dict)
                next_human_action = np.random.choice(
                    current_pending_set[:, 0], p=current_pending_set[:, 1].astype(float))

                next_sampled_explanation_index = np.random.choice(
                    inverse_pending_dict[next_human_action])
                if next_human_action == "add_water_cup_1":
                    print("here")

                # move to next agent state node with sampled_explanation
                node = children[next_sampled_explanation_index]
                node.pending_actions = SortedSet(
                    [action[0] for action in node.sampled_explanation._pendingSet])
                node.execute_sequences = [
                    taskNet._execute_sequence._sequence for taskNet in node.sampled_explanation._forest]
                flattened_execute_sequences = itertools.chain(
                    *node.execute_sequences)
                node.counter_execute_sequences = node.extract_execute_sequence(
                    flattened_execute_sequences)
                sensor_notification = copy.deepcopy(
                    realStateANDSensorUpdate(
                        next_human_action,
                        self.output_filename,
                        real_step=False))
                node.explaset.setSensorNotification(sensor_notification)
                node.explaset.action_posterior(
                    real_step=False, mcts_filename=self.output_filename)
            node.turn_information.action_node = not node.turn_information.action_node

    def _expand(self, node):
        "Update the `children` dict with the children of `node`"
        if node in self.children:
            return  # already expanded
        children = node.find_action_children()
        self.children[node] = children  # human_action: agent_action

    def _simulate(self, rootnode):
        '''args:
        rootnode: human_action node with agent action added as children
        Returns the reward for a random simulation (to completion) of `node`"
        "one simulation till the end'''
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
        previous_goal = None
        second_action = None
        num_goals = 0
        total_goals = np.random.choice(2) + 1
        while True:
            # chose agent action first
            if not node.turn_information.action_node:
                # select next action based on preference
                # if node in self.children:
                # children = self.children[node]
                # else:
                children = node.find_action_children()

                index = 0
                previous_node = node
                node = children[index]
                node.update_turn_information(previous_node)
                # node.turn_information = tmp_turn_information
                action = node.turn_information.chosen_action
                node = node.update_action(action, node)  # Todo: write better
            else:
                # then choose the human action with action response added to
                # it.
                children = node.find_observation_children()  # generate explasets
                if not children or step_num > self.depth or num_goals == total_goals:
                    return

                goal_complete = False
                single_goal_indices = []
                # if len(children) == 2:
                #     print("here")
                # len(children/ children[0].explaset._explaset) == 2 means
                # multiple goals
                for index, expla in enumerate(children[0].explaset._explaset):
                    if list(expla._start_task.values()).count(
                            0) == len(expla._start_task.keys()):
                        goal_complete = True
                    if list(expla._start_task.values()).count(1) == 1:
                        single_goal_indices.append(index)

                        # if all(expla._start_task.values == 0)
                inverse_pending_dict = defaultdict(list)
                current_explaset = children[0].explaset
                current_pending_set, inverse_pending_dict = current_explaset.pendingset_generate(
                    inverse_pending_dict, single_goal_indices, previous_goal, real_step=False)

                if not list(current_pending_set):
                    # print(node.children)
                    print("here")

                if goal_complete:
                    # start new goal
                    num_goals += 1
                    if previous_goal == "wash_hands":
                        # storing next action after turn_on_faucet
                        second_action = "add_water_kettle_1"

                    else:
                        second_action = "use_soap"
                    next_human_action = "turn_on_faucet_1"
                elif second_action:
                    next_human_action = second_action
                    second_action = None
                else:
                    # for next human action - either max, if goals 0 then start new goal by turn_on_faucet/add_kettle.
                    # first generate multiple goal correct step correctly. (based on end goal start new goal with turn_on_faucet)
                    # add low prob to repeat the previous use_soap/rinse.
                    # keep track of on and off turn_on_faucet-1, switch_on_kettle1, open_Tea_bnox1
                    # if len(current_explaset) > 1 :
                    # continue the previous goal
                    # if :
                    # multiple goal has started
                    # current_pending_set =

                    p = current_pending_set[:, 1].astype(float)
                    p /= p.sum()  # normalize
                    next_human_action = np.random.choice(
                        current_pending_set[:, 0], p=p)
                # TODO: maybe weighted sampled explanation
                if inverse_pending_dict == {}:
                    print("here")
                if next_human_action not in inverse_pending_dict.keys():
                    # new goal not supported by the current pending set.
                    return
                next_sampled_explanation_index = np.random.choice(
                    inverse_pending_dict[next_human_action])
                if next_human_action == "open_coffee_box_1":
                    print("here")

                # move to next agent state node with sampled_explanation
                for start_task, value in expla._start_task.items():
                    if value == 1:
                        previous_goal = start_task
                node = children[next_sampled_explanation_index]
                sensor_notification = copy.deepcopy(
                    realStateANDSensorUpdate(
                        next_human_action,
                        self.output_filename,
                        real_step=False))
                node.explaset.setSensorNotification(sensor_notification)

                # update the action posterior

                node.explaset.action_posterior(
                    real_step=False, mcts_filename=self.output_filename)
                # update the explaset and pending set to be used for next
                # iteration

                step_num += 1
                node.turn_information.step_index = step_num
            node.turn_information.action_node = not node.turn_information.action_node

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
