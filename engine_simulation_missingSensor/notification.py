#this class will accept sensor changes
#from the simulator



from Queue import *

class notification(object):
    def __init__(self, file_name):
        self._notif = Queue()
        
        step_input = open(file_name, "r")
        
        #step_input = open("Case1", "r")     #wash_hand, correct step
        #step_input = open("Case2", "r")    #make_tea, correct step 
        #step_input = open("Case3", "r")    #make_coffee, correct step
        #step_input = open("Case4", "r")    #wash_hand || make_tea, correct step, with shared step among tasks 
        #step_input = open("Case5", "r")    #wash_hand || make_tea, correct step, sequential tasks
        #step_input = open("Case6", "r")    #wash_hand || make_tea, correct step, interleaved steps, without shared step among tasks
        #step_input = open("Case7", "r")    #wash_hand || make_tea, correct step, interleaved steps, without shared step among tasks
        #step_input = open("Case8", "r")    #wash_hand, wrong step, hard constraint violate
        #step_input = open("Case9", "r")    #wash_hand, wrong step, soft Constraint violate
        #step_input = open("Case10", "r")   #wash_hand, wrong step, soft constraint and hard constraint violate
        #step_input = open("Case11", "r")   
        steps = step_input.readlines()
        step_input.close()
        
        for step in steps:
            step = ''.join(step.split("\n"))
            self._notif.put(step)
        
    ##without deleting
    def get_one_notif(self):
        if self._notif.empty():
            return None
        else:
            return self._notif.queue[0]  
        
        
    ##delete the next element in insertion order
    def delete_one_notif(self):
        if not self._notif.empty():
            self._notif.get() 
            
            
            
#notif = notification() 
