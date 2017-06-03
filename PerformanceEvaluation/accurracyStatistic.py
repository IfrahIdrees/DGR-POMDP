import re
import ast
from script_helper import *


sensor_reliability = [None, 0.95, 0.9, 0.8]
sensor_reliability = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]


##folder_name should be the directory where the running output is stored
folder_name = "./ExperimentResult/Case1-3/Case"
folder_name = "./ExperimentResult/Case5-6/Case"
folder_name = "./ExperimentResult/Case7-10/Case"
folder_name = "./ExperimentResult/Case11-12/Case"
folder_name = "./ExperimentResult/MCase1-3/Case"
folder_name = "./ExperimentResult/MCase5-6/Case"
#folder_name = "./ExperimentResult/MCase7-10/Case"
#folder_name = "./ExperimentResult/MCase11-12/Case"

#folder_name = "./ExperimentResultT/Case1-3/Case"
#folder_name = "./ExperimentResultT/Case5-6/Case"
#folder_name = "./ExperimentResultT/Case7-10/Case"
#folder_name = "./ExperimentResultT/Case11-12/Case"
#folder_name = "./ExperimentResultT/MCase1-3/Case"
#folder_name = "./ExperimentResultT/MCase5-6/Case"
folder_name = "./ExperimentResultT/MCase7-10/Case"
#folder_name = "./ExperimentResultT/MCase11-12/Case"


for case_num in range(7, 11):
    benchmark_file_name = folder_name + str(case_num) + "_DesiredResult.txt"
    with open(benchmark_file_name) as f:
        input_standard = f.readlines()
        f.close()
    bench_mark = []
    for step_standard in input_standard:
        step_standard_info = re.split('#|\n', step_standard)
        #print step_standard_info
        this_step_standard = {}
        this_step_standard['goal'] = ast.literal_eval(step_standard_info[0])
        this_step_standard['pendingSet'] = ast.literal_eval(step_standard_info[1])
        bench_mark.append(this_step_standard)
    
    with open('accurracyStatisticOutput.txt', 'a') as output:
        output.write("\n")
        output.close()
    for reliability in sensor_reliability:
        result_file_name = folder_name + str(case_num) + "_" + str(reliability) + ".txt"
        print "the result file name is: ", result_file_name
        with open(result_file_name) as f:
            input_result = f.readlines()
            f.close()
        k=0
        case_step_num = len(bench_mark)
        sum_point = 0
        for line in input_result:
            
            if line=='\n':
                continue
            elif line.startswith('=='):
                k=0
            else:
                thisline = re.split('\t|\n|#', line)
                print thisline
                goal_recognition_result = thisline[2:5]
                print goal_recognition_result
                
                sum_point = sum_point + stepResultTest(goal_recognition_result, thisline[5], bench_mark[k], reliability, case_num)
                k = k + 1
                
        print sum_point
        accurracy = (float)(sum_point)/(float)(case_step_num * 2 * 20)
        with open('accurracyStatisticOutput.txt', 'a') as output:
            
            output.write("Case " + str(case_num) + " reliability " + str(reliability) + ": " + str(round(accurracy, 4)) + "\n")
            output.close()
        
        
        
        
