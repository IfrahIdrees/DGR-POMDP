"""------------------------------------------------------------------------------------------
Hierarchical Task Recognition and Planning in Smart Homes with Partially Observability
Author: Dan Wang danwangkoala@gmail.com (May 2016 - June 2017)
Supervised by Prof. Jesse Hoey (https://cs.uwaterloo.ca/~jhoey/)
Association: Computer Science, University of Waterloo.
Research purposes only. Any commerical uses strictly forbidden.
Code is provided without any guarantees.
Research sponsored by AGEWELL Networks of Centers of Excellence (NCE).
----------------------------------------------------------------------------------------------"""


import pandas as pd
import argparse
from os.path import exists
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
    db = client.smart_home8


def get_output_path(args):
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # ROOT_DIR = os.path.dirname(BASE_DIR)
    output_name = "dp{}_sn{}_df{}_e{}_wp{}_qr{}_qp{}_oh{}_dt{}".format(
        # args.num_runs,
        # args.belief,
        args.max_depth,
        args.num_sims,
        args.d,
        args.e,
        args.wp,
        args.qr,
        args.qp,
        args.oh,
        args.dt
        # args.give_next_instr_reward,
        # args.give_next_instr_penalty,
    )
    # output_dir = "../outputs/{}/{}".format(args.agent_type, output_name)
    log_dir = "../logs/{}/{}/{}/".format(args.domain,
                                         args.agent_type, output_name)
    mcts_dir = log_dir + "/mcts/"
    step_dir = log_dir + "/step_reward/"
    episode_dir = log_dir + "/episode_reward/"
    corrective_action_dir = log_dir + "/corrective_actions_info/"
    # os.makedirs("../outputs", exist_ok=True)
    # os.makedirs("../outputs/{}".format(args.agent_type), exist_ok=True)

    os.makedirs("../logs/", exist_ok=True)
    # os.makedirs("../logs/{}".format(args.agent_type), exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(mcts_dir.format(args.agent_type,
                                output_name), exist_ok=True)
    os.makedirs(step_dir.format(args.agent_type,
                                output_name), exist_ok=True)
    os.makedirs(episode_dir.format(args.agent_type,
                                   output_name), exist_ok=True)
    os.makedirs(corrective_action_dir.format(args.agent_type,
                                             output_name), exist_ok=True)
    # os.makedirs("../logs/{}/{}real".format(args.agent_type), exist_ok=True)

    # os.makedirs(output_dir, exist_ok=True)

    return output_name, log_dir, mcts_dir, step_dir, episode_dir, corrective_action_dir


def parseArguments():

    # Necessary variables
    #parser.add_argument("is_random_agent", action="store_true")
    #parser.add_argument("is_heuristic_agent", action="store_true")
    # parser.add_argument("--belief", type=str, default="uniform")
    parser.add_argument(
        "--agent_type", type=str, default="htn",
        help="pomdp, random, htn, always_ask, greedy")
    # "--agent_type",
    # nargs="+",
    # default=[
    #     "pomdp",
    #     "htn",
    #     "fixed_always_ask"
    #     ],
    # help="standard, random, heuristic")
    parser.add_argument(
        "--max_depth",
        type=int,
        default=25,
        help="number of max depth")
    parser.add_argument("--num_sims", type=int, default=5,
                        help="num_sims for POMCP")
    parser.add_argument("--d", type=float, default=0.95,
                        help="discount factor")
    parser.add_argument("--e", type=int, default=0,
                        help="exploration constant")
    # parser.add_argument("--gr", type=int, default=5, help="goal reward")
    parser.add_argument("--wp", type=int, default=-5, help="wait penalty")
    parser.add_argument("--qr", type=int, default=5, help="question reward")
    parser.add_argument("--qp", type=int, default=-5, help="question penalty")
    parser.add_argument(
        "--dt",
        type=float,
        default=0.001,
        help="delete_trigger")
    parser.add_argument(
        "--domain",
        type=str,
        default=0.001,
        help="delete_trigger")
    # parser.add_argument("--give_next_instr_penalty", type=int, default=-10)
    # parser.add_argument("--num_runs", type=int, default=1)
    # parser.add_argument("--print_log", action="store_true")
    # parser.add_argument("--output_results", action="store_true")
    # parser.add_argument("--simulation_table_path", type=str, default="simulation_table.csv")
    args = parser.parse_args()

    # I/O parameters
    output_name, log_dir, mcts_dir, step_dir, episode_dir, corrective_action_dir = get_output_path(
        args)
    parser.add_argument("--output_name", type=str, default=output_name)
    parser.add_argument("--log_dir", type=str, default=log_dir)
    parser.add_argument("--mcts_dir", type=str, default=mcts_dir)
    parser.add_argument("--step_dir", type=str, default=step_dir)
    parser.add_argument("--episode_dir", type=str, default=episode_dir)
    parser.add_argument(
        "--corrective_action_dir",
        type=str,
        default=corrective_action_dir)
    # parser.add_argument("-sr", type=float, default = 0.99, help="sensor reliability")
    args = parser.parse_args()

    return parser, args


