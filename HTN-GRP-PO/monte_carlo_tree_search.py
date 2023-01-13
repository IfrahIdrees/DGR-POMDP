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
    1: ["turn_on_faucet_1",
        "use_soap",
        "rinse_hand",
        "turn_off_faucet_1",
        "dry_hand"],

    2: ["turn_on_faucet_1",
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

    3: ["turn_on_faucet_1",
        "add_water_kettle_1",
        "turn_off_faucet_1",
        "switch_on_kettle_1",
        "switch_off_kettle_1",
        "get_cup_1",
        "open_coffee_box_1",
        "add_coffee_cup_1",
        "close_coffee_box_1",
        "add_water_cup_1",
        "drink"
        ]
}

INVERSE_STEP_DICT = {
    "turn_on_faucet_1": [1, 2, 3],
    "use_soap": [1],
    "rinse_hand": [1],
    "turn_off_faucet_1": [1],
    "dry_hand": [9],
    "open_tea_box_1": [2],
    "add_tea_cup_1": [2],
    "close_tea_box_1": [2],
    "add_water_cup_1": [-1],
    "drink": [9],
    "add_water_kettle_1": [-1],
    "turn_off_faucet_1": [-1],
    "switch_on_kettle_1": [-1],
    "switch_off_kettle_1": [-1],
    "get_cup_1": [-1],
    "open_coffee_box_1": [3],
    "add_coffee_cup_1": [3],
    "close_coffee_box_1": [3]
}

