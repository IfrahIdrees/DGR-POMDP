"""------------------------------------------------------------------------------------------
Hierarchical Task Recognition and Planning in Smart Homes with Partially Observability
Author: Dan Wang danwangkoala@gmail.com (May 2016 - June 2017)
Supervised by Prof. Jesse Hoey (https://cs.uwaterloo.ca/~jhoey/)
Association: Computer Science, University of Waterloo.
Research purposes only. Any commerical uses strictly forbidden.
Code is provided without any guarantees.
Research sponsored by AGEWELL Networks of Centers of Excellence (NCE).
----------------------------------------------------------------------------------------------"""
##########################################################################
####                    The ExplaSet class                                                         ####
####                    Also refer to "Interface specification part II"                            ####
##########################################################################

# import numpy as np
import operator
import functools
import itertools
from config import *
import math
from CareGiver import *
from SensorCheck import *
from TaskHint import *
from helper import *
from Explanation import *
from database import *
from collections import deque
from collections import defaultdict
import collections

import copy
import sys
sys.dont_write_bytecode = True

# np.random.seed(10)
# from __future__ import print_function  # Only needed for Python 2

db = DB_Object()


class explaSet(object):
    def __init__(
            self,
            cond_satisfy=1.0,
            cond_notsatisfy=0.0,
            delete_trigger=0.001,
            non_happen=0.0001,
            output_file_name="Case4.txt"):
        self._cond_satisfy = cond_satisfy
        self._cond_notsatisfy = cond_notsatisfy
        self._delete_trigger = delete_trigger
        self._explaset = deque([])
        self._action_posterior_prob = {}
        self._non_happen = non_happen
        self._sensor_notification = []
        self._output_file_name = output_file_name
        self._prior = {}
        self._other_happen = None
        self.aggregate_pending_set = None
        self.flattened_execute_sequences = None
        if config.args.domain == "kitchen":
            self.start_task = {
                'wash_hand': 0,
                "make_tea": 0,
                "make_coffee": 0
            }
        else:
            self.start_task = {
                "stack_word_ROTE": 0,
                "stack_word_TONE": 0,
                "stack_word_TUNE": 0,
                "stack_word_HAWK": 0,
                "stack_word_CAPSTONE": 0
            }
        # self.start_task = None

    ##########################################################################
    # Part I
    # Basic function about the explanation set. Include:
    # add, pop, length, get, set parameter value, normalize,
    ##########################################################################

    def add_exp(self, e):
        if e._prob > self._delete_trigger:
            self._explaset.append(e)

    def pop(self):
        # get an explanation and remove it
        return self._explaset.popleft()

    def length(self):
        return len(self._explaset)

    def get(self, index):
        # return self._explaset[len(self._explaset) - index]
        return self._explaset[index]

    def setSensorNotification(self, sensor_notification):
        self._sensor_notification = copy.deepcopy(sensor_notification)

    # Functionality: remove explanations with prob smaller than delete_trigger
    # Normalize the remaining explanations
    def normalize(self):
        leng = len(self._explaset)
        my_sum = 0
        for x in self._explaset:
            my_sum = my_sum + x._prob
        if my_sum == 0.0:
            return
        for x in self._explaset:
            x._prob = x._prob / my_sum

    def normalize_dict(self, dict_):
        my_sum = sum(dict_.values())
        if my_sum == 0.0:
            return
        for key, x in dict_.items():
            dict_[key] = dict_[key] / my_sum

    def print_explaSet(self):
        with open(self._output_file_name, 'a') as f:
            f.write(str(len(self._explaset)) + "\n")
            # f.write('{:>12}'.format(str(len(self._explaset))))
            # f.write('\n')

    # write the explanation into a .txt file
    def print_explaSet1(self):

        with open(self._output_file_name, 'a') as f:
            new_line = "Explanation Number:  " + \
                str(len(self._explaset)) + "\n"
            f.write(new_line)
        '''
            for index in range(len(self._explaset)):
                x = self._explaset[index]
                new_line = "\n" + "--------------Explanation " + str(index+1) + "------------------\n"
                f.write(new_line)

                new_line = '{:>30} {:>12}'.format("The probability: ", round(x._prob, 4))
                f.write(new_line)
                f.write("\n")

                new_line = '{:>30} {:>12}'.format("The current pending set is: ", x._pendingSet)
                f.write(new_line)
                f.write("\n")

                new_line = '{:>30} {:>12}'.format("The tasks ongoing are: ", x._start_task)
                f.write(new_line)
                f.write("\n")

                for y in x._forest:
                    f.write("\n")
                    new_line = '{:>30} {:<12}'.format("Goal Name: ", y._goalName)
                    f.write(new_line)
                    f.write("\n")

                    for actions in y._pendingset:
                        new_line = '{:>30} {:>12}'.format("The pendingSet for this Goal: ", actions._pending_actions)
                        f.write(new_line)
                        f.write("\n")
            f.write("\n")
        '''

    ##########################################################################
    # Part II
    # Explanation Set initialization, especially initialize
    # This part is only executed when start the agent
    ##########################################################################

    def explaInitialize(self):
        # initialzie the explanation. At very beginning, the explanation is "nothing happend"
        # It's pendingSet is all the start actions of all the method in the
        # database
        goal = db.find_all_method()
        mypendingSet = []
        mystart_task = {}
        candicatePendingSet = {}

        goalNum = 0
        for x in goal:
            if len(x["start_action"]) > 0:
                goalNum = goalNum + 1
                mystart_task[x["m_name"]] = 0
        goalPrior = float(1) / goalNum
        for x in goal:
            if len(x["start_action"]) > 0:
                mystart_task[x["m_name"]] = 0  # this task has not started yet

                for y in x["start_action"]:
                    if y not in candicatePendingSet:
                        candicatePendingSet[y] = goalPrior * \
                            float(1) / len(x["start_action"])
                    else:
                        candicatePendingSet[y] = candicatePendingSet[y] + \
                            goalPrior * float(1) / len(x["start_action"])

        for x in candicatePendingSet:
            mypendingSet.append([x, candicatePendingSet[x]])
        exp = Explanation(v=1, pendingSet=mypendingSet,
                          start_task=mystart_task)
        self._explaset.append(exp)

    ##########################################################################
    # Part III
    # Calculate posterior probability of actions in the pend
    # Also refer to "Step recognition.md"
    ##########################################################################

    def action_posterior(self, real_step=True,
                         mcts_filename=None, is_correction=None):
        self._action_posterior_prob = {}
        otherHappen = 1
        for expla in self._explaset:
            for action in expla._pendingSet:
                if action[0] in self._action_posterior_prob:
                    self._action_posterior_prob[action[0]
                                                ] = self._action_posterior_prob[action[0]] + action[1]

                else:
                    self._action_posterior_prob[action[0]] = action[1]
        # ---------------------------------
        # '''
            for start_task in expla._start_task:
                if expla._start_task[start_task] == 0:
                    target_method = db.find_method(start_task)
                    initialize_prob = expla._prob / \
                        (len(expla._pendingSet) +
                         len(target_method["start_action"]))
                    for start_action in target_method["start_action"]:
                        if start_action in self._action_posterior_prob:
                            self._action_posterior_prob[start_action] = self._action_posterior_prob[start_action] + initialize_prob
                        else:
                            self._action_posterior_prob[start_action] = initialize_prob
                        # if start_action not in self._action_posterior_prob:
                            # self._action_posterior_prob[start_action] = self._delete_trigger #initialize_prob
        # '''
        # ---------------------------------
        # self.normalize_dict(self._action_posterior_prob)
        self._prior = copy.deepcopy(self._action_posterior_prob)

        highest_action_PS = ["", float('-inf')]
        for k, v in self._action_posterior_prob.items():
            if v > highest_action_PS[1]:
                highest_action_PS = [k, v]

        self.highest_action_PS = highest_action_PS
        # otherHappen = 0
        otherHappen_dict = {}
        happen_dict = {}
        for k in self._action_posterior_prob:
            posteriorK, not_happen_prob = self.cal_posterior(k)
            happen_dict[k] = posteriorK
            posteriorK = posteriorK / (posteriorK + not_happen_prob)
            otherHappen = otherHappen - posteriorK * \
                self._action_posterior_prob[k]  # * 1/ len(self._explaset)
            self._action_posterior_prob[k] = self._action_posterior_prob[k] * posteriorK
            otherHappen_dict[k] = not_happen_prob

        # otherHappen  = sum(otherHappen_dict.values())
        # with open(self._output_file_name, 'a') as f:
        #     f.write(str(round(otherHappen, 4)) + "\t")

        '''happen_posterior_dict = {}
        for key, value in happen_dict.items():
            happen_posterior_dict[key] = happen_dict[key] * self._prior[key]

        weighted_happen_dict = {}
        for key, value in happen_dict.items():
            weighted_happen_dict[key] = happen_dict[key] / \
                (happen_dict[key] + otherHappen_dict[key])

        weighted_posterior_happen_dict = {}
        for key, value in happen_dict.items():
            weighted_posterior_happen_dict[key] = weighted_happen_dict[key] * \
                self._prior[key]'''  # no used

        # return otherHappen > sum(happen_dict.values())
        # added to correct all except 10
        self.normalize_dict(self._action_posterior_prob)

        # variance = max(self._prior.values())-min(self._prior.values()) #added to correct 10 plans 10 plans wrong but other happen not called
        # otherHappen = otherHappen*variance
        if not is_correction:
            if not real_step:
                with open(mcts_filename, 'a') as f:
                    f.write(str(round(otherHappen, 4)) + "\n")
            else:
                with open(self._output_file_name, 'a') as f:
                    f.write(str(round(otherHappen, 4)) + "\t")
        self._other_happen = otherHappen
        return otherHappen

    # version begin from March 14, 2017

    def cal_posterior(self, action):
        op = db.get_operator(action)

        objAttSet = set()
        for obj in op["precondition"]:
            for att in op["precondition"][obj]:
                objAttSet.add(obj + "-" + att)
        for obj in op["effect"]:
            for att in op["effect"][obj]:
                objAttSet.add(obj + "-" + att)

        title = []
        for item in objAttSet:
            title.append(item.split("-"))
        # attribute is the corresponding attribute distribution in title
        title = sorted(title)
        attribute = []
        observe_prob = []
        for item in title:
            attri_distribute = db.get_object_attri(item[0], item[1])
            attribute.append(attri_distribute)
            observe_distribute = {}
            for value in attri_distribute:
                observe_distribute[value] = db.get_obs_prob(
                    value, item[0], item[1])
            observe_prob.append(observe_distribute)

        enum = self.myDFS(attribute)
        happen_prob, not_happen_prob = self.variable_elim(
            enum, op, title, attribute, observe_prob)

        return happen_prob, not_happen_prob

    # dfs is used to generate the enumeration of all possible state
    # combinations
    def myDFS(self, attribute):
        enum = []
        va = []
        self.realMyDFS(enum, va, attribute)
        return enum

    def realMyDFS(self, enum, va, attribute):
        if len(va) == len(attribute):
            enum.append(list(va))
            return
        index = len(va)
        for x in attribute[index]:
            va.insert(index, x)
            self.realMyDFS(enum, va, attribute)
            va.pop()

    # implement the bayesian network calculation for one possible state
    # op: the operator in knowlege base, prob: the prior of the action
    def variable_elim(self, enum, op, title, attribute, observe_prob):
        new_prob_1 = 0  # this action happened
        new_prob_2 = 0  # this action does not happend
        for before in enum:
            for after in enum:
                p = self.bayesian_expand(
                    before, after, op, title, attribute, observe_prob)
                new_prob_1 = new_prob_1 + p[0]
                new_prob_2 = new_prob_2 + p[1]
        # return float(new_prob_1)/(new_prob_1+new_prob_2)
        return new_prob_1, new_prob_2

    # sv: an concrete state value, op: the operator in knowledge base
    # state_c: the notification
    def bayesian_expand(
            self,
            before,
            after,
            op,
            title,
            attribute,
            observe_prob):
        # calculate p(s_t-1)
        ps_before = 1
        for i, s in enumerate(before):
            ps_before = ps_before * attribute[i][s]

        # calculate p(o_t|s_t)
        po_s = 1
        for i, s in enumerate(after):
            po_s = po_s * observe_prob[i][s]

        # calculate p(s|s_t-1, a_t)
        ps_actANDs_1 = self.get_ps_actANDs_1(before, after, op, title)
        ps_actANDs_2 = self.get_ps_actANDs_2(before, after)

        prob = []
        prob.append(float(ps_before) * po_s * ps_actANDs_1)
        prob.append(float(ps_before) * po_s * ps_actANDs_2)

        return prob

    # calculate p(s|s_t-1, a_t) happen
    def get_ps_actANDs_1(self, before, after, op, title):
        bef = list(before)
        af = list(after)

        # check precondition
        prob = 1
        precond = op["precondition"]
        for ob in precond:
            for attri in precond[ob]:
                index = title.index([ob, attri])
                if attri == "ability":
                    ability_list = bef[index].split(",")
                    if compare_ability(
                            ability_list, precond[ob][attri]) is False:
                        print("return not satisfy because of ability not enough ")
                        return self._cond_notsatisfy
                else:
                    if precond[ob][attri] != bef[index]:
                        return self._cond_notsatisfy

        # check effect
        effect = op["effect"]
        for ob in effect:
            for attri in effect[ob]:
                index = title.index([ob, attri])
                bef[index] = effect[ob][attri]
        if bef != af:
            return self._cond_notsatisfy

        return self._cond_satisfy

    # calculate p(s|s_t-1, a_t) not happen

    def get_ps_actANDs_2(self, before, after):
        if before == after:
            return self._cond_satisfy
        else:
            return self._cond_notsatisfy

    ##########################################################################
    # Part IV
    # Expand the explanation Set
    # Each explanation can be extended into multiple explanation
    # Based on which actions has happened
    ##########################################################################

    # "explaSet_expand_part1" is used to generate explanations that add a new tree structure, a bottom-up process
    # The bottom-up process depend on the previous state.
    def explaSet_expand_part1(self, length):

        for i in range(length):
            # x = self.get(i + 1)
            x = self.get(i)
            # x = self.pop()
            # print("action posterior after bayseian inference is",  self._action_posterior_prob)
            for action in self._action_posterior_prob:
                # case1: nothing happened: update the prob of the
                # explanation,do not need to update tree structure.
                if action == "nothing":
                    newstart_task = copy.deepcopy(x._start_task)
                    newexpla = Explanation(
                        v=x._prob *
                        self._action_posterior_prob[action],
                        forest=x._forest,
                        pendingSet=x._pendingSet,
                        start_task=newstart_task)
                    self.add_exp(newexpla)

                else:
                    # case2:something happend, need to update the tree
                    # structure
                    new_explas = x.generate_new_expla_part1(
                        [action, self._action_posterior_prob[action]])

                    for expla in new_explas:
                        self.add_exp(expla)

        return

    # "explaSet_expand_part2" is used to generate explanations by decomposing an existing tree structure. , a top-down process
    # The top=down process depends on the current state. (after adding the
    # effect of just happened action)
    def explaSet_expand_part2(self, length):
        for i in range(length):
            x = self.pop()
            for action in self._action_posterior_prob:
                if action == "nothing":
                    continue
                new_explas = x.generate_new_expla_part2(
                    [action, self._action_posterior_prob[action]])
                for expla in new_explas:
                    self.add_exp(expla)
        return

    ##########################################################################
    # Part V
    # Generate the new pending set for each explanation
    # based on the current tree structure and belief state
    ##########################################################################
    def extract_execute_sequence(self, execute_sequence):
        # counter_execute_sequence = collections.Counter(itertools.chain(*execute_sequence)).most_common()
        counter_execute_sequence = collections.Counter(
            execute_sequence).most_common()
        return counter_execute_sequence

    def pendingset_generate(self):
        ''',inverse_pending_set=None,
        single_goal_indices=None, previous_goal=None,
        real_step = True):'''
        self.normalize()
        inverse_pending_dict = defaultdict(list)
        aggregate_pending_set = np.zeros(shape=(1, 2))
        index = 0
        execute_sequences = []
        start_tasks = []
        for expla in self._explaset:
            pending_set = expla.create_pendingSet()
            for act, prob in pending_set:
                inverse_pending_dict[act].append(index)
                aggregate_pending_set = np.vstack(
                    [aggregate_pending_set, pending_set])
            start_tasks.append(expla._start_task)
            # update the execute sequence and start task
            for taskNet in expla._forest:
                execute_sequences.append(taskNet._execute_sequence._sequence)
            index += 1
        flattened_execute_sequences = itertools.chain(
            *execute_sequences)
        self.counter_execute_sequences = self.extract_execute_sequence(
            flattened_execute_sequences)
        # self.start_task = dict(functools.reduce(operator.add,
        # map(collections.Counter, start_tasks)))

        for start_task_dict in start_tasks:
            for key in start_task_dict:
                self.start_task[key] += start_task_dict[key]

        self.flattened_execute_sequences = execute_sequences
        # self.counter_execute_sequences = counter_execute_sequences
        aggregate_pending_set = np.delete(aggregate_pending_set, 0, 0)
        self.aggregate_pending_set = aggregate_pending_set[:, 0]
        return inverse_pending_dict, aggregate_pending_set

        '''##### pending set generate with
        aggregate_pending_set = np.zeros(shape=(1, 2))
        self.normalize()
        index = 0
        for expla in self._explaset:
            pending_set = expla.create_pendingSet()
            pending_dict = {}
            filtered_pending_set = []

            if not real_step:
                'Look for tasknets having goal similar to previous goal'
                'Need to make inverse pending dict'
                # pending_set = np.asarray(pending_set)
                if previous_goal == None:
                    aggregate_pending_set = np.vstack(
                    [aggregate_pending_set, pending_set])
                else:
                    for act, prob in pending_set:
                        pending_dict[act] = prob
                    for tasknet in expla._forest:
                        if tasknet._goalName == previous_goal:
                            for pending_action in tasknet._pendingset:
                                filtered_pending_set.append([pending_action,pending_dict[pending_action]])
                    aggregate_pending_set = np.vstack(
                        [aggregate_pending_set, filtered_pending_set])'''
        '''only look for explanation with single goal
                if single_goal_indices and index in single_goal_indices:
                if isinstance(inverse_pending_set, defaultdict):
                    for pending_action in pending_set:
                        inverse_pending_set[pending_action[0]].append(index)
                aggregate_pending_set = np.vstack(
                    [aggregate_pending_set, pending_set])'''

        '''# aggregate_pending_set[index] =  np.vstack([aggregate_pending_set,pending_set])
            index += 1
            # aggregate_pending_set.append(pending_set)
        aggregate_pending_set = np.delete(aggregate_pending_set, 0, 0)
        return aggregate_pending_set, inverse_pending_set'''
    ##########################################################################
    # Part VI
    # Calculate the probability of each node in the explanation
    # Output the probability of each tast and the average level
    # based on the current tree structure and belief state
    ##########################################################################

    def task_prob_calculate(self):
        taskhint = TaskHint(self._output_file_name)
        taskhint.reset()
        for expla in self._explaset:
            expla.generate_task_hint(taskhint)

        taskhint.average_level()

        taskhint.print_taskhintInTable()
        return taskhint
    ##########################################################################
    # Part VII
    # Exception handling. This part is used when the probability
    # "otherHappen" is too high.
    # Exception handling can deal with (1)sensor die (2)wrong st
    ##########################################################################

    def handle_exception(self):
        print("into handle exception")
        sensor_cause = {}
        sensor_cause["bad_sensor"] = []
        sensor_cause["sensor_cause"] = False
        wrong_step_cause = False

        for step in self._action_posterior_prob:
            operator = db.get_operator(step)
            effect_length = get_effect_length(operator)
            if effect_length >= len(self._sensor_notification):
                this_sensor_cause = operator_sensor_check(operator)
                sensor_cause["bad_sensor"].extend(
                    this_sensor_cause["bad_sensor"])

        # bad sensor cause the exception, call the caregiver to repair the
        # sensors
        if len(sensor_cause["bad_sensor"]) > 0:
            print("bad sensor cause sensor exception")
            sensor_cause["sensor_cause"] = True
            call_for_caregiver_sensor_cause(
                sensor_cause["bad_sensor"], self._output_file_name)

        # wrong step cause the exception
        self.handle_wrong_step_exception()

    # ----------------------------------------------------------------------
    # the wrong step might violate soft_constraint or hard_constraint
    # 1. soft_constraint:   the wrong step does not impact on objects related to already happened steps' effects.
    #                       In this case, the wrong step violate soft_constraint (logically wrong, e.g. rinse hand before use soap)
    #                       Do not update the current explanation, give the previous hint, do not update state belief,
    # 2. hard_constraint:   the wrong step does impact on objects related to already happened steps' effects
    #                       In this case, the wrong step violate hard_constraint (destroy the required preconditions for later steps)
    #                       Need to backtrack to the step that create the precondtions and start from that point.
    #                       Need to update tree structure and the new pendingSet. Need to update belief state
    # 3. state_update:      Finally weather update the state depends the sum
    # probability of update and no-update
    def handle_wrong_step_exception(self):
        # record to what degree the belief state should be updated
        belief_state_repair_summary = {}

        for expla in self._explaset:
            expla_repair_result = expla.repair_expla(self._sensor_notification)
            if expla_repair_result[0] != 0.0:
                self.belief_state_repair_summary_extend(
                    belief_state_repair_summary, expla_repair_result)

        self.belief_state_repair_execute(belief_state_repair_summary)

    # add the expla_repair_result into belief_state_repair_summary
    # expla_repair_result [prob, {key:value}]
    def belief_state_repair_summary_extend(
            self,
            belief_state_repair_summary,
            expla_repair_result):
        for x in expla_repair_result[1]:
            newkey = x + "/" + expla_repair_result[1][x]
            if newkey in belief_state_repair_summary:
                belief_state_repair_summary[newkey] = belief_state_repair_summary[newkey] + \
                    expla_repair_result[0]
            else:
                belief_state_repair_summary[newkey] = expla_repair_result[0]

    def belief_state_repair_execute(self, belief_state_repair_summary):
        for effect in belief_state_repair_summary:
            # if belief_state_repair_summary[effect] > 0.7:
            belief_state = effect.split("/")
            opposite_attri_value = db.get_reverse_attribute_value(
                belief_state[0], belief_state[1], belief_state[2])
            new_att_distribution = {}
            new_att_distribution[belief_state[2]
                                 ] = belief_state_repair_summary[effect]
            new_att_distribution[opposite_attri_value] = 1 - \
                belief_state_repair_summary[effect]

            db.update_state_belief(
                belief_state[0], belief_state[1], new_att_distribution)
        return

    def update_with_language_feedback(self, step, highest_action_PS, p_l):
        # for expla in self._explaset:
        #     expla
        weights = [0 for i in range(len(self._explaset))]
        for ind, expla in enumerate(self._explaset):
            # goal_prob = expla._prob
            correct_taskNets = 0

            for taskNet_ in expla._forest:
                # for taskNet_ in forest:
                ExecuteSequence = taskNet_._execute_sequence._sequence
                if ExecuteSequence == []:
                    # taskNet_._expandProb *= 0.01
                    # expla._prob*=0.01
                    continue
                if highest_action_PS[0] == ExecuteSequence[-1] and step == config.positive_feedback:
                    correct_taskNets += 1
                    # taskNet_._expandProb *= 0.99
                    # expla._prob*=0.99
                elif not (highest_action_PS[0] == ExecuteSequence[-1]) and step == config.positive_feedback:
                    # taskNet_._expandProb *= 0.01
                    # expla._prob*=0.01
                    continue
                elif step == config.negative_feedback and not (highest_action_PS[0] == ExecuteSequence[-1]):
                    correct_taskNets += 1
                    # taskNet_._expandProb *= 0.99
                    # expla._prob*=0.99
                elif step == config.negative_feedback and (highest_action_PS[0] == ExecuteSequence[-1]):
                    # taskNet_._expandProb *= 0.01
                    # expla._prob*=0.01
                    continue

                # taskNet_._expandProb *= p_l
                # expla._prob*=p_l
            delta = 0.001
            if len(expla._forest) == 0:
                weight = 0 + delta
            else:
                weight = float(correct_taskNets) / len(expla._forest) + delta
            # using tasknets as weightd for adjust probs of explanation prob.
            # but after normalizing it is the same.
            expla._prob *= weight * p_l

            for ind in range(len(expla._pendingSet)):
                '''expla._pendingSet[ind][1]*=weight*p_l'''
                expla._pendingSet[ind][1] = expla._prob / \
                    len(expla._pendingSet)

        return

        #         expla._pendingSet
        # if action[0] in self._action_posterior_prob:
        #     self._action_posterior_prob[action[0]] = self._action_posterior_prob[action[0]] + action[1]

        # else:
        #     self._action_posterior_prob[action[0]] = action[1]
        # for ac

    def update_without_language_feedback(self, p_l):
        # for expla in self._explaset:
        #     expla

        for expla in self._explaset:
            # goal_prob = expla._prob
            # for taskNet_ in expla._forest:
            # for taskNet_ in forest:
            # ExecuteSequence =  taskNet_._execute_sequence._sequence
            # if highest_action_PS[0] in ExecuteSequence and step == config.positive_feedback:
            #     taskNet_._expandProb *= 0.99
            #     expla._prob*=0.99
            # elif not (highest_action_PS[0] in ExecuteSequence) and step == 'Yes':
            #     taskNet_._expandProb *= 0.01
            #     expla._prob*=0.01
            # elif step == 'No' and  not (highest_action_PS[0] in ExecuteSequence):
            #     taskNet_._expandProb *= 0.99
            #     expla._prob*=0.99
            # elif step == 'No' and  (highest_action_PS[0] in ExecuteSequence):
            #     taskNet_._expandProb *= 0.01
            #     expla._prob*=0.01

            # taskNet_._expandProb *= (1-p_l)
            expla._prob *= (1 - p_l)
            # expla._prob*= 1
            for ind in range(len(expla._pendingSet)):
                '''expla._pendingSet[ind][1]*=weight*p_l'''
                expla._pendingSet[ind][1] = expla._prob / \
                    len(expla._pendingSet)
        return
