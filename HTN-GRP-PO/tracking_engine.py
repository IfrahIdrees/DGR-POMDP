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
        self._delete_trigger = delete_trigger
        self._non_happen = non_happen
        self._other_happen = otherHappen
        self._file_name = file_name
        self._output_file_name = output_file_name
        self._output_folder_name = output_folder_name
        self._p_l = 0.95  # probablity of getting observation
        self._step_dict = [
            'use_soap',
            'rinse_hand',
            'turn_on_faucet_1',
            'turn_off_faucet_1',
            'dry_hand',
            'switch_on_kettle_1',
            'switch_off_kettle_1',
            'add_water_kettle_1',
            'get_cup_1',
            'open_tea_box_1',
            'add_tea_cup_1',
            'close_tea_box_1',
            'add_water_cup_1',
            'open_coffee_box_1',
            'add_coffee_cup_1',
            'close_coffee_box_1',
            'drink']
        self.output_case_file_name = output_file_name.split("/")[1]
        self.reward_csv_filename = Path(
            self._output_folder_name +
            "Reward_" +
            self.output_case_file_name).with_suffix('.csv')
        self.trial = trial

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
            self._output_folder_name,
            self.output_case_file_name,
            db=db,
            trial=self.trial)
        agent_state = AgentState(
            exp,
            terminal=False,
            action_node=False,
            step_index=0)

        # always iterate
        step_index = 0
        while(notif._notif.qsize() > 0):
            step = notif.get_one_notif()
            notif.delete_one_notif()

            # if no notification, and the random prob is less than
            # no_notif_trigger_prob, sleep the engine
            if step == "none" and random.random() < self._no_trigger:
                time.sleep(self._sleep_interval)

            # go through the engine logic
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

                if not notif._notif.empty():
                    agent_state = AgentState(
                        exp, terminal=False, action_node=False, step_index=step_index)
                    monte_carlo_tree.rollout_loop(agent_state, step)

                # agent_state.simulate(monte_carlo_tree)

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
                    exp.handle_exception()

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

                exp.pendingset_generate()

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
                    spamwriter.writerow(
                        [step_index, time_per_step])
                step_index += 1
                print("go into the next loop\n\n")
                # print(
                # print
