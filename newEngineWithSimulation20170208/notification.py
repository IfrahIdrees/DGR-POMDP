#this class will accept sensor changes
#from the simulator



from Queue import *

class notification(object):
    def __init__(self):
        self._notif = Queue()
        
        #step_input = open("Case1", "r")
        step_input = open("Case2", "r")
        #step_input = open("Case3", "r")
        #step_input = open("Case4", "r")
        #step_input = open("Case5", "r")
        #step_input = open("Case6", "r")
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
            
            
            
notif = notification() 
