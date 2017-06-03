"""------------------------------------------------------------------------------------------
Hierarchical Task Recognition and Planning in Smart Homes with Partially Observability
Author: Dan Wang danwangkoala@gmail.com (May 2016 - June 2017)
Association: Computer Science, University of Waterloo.
Research purposes only. Any commerical uses strictly forbidden.
Code is provided without any guarantees.
Research sponsored by AGEWELL Networks of Centers of Excellence (NCE).
----------------------------------------------------------------------------------------------"""
################################################################################################
####                        The control of an algorithm iteration                           ####
################################################################################################

import random
import time
from notification import *
from ExplaSet import *
from State import *
from Simulator import *

class Tracking_Engine(object):
    def __init__(self, no_trigger = 0, sleep_interval = 1, cond_satisfy=1.0, cond_notsatisfy = 0.0, delete_trigger = 0.001, non_happen = 0.00001, otherHappen = 0.75, file_name = "Case1", output_file_name = "Case1.txt"):
        self._no_trigger = no_trigger
        self._sleep_interval = sleep_interval
        self._cond_satisfy = cond_satisfy
        self._cond_notsatisfy = cond_notsatisfy
        self._delete_trigger = delete_trigger
        self._non_happen = non_happen
        self._other_happen = otherHappen
        self._file_name = file_name
        self._output_file_name = output_file_name

            
    def start(self):
        print
        print "the engine has been started..."
        print
        
        notif = notification(self._file_name)   ##check the current notification
        exp = explaSet(cond_satisfy = self._cond_satisfy, cond_notsatisfy = self._cond_notsatisfy, delete_trigger = self._delete_trigger, non_happen = self._non_happen, output_file_name = self._output_file_name)
        exp.explaInitialize()  
        
        #always iterate
        while(notif._notif.qsize()>0):
            step = notif.get_one_notif()
            notif.delete_one_notif()
            
            #if no notification, and the random prob is less than no_notif_trigger_prob, sleep the engine
            if step == "none" and random.random()<self._no_trigger:
                time.sleep(self._sleep_interval)
                
            #go through the engine logic
            else:
                if step != "none":
                    sensor_notification = copy.deepcopy(realStateANDSensorUpdate(step, self._output_file_name))
                    
                    exp.setSensorNotification(sensor_notification)
                      
                # posterior
                otherHappen = exp.action_posterior()
                
                
                # wrong step detect
                if otherHappen > self._other_happen:
                    # wrong step handling
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
                exp.task_prob_calculate()
                
                #output PROB and PS in a file
                exp.print_explaSet()
                
                print "go into the next loop"
                print 
                print
                
                
        
        
        
       
            
       
            
        
    
    
