import sys
sys.dont_write_bytecode = True
from helper import *


class TaskHint(object):
    def __init__(self, output_file_name = "Case4.txt"):
        self._output_file_name = output_file_name
        self.prompt_task = {}
    
    #reset the prompt_task
    def reset(self):
        self.prompt_task = {}    
    
    #task_id: the name of the task
    #expla_prob: the probability of the corresponding explanation
    #level: the list of level of the task in this explanation, it is a list>>
    def add_task(self, task_tag, expla_prob, level):
        if task_tag in self.prompt_task.keys():
            key_value = self.prompt_task.get(task_tag)
            key_value[0] = key_value[0]+expla_prob
            key_value[1] = key_value[1]+level
            new_dict = {task_tag: key_value}
            self.prompt_task.update(new_dict)
        else:
            key_value = []
            key_value.append(expla_prob)
            key_value.append(level)
            new_dict = {task_tag:key_value}
            self.prompt_task.update(new_dict)    
        #print "after add, now the length of task hint is", len(self.prompt_task)
    def average_level(self):
        #print "go into task hint average level"
        for k, v in self.prompt_task.items():
            ave = list_average(v[1])
            key_value = []
            key_value.append(v[0])
            key_value.append(ave)
            new_dict = {k:key_value}
            self.prompt_task.update(new_dict)
            
    def get_key(self, item):
        return item[1]
        
    def print_taskhint(self):
        hint_in_level_format = {}
        for k, v in self.prompt_task.items():
            if v[1] in hint_in_level_format:
                hint_in_level_format[v[1]].append([k, v[0]])
            else:
                level_task_list = []
                level_task_list.append([k, v[0]])
                hint_in_level_format[v[1]] = level_task_list
            
        for key in hint_in_level_format:
            hint_in_level_format[key] = sorted(hint_in_level_format[key], key = self.get_key, reverse = True)
        
        with open(self._output_file_name, 'a') as f:
            f.write("Hint Output In Level Sequence: \n")
            for key in hint_in_level_format:
                line_new = "------------Level  " + str(key) + "-------------------\n"
                f.write(line_new)
                for task in hint_in_level_format[key]:
                    line_new = '{:>8}  {:<20}  {:>20}  {:>12}'.format("task name: ", task[0], "with probability of: ", round(task[1], 4))
                    f.write(line_new)
                    f.write("\n")
                f.write("\n")
            f.write("\n")    
   

    
        
        
        
        
                    
