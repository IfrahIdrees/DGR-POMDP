"""------------------------------------------------------------------------------------------
Hierarchical Task Recognition and Planning in Smart Homes with Partially Observability
Author: Dan Wang danwangkoala@gmail.com (May 2016 - June 2017)
Supervised by Prof. Jesse Hoey (https://cs.uwaterloo.ca/~jhoey/)
Association: Computer Science, University of Waterloo.
Research purposes only. Any commerical uses strictly forbidden.
Code is provided without any guarantees.
Research sponsored by AGEWELL Networks of Centers of Excellence (NCE).
----------------------------------------------------------------------------------------------"""


from os.path import exists
import numpy as np
from tracking_engine import *
import config
import os
import sys
from pymongo import MongoClient
sys.dont_write_bytecode = True
client = MongoClient()
if config.RANDOM_BASELINE:
    db = client.smart_homeRANDOM
else:
    db = client.smart_homeextended_domain

if __name__ == '__main__':

    ############                global variables                ##############
    #######################################################
    # if there is no notification, the engine still should run the whole
    # update process if the generated random is bigger than
    # no_notif_trigger_prob
    no_notif_trigger_prob = 0.5

    # sleep interval
    interval = 1

    # conditional probability of p(s|s_t-1, a_t)
    cond_satisfy = 1.0
    cond_notsatisfy = 0.0

    # threshhold that an explanation is no longer maintain
    delete_trigger = 0.001  # 0.0004# 0.001 (orignal)

    # if there is a notification, the probability that nothing happend
    nothing_happen = 0.01

    # the otherHappen triggering threshhold
    # other_happen = 0.76 #0.75 #0.68 try 0.78 next
    other_happens = [0.765, 0.78]  # 0.75 #0.68 try 0.78 next
    other_happens = [0.76, 0.765]  # 0.75 #0.68 try 0.78 next

    # sensor set up files
    # sensor_reliability = [0.99, 0.95, 0.9, 0.8]
    sensor_reliability = [0.99, 0.95, 0.9, 0.8]
    # sensor_reliability = 	[0.95, 0.9, 0.8, 0.75]

    trials = 21
    config.seed = 5999
    config.trials = trials
    random.seed(config.seed)
    config.randomNs = [random.random()
                       for i in range((config.trials - 1) * 100)]

    # file_nums = [1,2,3,5,7,9,10]
    # for file_num in file_nums:
    for other_happen in np.arange(other_happens[0], other_happens[1], 0.005):
        output_folder_name = "otherhappen_" + str(other_happen) + "/"
        if not exists(output_folder_name):
            os.mkdir(output_folder_name)
            with open(output_folder_name + "parameters.txt", 'a') as f:
                f.write(
                    "otherhappen-" +
                    str(other_happen) +
                    "delete trigger-:" +
                    str(delete_trigger))

        # file_nums = [9]
        # for file_num in file_nums:
        for file_num in range(13, 14):
            for x in sensor_reliability:
                # output file name
                if config.RANDOM_BASELINE:
                    output_file_name = output_folder_name + "Random_Case" + \
                        str(file_num) + "_" + str(x) + ".txt"
                else:
                    output_file_name = output_folder_name + "Case" + \
                        str(file_num) + "_" + str(x) + ".txt"

                # input file name
                input_file_name = "../TestCases/BlockTests/Case" + str(file_num)
                if not exists(input_file_name):
                    continue

                # each test case run 20 times
                for repeat in range(1, trials):
                    if config.RANDOM_BASELINE:
                        with open("debugrandom_no.txt", 'a') as f:
                            f.write(
                                "************case:" +
                                str(file_num) +
                                "-" +
                                str(x) +
                                "-" +
                                str(repeat))
                    else:
                        with open("random_no.txt", 'a') as f:
                            f.write(
                                "************case:" +
                                str(file_num) +
                                "-" +
                                str(x) +
                                "-" +
                                str(repeat))
                    if repeat == 1:
                        # config.seed = 5999
                        config.randomIndex = 0
                        config.randomIndex = 48
                        # config.randomIndex = 321

                    db.method.drop()
                    db.state.drop()
                    db.operator.drop()
                    db.sensor.drop()
                    db.Rstate.drop()
                    sensor_command = ""

                    # Some times those command do not work, add "--jsonArray"
                    # to the end of each command line
                    if config.RANDOM_BASELINE:
                        os.system(
                            "mongoimport --db smart_homeRANDOM --collection method --drop --file ../KnowledgeBase_block_domain/method.json")
                        os.system(
                            "mongoimport --db smart_homeRANDOM --collection state --drop --file ../KnowledgeBase_block_domain/state.json")
                        os.system(
                            "mongoimport --db smart_homeRANDOM --collection operator --drop --file ../KnowledgeBase_block_domain/operator.json")
                        os.system(
                            "mongoimport --db smart_homeRANDOM --collection Rstate --drop --file ../KnowledgeBase_block_domain/realState.json")
                    else:
                        os.system(
                            "mongoimport --db smart_homeextended_domain --collection method --drop --file ../KnowledgeBase_block_domain/method.json")
                        os.system(
                            "mongoimport --db smart_homeextended_domain --collection state --drop --file ../KnowledgeBase_block_domain/state.json")
                        os.system(
                            "mongoimport --db smart_homeextended_domain --collection operator --drop --file ../KnowledgeBase_block_domain/operator.json")
                        os.system(
                            "mongoimport --db smart_homeextended_domain --collection Rstate --drop --file ../KnowledgeBase_block_domain/realState.json")

                    # command for sensor reliability set up
                    if config.RANDOM_BASELINE:
                        if x is None:
                            sensor_command = "mongoimport --db smart_homeRANDOM --collection sensor --drop --file ../KnowledgeBase_block_domain/sensor_reliability/sensor.json"
                        else:
                            sensor_command = "mongoimport --db smart_homeRANDOM --collection sensor --drop --file ../KnowledgeBase_block_domain/sensor_reliability/sensor" + \
                                "_" + str(x) + ".json"

                    else:
                        if x is None:
                            sensor_command = "mongoimport --db smart_homeextended_domain --collection sensor --drop --file ../KnowledgeBase_block_domain/sensor_reliability/sensor.json"
                        else:
                            sensor_command = "mongoimport --db smart_homeextended_domain --collection sensor --drop --file ../KnowledgeBase_block_domain/sensor_reliability/sensor" + \
                                "_" + str(x) + ".json"
                    os.system(sensor_command)
                    print(db.list_collection_names())

                    # command for sensor missing set up
                    '''
                    sensor_command = "mongoimport --db smart_homeextended_domain --collection sensor --drop --file ../KnowledgeBase_block_domain/missing_sensor/sensor" + "_" + str(x) + ".json"
                    os.system(sensor_command)
                    '''

                    with open(output_file_name, 'a') as f:
                        f.write('\n========================\n')
                    print(
                        "file number is",
                        output_file_name,
                        "trial number is",
                        repeat)

                    tracking_engine = Tracking_Engine(
                        no_trigger=no_notif_trigger_prob,
                        sleep_interval=interval,
                        cond_satisfy=cond_satisfy,
                        cond_notsatisfy=cond_notsatisfy,
                        delete_trigger=delete_trigger,
                        otherHappen=other_happen,
                        file_name=input_file_name,
                        output_file_name=output_file_name,
                        output_folder_name=output_folder_name)
                    tracking_engine.start()

                print("I am good until now")

else:
    print('I am being imported')
