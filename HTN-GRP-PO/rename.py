import re
import ast
import os
import sys
import numpy as np
# import json
import pandas as pd
from os.path import exists
# from script_helper import *
# import matplotlib.pyplot as plt
# from os.path import exists
# from scipy.stats import rankdata
# import argparse
# from main import parseArguments


if __name__ == "__main__":

    # path = "/home/ifrah/DDrive/Research_Projects/ICAPS2023/DGR-POMDP/tian/kitchen/log/htn/dp17_sn5_df0.95_e1_wp-5_qr5_qp-5_oh0.76_dt0.001/" 
    # out_index=12
    # for i in range(1,12):
    #     for sr in [0.8,0.9,0.95,0.99]:
    #         if i ==4:
    #             continue
    #         file1 = open(path+f"Case{i}_{sr}.txt","r")
    #         file2 = open(path+f"Case{out_index}_{sr}.txt","w")

    #         data = pd.read_csv(path+f"Case{i}_{sr}.csv")
    #         data.to_csv(path+f"Case{out_index}_{sr}.csv",  index=False)
    #     out_index+=1

   
    for agent_type in ["htn", "pomdp", "fixed_always_ask"]:
        out_index =12
        for i in range(1,12):
            for sr in [0.8,0.9,0.95,0.99]:
                if i ==4:
                    continue

                for path_i in range(2):
                    if path_i == 0:
                        path = "/home/ifrah/DDrive/Research_Projects/ICAPS2023/DGR-POMDP/tian/block/log/"+ agent_type +"/dp17_sn5_df0.95_e1_wp-5_qr5_qp-5_oh0.76_dt0.001/episode_reward/"
                                # /home/ifrah/DDrive/Research_Projects/ICAPS2023/DGR-POMDP/tian/block/log/fixed_always_ask/dp17_sn5_df0.95_e1_wp-5_qr5_qp-5_oh0.76_dt0.001/episode_reward
                        filename = f"Episode-Case{i}_{sr}.csv"
                        out = f"Episode-Case{out_index}_{sr}.csv"
                    else:
                        path = "/home/ifrah/DDrive/Research_Projects/ICAPS2023/DGR-POMDP/tian/block/log/"+ agent_type +"/dp17_sn5_df0.95_e1_wp-5_qr5_qp-5_oh0.76_dt0.001/step_reward/"

                        filename = f"Step_Case{i}_{sr}.csv"
                        out = f"Step_Case{out_index}_{sr}.csv"
                        
                    data = pd.read_csv(path+filename)
                    print(exists(path))
                    data.to_csv(path+out, index=False)
                    print("writing", path+out )
            out_index+=1