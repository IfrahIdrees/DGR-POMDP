from collections import namedtuple
from random import choice
import copy
import collections
import itertools

from sortedcontainers import SortedSet

from monte_carlo_tree_search import MCTS, MCNode
from ExecuteSequence import *
from TaskNet import *
from Explanation import *
from config import *
from State import *

_AS = namedtuple("AgentState", "explaset terminal action_node, step_index")
# Inheriting from a namedtuple is convenient because it makes the class
# immutable and predefines __init__, __repr__, __hash__, __eq__, and others


class AgentState(_AS, MCNode):
    # equality should be at expla not explaset
    # children will be expla

    def __init__(self, explaset, terminal, action_node, step_index):
        # self.explaset = explaset
        # self.terminal = terminal
        # self.pending_actions = set([action[0] for action in self._pendingSet])
        # self.execute_sequences = [taskNet._execute_sequence for taskNet in self._forest]
        # # self.flattened_execute_sequences = itertools.chain(*self.execute_sequences)
        # self.counter_execute_sequences = self.extract_execute_sequence(self.flattened_execute_sequences)

        self.pending_actions = None
        self.execute_sequences = None
        self.counter_execute_sequences = None
        self.sampled_explanation = None
        self._delete_trigger = self.explaset._delete_trigger
        self.successor_explanations = None
        # self.current_action =
        # TODO: ADD ACTION LIST
        # self.question_asked = None

    def append_children(self, children, new_explas):
        # remove = []
        for expla in new_explas:
            if expla._prob > self._delete_trigger:

                children.append(expla)
        return children

    def __hash__(self) -> int:
        hashint = 0
        # hashint+=hash(str(self.terminal))
        hashint += hash("".join(set(self.pending_actions)))
        hashint += hash(json.dumps(self.counter_execute_sequences))
        hashint += hash(json.dumps(self.sampled_explanation._start_task))
        hashint += self.step_index
        return hashint

    def extract_execute_sequence(self, execute_sequence):
        # counter_execute_sequence = collections.Counter(itertools.chain(*execute_sequence)).most_common()
        counter_execute_sequence = collections.Counter(
            execute_sequence).most_common()
        return counter_execute_sequence

    def __eq__(self, other):
        # self_pending_actions = set([action[0] for action in self._pendingSet])
        # other_pending_actions = set([action[0] for action in other._pendingSet])
        # self_execute_sequence = [taskNet._execute_sequence for taskNet in self._forest]
        # other_execute_sequence = [taskNet._execute_sequence for taskNet in other._forest]
        # check_counter_execute_sequence = collections.Counter(itertools.chain(*self_execute_sequence)) == collections.Counter(itertools.chain(*other_execute_sequence))
        # if isinstance(other, Explanation) and \
        #     self._start_task == other._start_task and\
        #     len(self.execute_sequences)  == len(other.execute_sequences) and\
        #     check_counter_execute_sequence:
        #     # self_pending_actions == other_pending_actions and
        #     return True
        # return False

        if self.__hash__() == other.__hash__():
            return True
        return False

    def find_children(self):
        children = []
        # find = False
        # Case2 : continue on an on-going task
        # update existing tree structure, if the action exist in the
        # pending set of this tree structure
        # TODO: human tuurn. agent tuen and terminal of next child set
        for action, action_prob in self.explaset._action_posterior_prob.items():
            new_explas = self.sampled_explanation.generate_new_expla_part1(
                [action, action_prob])

            children = self.append_children(children, new_explas)

        if "nothing" in self.explaset._action_posterior_prob.keys():
            print("here")
            del self.explaset._action_posterior_prob["nothing"]

        state = State()
        state.update_state_belief(self.explaset)

        for action, action_prob in self.explaset._action_posterior_prob.items():
            new_explas = self.sampled_explanation.generate_new_expla_part2(
                [action, action_prob])
            children = self.append_children(children, new_explas)

        # for taskNet in self.sampled_explanation._forest:
        #     for taskNetPending in taskNet._pendingset:
        #         for act_expla in taskNetPending._pending_actions:
        #         #get a new taskNet start
        #             theTree = copy.deepcopy(taskNetPending._tree)
        #             action_node = theTree.get_node(act_expla)
        #             action_node.data._completeness = True
        #             executed_sequence = ExecuteSequence(sequence = copy.deepcopy(taskNet._execute_sequence._sequence), effect_summary = copy.deepcopy(taskNet._execute_sequence._effect_summary))
        #             executed_sequence.add_action(act_expla)
        #             newTaskNet = TaskNet(goalName = theTree.get_node(theTree.root).tag, tree = theTree, expandProb = taskNetPending._branch_factor, execute_sequence = executed_sequence)
        #             # newTaskNet = TaskNet(goalName = theTree.get_node(theTree.root).tag, tree = theTree, expandProb = taskNetPending._branch_factor, execute_sequence = copy.deepcopy(executed_sequence))
        #             newTaskNet.update()
        #             #get a new taskNet end

        #             newforest = list(self.sampled_explanation._forest)
        #             newforest.remove(taskNet)
        #             prob = newTaskNet._expandProb*self.sampled_explanation._prob

        #                 ##this goal has already been completed
        #                 ##remove it and add its start action into
        #                 ##the explanation start action list
        #             if newTaskNet._complete==True:
        #                 newstart_task = copy.deepcopy(self.sampled_explanation._start_task)
        #                 newstart_task[newTaskNet._goalName] = 0
        #                 newexp = Explanation(v=prob, forest = newforest, start_task=newstart_task)

        #                 ##this goal has not been completed
        #             else:
        #                 newforest.append(newTaskNet)
        #                 newstart_task = copy.deepcopy(self.sampled_explanation._start_task)
        #                 newexp = Explanation(v=prob, forest = newforest, start_task=newstart_task)

        #             children = self.append_children(children, [newexp])

        '''self.successor_explanations = children'''
        # node.pending_actions = set([action[0] for action in node.sampled_explanation._pendingSet])
        # node.execute_sequences = [taskNet._execute_sequence for taskNet in node.sampled_explanation._forest]
        # flattened_execute_sequences = itertools.chain(*node.execute_sequences)
        # node.counter_execute_sequences = node.extract_execute_sequence(flattened_execute_sequences)

        '''create agent states from the children'''
        next_states = []
        for index in range(len(children)):
            next_state = copy.deepcopy(self)
            next_state.explaset._explaset = children
            next_state.sampled_explanation = children[index]
            next_states.append(next_state)
        return next_states

    def sample_explanation(self, explanations):
        # probs = [explanations[i]._prob for i in range(len(explanations))]
        # index = np.random.choice(len(self.explaset._explaset), 1, p=probs)[0]
        # print(self.explaset)
        index = np.random.choice(len(explanations))
        self.sampled_explanation = copy.deepcopy(explanations[index])

    def find__highes_prob_children(self):
        new_explas = []

        # sample next tasknet
        taskNets = self.sampled_explanation._forest
        probs = [taskNets[i]._expandProb for i in range(len(taskNets))]
        index = np.random.choice(len(taskNets), 1, p=probs)[0]
        next_taskNet = taskNets[index]

        # sample next action for taskNet
        taskNetPending = next_taskNet._pendingset
        probs = [
            taskNetPending._branch_factor for i in range(
                len(taskNetPending))]
        index = np.random.choice(len(taskNetPending), 1, p=probs)[0]
        next_sampled_human_action = np.random.uniform(
            taskNetPending[index]._pending_actions)

        # get a new taskNet start
        theTree = copy.deepcopy(taskNetPending._tree)
        action_node = theTree.get_node(next_sampled_human_action)
        action_node.data._completeness = True
        executed_sequence = ExecuteSequence(
            sequence=copy.deepcopy(
                taskNet._execute_sequence._sequence), effect_summary=copy.deepcopy(
                taskNet._execute_sequence._effect_summary))
        executed_sequence.add_action(next_sampled_human_action)
        newTaskNet = TaskNet(
            goalName=theTree.get_node(
                theTree.root).tag,
            tree=theTree,
            expandProb=taskNetPending._branch_factor,
            execute_sequence=executed_sequence)
        # newTaskNet = TaskNet(goalName = theTree.get_node(theTree.root).tag, tree = theTree, expandProb = taskNetPending._branch_factor, execute_sequence = copy.deepcopy(executed_sequence))
        newTaskNet.update()
        # get a new taskNet end

        prob = newTaskNet._expandProb * self.sampled_explanation._prob

        # this goal has already been completed
        # remove it and add its start action into
        # the explanation start action list
        if newTaskNet._complete:
            newstart_task = copy.deepcopy(self._start_task)
            newstart_task[newTaskNet._goalName] = 0
            newexp = Explanation(
                v=prob,
                forest=newforest,
                start_task=newstart_task)

            # this goal has not been completed
        else:
            newforest.append(newTaskNet)
            newstart_task = copy.deepcopy(self._start_task)
            newexp = Explanation(
                v=prob,
                forest=newforest,
                start_task=newstart_task)

        new_explas.append(newexp)

        return new_explas

        # for taskNet in self._forest:

        # return super().find_children()

    def sample(self):
        '''Sample for current node from current explaset'''
        probs = [self.explaset._explaset[i]._prob for i in range(
            len(self.explaset._explaset))]
        index = np.random.choice(len(self.explaset._explaset), 1, p=probs)[0]
        print(self.explaset)
        self.sampled_explanation = copy.deepcopy(
            self.explaset._explaset[index])

        self.pending_actions = SortedSet(
            [action[0] for action in self.sampled_explanation._pendingSet])
        self.execute_sequences = [
            taskNet._execute_sequence._sequence for taskNet in self.sampled_explanation._forest]
        flattened_execute_sequences = itertools.chain(*self.execute_sequences)
        self.counter_execute_sequences = self.extract_execute_sequence(
            flattened_execute_sequences)

    # def simulate(self,monte_carlo_tree):
    #     self.pending_actions = set([action[0] for action in self.sampled_explanation._pendingSet])
    #     self.execute_sequences = [taskNet._execute_sequence for taskNet in self.sampled_explanation._forest]
    #     flattened_execute_sequences = itertools.chain(*self.execute_sequences)
    #     self.counter_execute_sequences = self.extract_execute_sequence(flattened_execute_sequences)
    #     # for i in range(monte_carlo_tree.sim_num):
    #     for i in range(1):
    #         pipeline = [ {"$match": {}},
    #                     {"$out": "state"},
    #         ]
    #         self.db._backup_state.aggregate(pipeline)

    #         pipeline = [ {"$match": {}},
    #                     {"$out": "sensor"},
    #         ]
    #         self.db._backup_sensor.aggregate(pipeline)

    #         monte_carlo_tree.do_rollout(self)

    #     # return monte_carlo_tree.choose(self)
    #     return None