parser = argparse.ArgumentParser()
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
    sensor_reliability = [0.99, 0.95, 0.9, 0.8]
    # sensor_reliability = [0.99, 0.9, 0.8]
    # sensor_reliability = [0.95, 0.9]
    # sensor_reliability = [0.99, 0.8]
    # sensor_reliability = [0.99, 0.8]
    # sensor_reliability = [0.95]
    # trials = 51
    # trials = 11
    # trials = 8
    trials = 20
    config.seed = 5999
    config.trials = trials
    random.seed(config.seed)
    # other_happen=2
    # file =12
    # trial = 51
    # steps = 17
    # simulation = 11

    # file_nums = [1,2,3,5,7,9,10]
    # for file_num in file_nums:
    is_first_other_happen = True
    for other_happen in [0.76]:
    # for other_happen in config.np.arange(
            # other_happens[0], other_happens[1], 0.005):
        if is_first_other_happen == True:
            parser.add_argument("--oh", type=float, default=other_happen)
            is_first_other_happen = False
            parser, args = parseArguments()
            config.randomNs = [random.random()
                               #    for i in range((config.trials - 1) * 100)]
                               for i in range(2 * 30 * args.max_depth * args.num_sims * (51 - 1) * 100)]

        else:
            args.oh = other_happen

        config.args = args
        # ou

        # file_nums = [1,11]
        # file_nums = [7]
        # for file_num in file_nums:
        for file_num in range(1, 30):
            if config.args.domain == "kitchen" and file_num == 4:
                continue
            for x in sensor_reliability:
                # output file name
                # if config.RANDOM_BASELINE:
                #     output_file_name = output_folder_name + "Random_Case" + \
                #         str(file_num) + "_" + str(x) + ".txt"
                # else:
                output_file_name = args.log_dir + "Case" + \
                    str(file_num) + "_" + str(x) + ".txt"

                # input file name
                # if args.domain == "kitchen":
                # input_file_name = "../TestCases/Case" + str(file_num)
                # else:
                input_file_name = "../TestCases_" + \
                    args.domain + "/Case" + str(file_num)

                if not exists(input_file_name):
                    continue

                # each test case run 20 times
                for repeat in range(1, trials):
                    if config.RANDOM_BASELINE:
                        with open("debugrandom_no.txt", 'a') as f:
                            f.write(
                                "\n************case:" +
                                str(file_num) +
                                "-" +
                                str(x) +
                                "-" +
                                str(repeat))

                        with open("mcts_debugrandom_no.txt", 'a') as f:
                            f.write(
                                "\n************case:" +
                                str(file_num) +
                                "-" +
                                str(x) +
                                "-" +
                                str(repeat))
                    else:
                        with open("random_no.txt", 'a') as f:
                            f.write(
                                "\n************case:" +
                                str(file_num) +
                                "-" +
                                str(x) +
                                "-" +
                                str(repeat))

                        with open("mcts_random_no.txt", 'a') as f:
                            f.write(
                                "\n************case:" +
                                str(file_num) +
                                "-" +
                                str(x) +
                                "-" +
                                str(repeat))

                    # cum_rew_file_name = "{}/{}_overall_stats.csv".format(
                    # args.output_dir, output_file_name)
                    episode_filename = args.episode_dir + "Episode-Case" + \
                        str(file_num) + "_" + str(x) + ".csv"
                    if os.path.exists(episode_filename):
                        episode_cumulative_reward_df = pd.read_csv(
                            episode_filename)
                    else:
                        episode_cumulative_reward_df = pd.DataFrame(
                            columns=[
                                'Iteration#',
                                "cumu_reward",
                                "cumu_discounted_reward",
                                "num_question_asked",
                                "normalized_num_question_asked",
                                "normalized_time"])
                    config.episode_cumulative_reward_df = episode_cumulative_reward_df
                    config.trial = repeat
                    if repeat == 1:
                        # config.seed = 5999
                        config.randomIndex = 0
                        config.randomIndex = 48
                        config.realRandomIndex = 48
                        # config.randomIndex = 321

                    db.method.drop()
                    db.state.drop()
                    db.operator.drop()
                    db.sensor.drop()
                    db.Rstate.drop()
                    db.backup_state.drop()
                    db.backup_sensor.drop()
                    sensor_command = ""

                    # Some times those command do not work, add "--jsonArray"
                    # to the end of each command line
                    knowledgebase_directory = "KnowledgeBase" + "_" + args.domain + "_domain"
                    if config.RANDOM_BASELINE:
                        os.system(
                            "mongoimport --db smart_homeRANDOM --collection method --drop --file " + "../" + knowledgebase_directory + "/method.json")
                        os.system(
                            "mongoimport --db smart_homeRANDOM --collection state --drop --file " + "../" + knowledgebase_directory + "/state.json")
                        os.system(
                            "mongoimport --db smart_homeRANDOM --collection operator --drop --file " + "../" + knowledgebase_directory + "/operator.json")
                        os.system(
                            "mongoimport --db smart_homeRANDOM --collection Rstate --drop --file " + "../" + knowledgebase_directory + "/realState.json")
                    else:
                        os.system(
                            "mongoimport --db smart_home8 --collection method --drop --file " + "../" + knowledgebase_directory + "/method.json")
                        os.system(
                            "mongoimport --db smart_home8 --collection state --drop --file " + "../" + knowledgebase_directory + "/state.json")
                        os.system(
                            "mongoimport --db smart_home8 --collection operator --drop --file " + "../" + knowledgebase_directory + "/operator.json")
                        os.system(
                            "mongoimport --db smart_home8 --collection Rstate --drop --file " + "../" + knowledgebase_directory + "/realState.json")

                    # command for sensor reliability set up
                    if config.RANDOM_BASELINE:
                        if x is None:
                            sensor_command = "mongoimport --db smart_homeRANDOM --collection sensor --drop --file " + \
                                "../" + knowledgebase_directory + "/sensor_reliability/sensor.json"
                        else:
                            sensor_command = "mongoimport --db smart_homeRANDOM --collection sensor --drop --file " + "../" + knowledgebase_directory + "/sensor_reliability/sensor" + \
                                "_" + str(x) + ".json"

                    else:
                        if x is None:
                            sensor_command = "mongoimport --db smart_home8 --collection sensor --drop --file " + \
                                "../" + knowledgebase_directory + "/sensor_reliability/sensor.json"
                        else:
                            sensor_command = "mongoimport --db smart_home8 --collection sensor --drop --file " + "../" + knowledgebase_directory + "/sensor_reliability/sensor" + \
                                "_" + str(x) + ".json"
                    os.system(sensor_command)
                    print(db.list_collection_names())

                    # command for sensor missing set up
                    '''
                    sensor_command = "mongoimport --db smart_home8 --collection sensor --drop --file "+"../"+knowledgebase_directory+"/missing_sensor/sensor" + "_" + str(x) + ".json"
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
                        output_folder_name=args.log_dir,
                        trial=repeat)
                    tracking_engine.start()

                    config.episode_cumulative_reward_df.to_csv(
                        episode_filename, index=False)

                print("I am good until now")

                with open('config_info.csv', 'a', newline='') as csvfile:
                    spamwriter = csv.writer(
                        csvfile,
                        delimiter=',',
                        quotechar='|',
                        quoting=csv.QUOTE_MINIMAL)
                    # spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
                    spamwriter.writerow([file_num, str(x), str(
                        repeat), config.randomIndex, config.realRandomIndex])

else:
    print('I am being imported')
