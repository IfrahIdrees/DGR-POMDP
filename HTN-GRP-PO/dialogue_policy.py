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


class Action:

    def __init__(self, name):
        self.name = name


class TurnInformation:

    def __init__(self, terminal, action_node, step_index):
        self.terminal = terminal
        self.action_node = action_node
        self.step_index = step_index
        self.chosen_action = None


class AgentAskClarificationQuestion(Action):
    """
    Robot action for giving the next instruction
    """
    # @II need to code that it increases instruction by 1. As in MoveAction East is (1,0) (just defining)

    def __init__(self):
        super().__init__("ask-clarification-question")
        self.question_asked = None

    def update_question_asked_param(self, state, question_asked_pair=None):
        current_pending_set = np.asarray(state.sampled_explanation._pendingSet)
        index = np.argmax(current_pending_set[:, 1], axis=0)
        self.question_asked = current_pending_set[index, 0]


_AS = namedtuple("AgentState", "explaset turn_information")
# Inheriting from a namedtuple is convenient because it makes the class
# immutable and predefines __init__, __repr__, __hash__, __eq__, and others


class AgentState(_AS, MCNode):
    # equality should be at expla not explaset
    # children will be expla

    def __init__(self, explaset, turn_information):
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
        hashint += self.turn_information.step_index
        hashint += self.turn_information.action_node
        hashint += hash(self.turn_information.chosen_action)
        return hashint

    def extract_execute_sequence(self, execute_sequence):
        # counter_execute_sequence = collections.Counter(itertools.chain(*execute_sequence)).most_common()
        counter_execute_sequence = collections.Counter(
            execute_sequence).most_common()
        return counter_execute_sequence

    def __eq__(self, other):
        if self.__hash__() == other.__hash__():
            return True
        return False

    def find_action_children(self):
        children = []
        action_list = [Action("wait"), AgentAskClarificationQuestion()]
        for action in action_list:
            next_state = copy.deepcopy(self)
            # next_state.turn_information.action_node = True
            next_state = self.update_action(action, next_state)
            children.append(next_state)

        return children

    def update_turn_information(self, tmp_node):
        self.turn_information.action_node = tmp_node.turn_information.action_node
        self.turn_information.chosen_action = tmp_node.turn_information.chosen_action
        self.turn_information.step_index = tmp_node.turn_information.step_index
        self.turn_information.terminal = tmp_node.turn_information.terminal

    def update_action(self, action, next_state):
        if isinstance(action, AgentAskClarificationQuestion):
            action.update_question_asked_param(next_state)
            next_state.turn_information.chosen_action = action
        return next_state

    def __str__(self):
        return self.__repr__()

    def find_observation_children(self):
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

        # return super().find_observation_children()

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