GOAL = {
    1: "wash_hand",
    2: "make_tea",
    3: "make_coffee"
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
        self.gamma = 0.95

    def choose(self, node):
        "Choose the best successor of node. (Choose a move in the game)"
        # if node.is_terminal():
        # raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            print("here")
            # return node.find_random_child()

        def score(n):
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            return self.Q[n] / self.N[n]  # average reward

        action_node = max(self.children[node], key=score)
        print("\n=========All node Reward==========")
        for n in self.children[node]:
            print(
                "Node:",
                n.turn_information.chosen_action.name,
                "Reward",
                score(n))
            # "Reward": score(n))
        # print("self.children[")
        return action_node, score(action_node)

    def rollout_loop(self, node, step):
        # node.pending_actions = set([action[0] for action in node.sampled_explanation._pendingSet])
        # node.execute_sequences = [taskNet._execute_sequence for taskNet in node.sampled_explanation._forest]
        # flattened_execute_sequences = itertools.chain(*node.execute_sequences)
        # node.counter_execute_sequences = node.extract_execute_sequence(flattened_execute_sequences)
        # # for i in range(monte_carlo_tree.sim_num):

        for i in range(5):
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
            # self._expand(root_node) ##Todo: trying what Jason does expands
            # the root
            print("\n\n ROLL OUT # ", i)
            if i == 2:
                print("here")
            self.do_rollout(root_node)

        # TODO: check, jason does uct for choose as well
        return self.choose(root_node)
        # return None

    def do_rollout(self, node):
        "Make the tree one layer better. (Train for one iteration.)"
        # self._expand(node)
        # agent_action_node = self._uct_select(node)
        #####
        path, step_rewards, is_haction_in_belief, num_goals, is_goal_chosen = self._select(
            node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._simulate(
            leaf,
            is_haction_in_belief,
            num_goals,
            is_goal_chosen)
        self._backpropagate(path, reward, step_rewards)

    def _select(self, node):
        '''Find an unexplored descendent of `node` -
        find unexplored agent's move'''
        path = []
        step_rewards = []  # o,a,o,a
        is_haction_in_belief = True
        num_goals = 0
        is_goal_chosen = False
        # human_turn =  True
        while True:
            # entering node is always observation
            path.append(node)
            step_rewards.append(0)

            if node in self.children and not self.children[node]:
                print("here")
            if (not node.turn_information.action_node and node not in self.children):
                # or not self.children[
                # node]:
                # exiting node is always observation
                # node is either unexplored or terminal
                # step_rewards.append(0)
                return path, step_rewards, is_haction_in_belief, num_goals, is_goal_chosen

            if not node.turn_information.action_node:
                # handling vnode (observation node) and selecting action
                # children for it
                # return only when observation node
                '''we don't need to check if the node is
                expanded or not inside if condition. This
                is checked before the if condition. When reach if condition
                unexplored_action = self.children[node] - self.children.keys()
                if unexplored_action:
                    # continue
                    ## if unexplored so return the existing path, step rewards
                    ## and expand the existing path
                    # n = unexplored_action.pop()
                    # path.append(n)
                    return path, step_rewards'''

                # descend a layer deeper and get action node
                previous_node = node
                node = self._uct_select(node)  # UCT checked and verified

                # add step reward for asking questions

                node.update_turn_information(previous_node)
                action = node.turn_information.chosen_action
                node = node.update_action(action, node)  # Todo: write better
                step_reward = self.get_step_reward(
                    is_haction_in_belief, action)
                # figure out is_haction_in_belief passed here
                step_rewards.append(step_reward)
                is_haction_in_belief = True  # reset is_haction_in_belief for the next step

            else:

                # if node.explaset:
                #     children = self.children[node]
                # else:
                # children = []
                # while not children:
                children = node.find_observation_children()  # generate explasets
                # see children is in the self.children then just to dict access
                # add children and node in dict
                if children == []:
                    return path, step_rewards, is_haction_in_belief, num_goals, is_goal_chosen
                inverse_pending_dict = defaultdict(list)
                current_explaset = children[0].explaset
                inverse_pending_dict, current_pending_set = current_explaset.pendingset_generate()
                step_index, next_human_action, next_goal, num_goals, is_goal_chosen = self.get_turn_information(
                    children, num_goals, select=True, is_goal_chosen=is_goal_chosen)
                # step_index
                # next_human_action = np.random.choice(
                # current_pending_set[:, 0], p=current_pending_set[:,
                # 1].astype(float))

                '''p = current_pending_set[:, 1].astype(float)
                p /= p.sum()  # normalize
                next_human_action = np.random.choice(
                    current_pending_set[:, 0], p=p)'''
                if not next_human_action in inverse_pending_dict:
                    sensor_notification, is_haction_in_belief = self.execute_wrong_step_or_belief(
                        next_human_action)
                    node.explaset.setSensorNotification(sensor_notification)
                else:
                    next_sampled_explanation_index = np.random.choice(
                        inverse_pending_dict[next_human_action])
                    # move to next agent state node with sampled_explanation

                    node = children[next_sampled_explanation_index]
                    sensor_notification = copy.deepcopy(
                        realStateANDSensorUpdate(
                            next_human_action,
                            self.output_filename,
                            real_step=False))
                    node.explaset.setSensorNotification(sensor_notification)

                if next_human_action == "dry_hand":
                    print("here")

                node.pending_actions = SortedSet(
                    [action[0] for action in node.sampled_explanation._pendingSet])
                node.execute_sequences = [
                    taskNet._execute_sequence._sequence for taskNet in node.sampled_explanation._forest]
                flattened_execute_sequences = itertools.chain(
                    *node.execute_sequences)
                node.counter_execute_sequences = node.extract_execute_sequence(
                    flattened_execute_sequences)

                node.turn_information.update_turn_information(
                    step_index, next_human_action, next_goal)  # Todo: get the correct goal when turn_on comes again then
                # two tasknets start
                node.explaset.action_posterior(
                    real_step=False, mcts_filename=self.output_filename)

            node.turn_information.action_node = not node.turn_information.action_node

    def _expand(self, node):
        "Update the `children` dict with the children of `node`"
        if node in self.children:
            return  # already expanded
        children = node.find_action_children()
        self.children[node] = children  # human_action: agent_action
        self.N[node] = 0
        for action in children:
            self.N[action] = 0
            self.Q[action] = 0

    def get_step_reward(self, is_haction_in_belief, action):
        if not is_haction_in_belief and action.name == "ask-clarification-question":
            return 5
        elif not is_haction_in_belief and action.name == "wait":
            return -5
        elif is_haction_in_belief and action.name == "ask-clarification-question":
            return -5
        else:
            return 0

    # def get_turn_information_select(self,children, is_goal_chosen, num_goals=0, previous_goal=0, ):
    #     current_explaset = children[0].explaset
    #     inverse_pending_dict, current_pending_set = current_explaset.pendingset_generate()
    #     previous_goal, current_goal = children[0].turn_information._goal
    #     step_index = children[0].turn_information._step_information[0]

    #     p = current_pending_set[:, 1].astype(float)
    #     p /= p.sum()  # normalize
    #     next_human_action = np.random.choice(
    #         current_pending_set[:, 0], p=p)
    #     # current_explaset._explaset
    #     # INVERSE_STEP_DICT[next_human_action]
    #     if current_goal  == 0 and next_human_action =="use_soap":
    #         next_goal = 1
    #     elif current_goal  == 0 and next_human_action =="add_water_kettle_1":
    #         next_goal = 2
    #     elif next_human_action in ["dry_hand", "drink"]:
    #         next_goal = INVERSE_STEP_DICT[next_human_action]
    #     elif current_goal == -1 and not is_goal_chosen:

    #         # next_goal =
    #         current_goal = INVERSE_STEP_DICT[next_human_action]
    #         if
    #         ## new goal will be use_soap/add_Wayer
    #     return is_goal_chosen

    def get_turn_information(self, children, num_goals=0,
                             select=True, is_goal_chosen=False):
        if select:
            child = children[0]
            current_explaset = child.explaset
            start_task_dict = child.sampled_explanation._start_task
            inverse_pending_dict, current_pending_set = current_explaset.pendingset_generate()
        previous_goal, current_goal = children[0].turn_information._goal
        step_index = children[0].turn_information._step_information[0]

        next_human_action = None
        if select:
            p = current_pending_set[:, 1].astype(float)
            p /= p.sum()  # normalize
            next_human_action = np.random.choice(
                current_pending_set[:, 0], p=p)

        if current_goal == 0:
            # this is the first step choose any of the
            # second steps
            if not select:
                next_human_action = np.random.choice(
                    ["use_soap", "add_water_kettle_1"], p=[0.33, 1 - 0.33])
            if next_human_action == "use_soap":  # restricted when multiple goals
                # if next_human_action in STEP_DICT[1]:
                next_goal = 1
            else:
                next_goal = 2
                # TODO: need to make next goal random
                # next_goal = np.random.choice([2,3])
                # next_goal = -1
            # step_index+=1 #[Done]TODO:(not increment the previous stepindex that continues the numbering
            # rather reset it)
            step_index = 1  # not restrict to 1
        elif current_goal == 9:
            next_human_action = "turn_on_faucet_1"
            next_goal = 0
            step_index = 0
            num_goals += 1
        else:
            # select the next human action for
            # the current ongoing goal
            # if current_goal == -1:
            # current_goal =previous_goal #np.random.choice([2,3])
            if current_goal == -1 and not is_goal_chosen:
                if select:
                    # fix this
                    current_goal = 2 if start_task_dict[GOAL[2]] == 1 else 3
                    # goal should be matching the next_human_Action
                    # if start_task_dict[GOAL[2]]==1 and next_human_action in STEP_DICT[2]:
                    #     current_goal=2
                    # elif start_task_dict[GOAL[3]]==1 and next_human_action in STEP_DICT[3]:
                    #     current_goal=3
                else:
                    current_goal = np.random.choice([2, 3])
                is_goal_chosen = True
            elif current_goal == -1:
                current_goal = previous_goal
            # if select:

            next_goal = current_goal

            previous_next_human_action = next_human_action
            # if not select: ## added just now
            next_human_action = STEP_DICT[current_goal][step_index + 1]
            if previous_next_human_action != next_human_action and select:
                print("here")
            if step_index + 2 == len(STEP_DICT[current_goal]):
                # at second last step say that the goal for the last
                # step is 9
                next_goal = 9
            step_index += 1
        return step_index, next_human_action, next_goal, num_goals, is_goal_chosen

    def get_turn_information_old(self, children, num_goals=0):
        previous_goal, current_goal = children[0].turn_information._goal
        step_index = children[0].turn_information._step_information[0]
        if current_goal == 0:
            # this is the first step choose any of the
            # second steps
            next_human_action = np.random.choice(
                ["use_soap", "add_water_kettle_1"], p=[0.33, 1 - 0.33])
            if next_human_action == "use_soap":
                next_goal = 1
            else:
                next_goal = 2
                # TODO: need to make next goal random
                # next_goal = np.random.choice([2,3])
                # next_goal = -1
            # step_index+=1 #[Done]TODO:(not increment the previous stepindex that continues the numbering
            # rather reset it)
            step_index = 1
        elif current_goal == 9:
            # new goal needs to start
            # it should be opposite to previous
            # if previous_goal == 1:
            #     next_human_action = "add_water_kettle_1"
            # elif previous_goal == 2 or previous_goal ==3:
            #     next_human_action = "use_soap"
            next_human_action = "turn_on_faucet_1"
            next_goal = 0
            step_index = 0
            num_goals += 1
        else:
            # select the next human action for
            # the current ongoing goal
            # if current_goal == -1:
            # current_goal =previous_goal #np.random.choice([2,3])
            if current_goal == -1 and not is_goal_chosen:
                current_goal = np.random.choice([2, 3])
                is_goal_chosen = True
            elif current_goal == -1:
                current_goal = previous_goal
            next_goal = current_goal
            next_human_action = STEP_DICT[current_goal][step_index + 1]
            if step_index + 2 == len(STEP_DICT[current_goal]):
                # at second last step say that the goal for the last
                # step is 9
                next_goal = 9
            step_index += 1

        return step_index, next_human_action, next_goal, num_goals

    def execute_wrong_step_or_belief(self, next_human_action):
        is_wrong_step_or_belief = True
        sensor_notification = copy.deepcopy(
            realStateANDSensorUpdate(
                next_human_action,
                self.output_filename,
                real_step=False,
                is_wrong_step_or_belief=is_wrong_step_or_belief))
        is_haction_in_belief = False
        return sensor_notification, is_haction_in_belief

    def _simulate(self, rootnode, is_haction_in_belief,
                  num_goals, is_goal_chosen):
        '''args:
        rootnode: human_action node(vnode) with agent action added as children

        Returns the reward for a random simulation (to completion) of `node`"
        "one simulation till the end, this is rollout in jason's code'''
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
        # previous_goal = None
        # second_action = None
        # num_goals = 0
        total_goals = np.random.choice(2) + 1
        is_wrong_step_or_belief = False
        # is_goal_chosen = False
        total_reward = 0
        # is_haction_in_belief = True ## Done TODO: use the one passed down
        # from select
        discount = 1

        real_current_goal = node.turn_information._goal[1]  # current goal
        if real_current_goal != 0 and real_current_goal != 9:
            # current step names
            real_current_step = node.turn_information._step_information[1]
            # use the above information to update the step_information[0]
            if real_current_goal == -1:
                real_current_goal = np.random.choice([2, 3])
            adjusted_real_current_step_index = STEP_DICT[real_current_goal].index(
                real_current_step)
            node.turn_information._step_information[0] = adjusted_real_current_step_index

        # fix the step index to be the one relative to one goal not the one in
        # multiple goal
        while True:
            # chose agent action first

            if not node.turn_information.action_node:
                # current node isif node in self.children:
                #     children = self.children[node]
                # else: observation node
                # select next node - action based on preference
                # if node in self.children:
                #     children = self.children[node]
                # else:
                children = node.find_action_children()
                # should NOT make the node.turn_information.action_node true since flip at bottom
                # should make the node.turn_information.chosen_action non-None

                index = np.random.choice([0, 1])
                previous_node = node
                node = children[index]
                node.update_turn_information(previous_node)
                # node.turn_information = tmp_turn_information
                action = node.turn_information.chosen_action
                node = node.update_action(action, node)  # Todo: write better
                step_reward = self.get_step_reward(
                    is_haction_in_belief, action)
                is_haction_in_belief = True  # reset is_haction_in_belief for the next step
                total_reward += step_reward * discount
                discount *= self.gamma
            else:
                # then choose the human action with action response added to
                # it.
                children = node.find_observation_children()  # generate explasets
                if not children or step_num > self.depth or num_goals == total_goals:
                    return total_reward

                '''goal_complete = False
                single_goal_indices = []'''

                '''# select the index of explaset that have single goals
                for index, expla in enumerate(children[0].explaset._explaset):
                    if list(expla._start_task.values()).count(
                            0) == len(expla._start_task.keys()):
                        goal_complete = True
                    if list(expla._start_task.values()).count(1) == 1:
                        single_goal_indices.append(index)
                        # if all(expla._start_task.values == 0)'''

                # generate pending
                # inverse_pending_dict = defaultdict(list)
                current_explaset = children[0].explaset
                inverse_pending_dict, _ = current_explaset.pendingset_generate()
                step_index, next_human_action, next_goal, num_goals, is_goal_chosen = self.get_turn_information(
                    children, num_goals=num_goals, select=False, is_goal_chosen=is_goal_chosen)
                print("next human action is:", next_human_action, "next_goal is:", next_goal,
                      "next human action is part of belief:", next_human_action in inverse_pending_dict,
                      "pending dict is", inverse_pending_dict)
                if next_human_action == "get_cup_1":
                    print("here")
                if not next_human_action in inverse_pending_dict:
                    # is_wrong_step_or_belief = True
                    # sensor_notification = copy.deepcopy(
                    #     realStateANDSensorUpdate(
                    #         next_human_action,
                    #         self.output_filename,
                    #         real_step=False,
                    #         is_wrong_step_or_belief=is_wrong_step_or_belief))
                    # node.explaset.setSensorNotification(sensor_notification)
                    # is_haction_in_belief = False
                    sensor_notification, is_haction_in_belief = self.execute_wrong_step_or_belief(
                        next_human_action)
                    node.explaset.setSensorNotification(sensor_notification)

                    # keep the turn_information and node same, in case our simulator's action
                    # are not same as agent's belief
                    # we are covering the other happen corner case

                elif next_human_action in inverse_pending_dict:
                    next_sampled_explanation_index = np.random.choice(
                        inverse_pending_dict[next_human_action])
                    # TODO: Fix this add heauristic!
                    # if next_human_action == "open_coffee_box_1":
                    # print("here")
                    # print("next human action is:",next_human_action, "next_goal is:", goal)

                    # move to next agent state node with sampled_explanation
                    '''for start_task, value in expla._start_task.items():
                        if value == 1:
                            previous_goal = start_task'''
                    node = children[next_sampled_explanation_index]

                    sensor_notification = copy.deepcopy(
                        realStateANDSensorUpdate(
                            next_human_action,
                            self.output_filename,
                            real_step=False))
                    node.explaset.setSensorNotification(sensor_notification)

                with open(self.output_filename, 'a') as f:
                    f.write(
                        str(step_index) +
                        "\t " +
                        inverse_pending_dict.__str__() +
                        "\t")

                node.turn_information.update_turn_information(
                    step_index, next_human_action, next_goal)
                # node.turn_information._goal[0] = node.explaset._goal[1] ##make the current goal as previous
                # node.turn_information.goal[1] = next_goal
                # node.turn_information._step_information = [step_index,next_human_action]

                # update the action posterior

                node.explaset.action_posterior(
                    real_step=False, mcts_filename=self.output_filename)
                # update the explaset and pending set to be used for next
                # iteration

                step_num += 1
                # node.turn_information.step_index = step_num
            node.turn_information.action_node = not node.turn_information.action_node

            # TODO: keep track of goal change and 0,0,0
            # keep track of wrong step
            # some human action should be chosen from pending set

            # thisTree = copy.deepcopy(temp_forest.popleft())
            # tag = thisTree[0].get_node(thisTree[0].root).tag
            # parents = db.get_parent_list(tag)

    def _backpropagate(self, path, reward, step_rewards):
        "Send the reward back up to the ancestors of the leaf"
        # path [o,a,o] always end in o
        for node, step_reward in zip(reversed(path), reversed(step_rewards)):
            self.N[node] += 1
            if node.turn_information.action_node:
                self.Q[node] += step_reward + self.gamma * reward
            # reward = 1 - reward  # 1 for me is 0 for my enemy, and vice versa

    def _uct_select(self, node):
        "Select a action child of the current vnode(observation), balancing exploration & exploitation"

        # All children of node should already be expanded:
        # assert all(n in self.children for n in self.children[node]) ## so not
        # handle 0/inf case

        log_N_vertex = math.log(self.N[node])  # TODO:jason has plus 1 here

        def uct(n):
            "Upper confidence bound for trees"
            # Todo: handle n=0 case jason return Q
            q_val = self.Q[n] / self.N[n] if self.N[n] != 0 else self.Q[n]
            if self.N[n] == 0:
                return float("inf")
            return q_val + self.exploration_weight * math.sqrt(
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
