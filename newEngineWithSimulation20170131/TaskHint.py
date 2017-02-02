import sys
sys.dont_write_bytecode = True
from helper import *


class TaskHint(object):
    prompt_task = {}
    
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
    
    def print_taskhint(self):
        print "go into task hint print"
        for k, v in self.prompt_task.items():
            print "task name:", k
            print "task prob:", v[0]
            print "task leve:", v[1]
            print "~~~~~~~~~~~~~~~~~~~~~~~"
            
