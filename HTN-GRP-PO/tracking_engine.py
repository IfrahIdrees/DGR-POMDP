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
####                        The control of an algorithm iteration                           ####
##########################################################################


import time
from notification import *
from ExplaSet import *
from State import *
from Simulator import *
import config
import csv
from pathlib import Path
from monte_carlo_tree_search import *
from dialogue_policy import *


class Tracking_Engine(object):
    def __init__(
            self,
            no_trigger=0,
            sleep_interval=1,
            cond_satisfy=1.0,
            cond_notsatisfy=0.0,
            delete_trigger=0.001,
            non_happen=0.00001,
            otherHappen=0.75,
            file_name="Case1",
            output_file_name="Case1.txt",
            output_folder_name="otherhappen_0.75/",
            trial=0):
        self._no_trigger = no_trigger
        self._sleep_interval = sleep_interval
        self._cond_satisfy = cond_satisfy
        self._cond_notsatisfy = cond_notsatisfy
        self._delete_trigger = config.args.dt
        self._non_happen = non_happen
        self._other_happen = config.args.oh
        self._file_name = file_name
        self._output_file_name = output_file_name
        self._output_folder_name = output_folder_name
        self._p_l = 0.95  # probablity of getting observation
        self.output_case_file_name = output_file_name.split("/")[-1]
        self.reward_csv_filename = Path(
            config.args.step_dir +
            "Step_" +
            self.output_case_file_name).with_suffix('.csv')
        self.corrective_action_filename = Path(
            config.args.corrective_action_dir +
            # "Step_" +
            self.output_case_file_name
        )
        with open(self.corrective_action_filename, 'a') as f:
            f.write('\n========================\n')
        self.trial = trial
        self.INVERSE_PENDING_DICT = {"kitchen": {"turn_on_faucet": [0]},
                                     "block": {"pick_up_blockT": [0],
                                               "pick_up_blockN": [0],
                                               "pick_up_blockW": [0]
                                               }}

    def get_human_feedback(self, action_name, real_steps, action_arg=None, ):
        feedback = None
        if action_name == "ask-clarification-question":
            if action_arg == real_steps[-1]:
                feedback = config.positive_feedback
            else:
                feedback = config.negative_feedback
        return feedback

    def check_is_ha_inbelief(self, inverse_pending_action,
                             action_name, action_args=None):
        if action_name in inverse_pending_action:
            is_ha_inbelief = True
        else:
            is_ha_inbelief = False
        return is_ha_inbelief

    def extract_action_name(
            self, action_node, num_question_asked, is_question_asked):
        action_name = action_node.turn_information.chosen_action.name
        action_arg = None
        if action_name == "ask-clarification-question":
            action_arg = action_node.turn_information.chosen_action.question_asked
            # action_name = action_name + "_" + action_arg
            is_question_asked = 1
            num_question_asked += is_question_asked
        return action_name, action_arg, is_question_asked, num_question_asked

    def create_wait_action_node(self, agent_state):
        action_node = agent_state
        action_node.turn_information.chosen_action = Action("wait")
        feedback = None
        return feedback, action_node

    def start(self):
        print
        print("the engine has been started...")
        print

        notif = notification(self._file_name)  # check the current notification
        exp = explaSet(
            cond_satisfy=self._cond_satisfy,
            cond_notsatisfy=self._cond_notsatisfy,
            delete_trigger=self._delete_trigger,
            non_happen=self._non_happen,
            output_file_name=self._output_file_name)
        exp.explaInitialize()
        monte_carlo_tree = MCTS(
            config.args.mcts_dir,
            self.output_case_file_name,
            db=db,
            trial=self.trial)
        turn_information = TurnInformation(terminal=False,
                                           action_node=False)
        agent_state = AgentState(
            exp,
            turn_information)

        # always iterate
        step_index = 0
        real_steps = []
        num_questions = 0
        total_reward = 0
        total_discounted_reward = 0
        num_question_asked = 0
        gamma = 1
        total_time = 0.0
        inverse_pending_dict = self.INVERSE_PENDING_DICT[config.args.domain]
        while(notif._notif.qsize() > 0):
            is_question_asked = 0
            step, goal = notif.get_one_notif()
            real_steps.append(step)
            notif.delete_one_notif()
            if step == "pick_up_blockR":
                print("step here")
            # if no notification, and the random prob is less than
            # no_notif_trigger_prob, sleep the engine
            if step == "none" and random.random() < self._no_trigger:
                time.sleep(self._sleep_interval)

            # go through the "here"engine logic
            else:
                if step != "none":
                    sensor_notification = copy.deepcopy(
                        realStateANDSensorUpdate(
                            step, self._output_file_name, real_step=True))

                    exp.setSensorNotification(sensor_notification)

                # posterior
                start_time = time.time()
                otherHappen = exp.action_posterior()
                # robot plans dialogue action
                pipeline = [{"$match": {}},
                            {"$out": "backup_state"},
                            ]

                db._state.aggregate(pipeline)
                # db._backup_state = self.db_client.backup_state

                pipeline = [{"$match": {}},
                            {"$out": "backup_sensor"},
                            ]
                db._sensor.aggregate(pipeline)

                real_exp = copy.deepcopy(exp)

                if config.args.agent_type == "pomdp":
                    agent_state.turn_information.update_turn_information(
                        step_index, step, goal)
                    agent_state.copy_explaset(exp)
                    # agent_state.explaset =copy.deepcopy(exp)
                    if step_index == 0:
                        # is_first_real_step = True
                        feedback, action_node = self.create_wait_action_node(
                            agent_state)
                    else:
                        is_first_real_step = False
                        action_node, _ = monte_carlo_tree.rollout_loop(
                            agent_state, step, is_first_real_step)
                        # action_name = action_node.turn_information.chosen_action.name
                        # action_arg = None
                        # if action_name == "ask-clarification-question":
                        #     action_arg = action_node.turn_information.chosen_action.question_asked
                        #     action_name = action_name + "_" + action_arg
                        #     is_question_asked = 1
                        #     num_question_asked+=is_question_asked
                    action_name, action_arg, is_question_asked, num_question_asked = \
                        self.extract_action_name(
                            action_node, num_question_asked, is_question_asked)

                if config.args.agent_type == "fixed_always_ask":
                    action_node = agent_state
                    action_node.turn_information.chosen_action = AgentAskClarificationQuestion()

                    # highest_action_PS = ["", float('-inf')]
                    # for k, v in exp._action_posterior_prob.items():
                    #     if v > highest_action_PS[1]:
                    #         highest_action_PS = [k, v]
                    # exp.highest_action_PS = highest_action_PS
                    action_node.turn_information.chosen_action.question_asked = step
                    action_name, action_arg, is_question_asked, num_question_asked = \
                        self.extract_action_name(
                            action_node, num_question_asked, is_question_asked)

                '''feedback generation'''
                if config.args.agent_type in ["pomdp", "fixed_always_ask"]:
                    feedback = self.get_human_feedback(
                        action_node.turn_information.chosen_action.name,
                        real_steps,
                        action_arg=action_arg)
                elif config.args.agent_type == "htn":
                    feedback, action_node = self.create_wait_action_node(
                        agent_state)
                '''Restoring the state for next iteration, env variable in HTNcoachproblem should be reset'''
                exp = real_exp
                pipeline = [{"$match": {}},
                            {"$out": "state"},
                            ]
                db._backup_state.aggregate(pipeline)

                pipeline = [{"$match": {}},
                            {"$out": "sensor"},
                            ]
                db._backup_sensor.aggregate(pipeline)

                if otherHappen > self._other_happen:
                    # if otherHappen:
                    # wrong step handling
                    # print("action posterior after bayseian inference is",  exp._action_posterior_prob)
                    if config.args.agent_type == "htn":
                        exp.handle_exception()
                    else:
                        '''TODO: see what to do for pomdp when the action_arg can be wrong'''
                        if action_name == "ask-clarification-question" and feedback == config.positive_feedback:
                            sensor_notification = update_db(
                                step_index, step, self.corrective_action_filename)
                            exp.setSensorNotification(sensor_notification)
                            exp.action_posterior(is_correction=True)
                            length = len(exp._explaset)

                            # input step start a new goal (bottom up procedure to create ongoing status)
                            # include recognition and planning
                            # exp._delete_trigger = config._real_delete_trigger
                            exp.explaSet_expand_part1(length)

                            # belief state update
                            state = State()
                            state.update_state_belief(exp)
                            # input step continues an ongoing goal
                            # include recognition and planning
                            exp.explaSet_expand_part2(length)

                            # print("here")

                # correct step procedure
                else:
                    length = len(exp._explaset)

                    # input step start a new goal (bottom up procedure to create ongoing status)
                    # include recognition and planning
                    exp.explaSet_expand_part1(length)

                    # belief state update
                    state = State()
                    state.update_state_belief(exp)

                    # input step continues an ongoing goal
                    # include recognition and planning
                    exp.explaSet_expand_part2(length)

                if feedback is None:
                    exp.update_without_language_feedback(self._p_l)
                else:
                    if config.args.agent_type == "fixed_always_ask":
                        exp.update_with_language_feedback(
                            feedback, [action_arg, 0.99], self._p_l)
                    else:
                        # TODO:NEED TO FIX WHAT SHOULD BE PASSED
                        exp.update_with_language_feedback(
                            feedback, exp.highest_action_PS, self._p_l)
                is_haction_in_belief = self.check_is_ha_inbelief(
                    inverse_pending_dict, step)
                env_reward = monte_carlo_tree.get_step_reward(
                    is_haction_in_belief, action_node)
                total_reward += env_reward
                total_discounted_reward += env_reward * gamma
                gamma *= config.args.d

                print("\n========================")
                print(
                    "Step index is",
                    step_index,
                    "CHOSEN ACTION IS",
                    action_node.turn_information.chosen_action.name,
                    env_reward)

                inverse_pending_dict, _ = exp.pendingset_generate()

                # compute goal recognition result PROB and planning result PS
                taskhint = exp.task_prob_calculate()
                print("taskhint is", taskhint.__dict__)

                # output PROB and PS in a file
                exp.print_explaSet()
                time_per_step = time.time() - start_time

                with open(self.reward_csv_filename, 'a', newline='') as csvfile:
                    spamwriter = csv.writer(
                        csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    # spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
                    if step_index == 0 and self.trial == 1:
                        spamwriter.writerow(
                            ["step_index", "time_per_step", "action_name", "step_reward", "total_reward", "cumulative_reward", "is_question_asked"])
                    if config.args.agent_type == "htn" or action_arg is None:
                        spamwriter.writerow(
                            [step_index, time_per_step, action_node.turn_information.chosen_action.name, env_reward, total_reward, total_discounted_reward, is_question_asked])
                    else:
                        # action_name
                        # if action_arg!=None:
                        spamwriter.writerow(
                            [step_index, time_per_step, action_name + "+" + action_arg, env_reward, total_reward, total_discounted_reward, is_question_asked])
                        # else:
                        # spamwriter.writerow(
                        # [step_index, time_per_step, action_name, env_reward, total_reward, total_discounted_reward, is_question_asked])
                total_time += time_per_step
                step_index += 1
                print("go into the next loop\n\n")
                # print(
                # print
        normalized_question_asked = num_question_asked / step_index
        normalized_time = total_time / step_index
        config.episode_cumulative_reward_df.loc[len(config.episode_cumulative_reward_df.index)] = ([config.trial,
                                                                                                    total_reward,
                                                                                                    total_discounted_reward,
                                                                                                    num_question_asked,
                                                                                                    normalized_question_asked,
                                                                                                    normalized_time])

        # config.normalized_
