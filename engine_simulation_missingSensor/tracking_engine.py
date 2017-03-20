import random
import time
from notification import *
from ExplaSet import *
from State import *
from Simulator import *



class Tracking_Engine(object):
    def __init__(self, no_trigger = 0, sleep_interval = 1, cond_satisfy=1.0, cond_notsatisfy = 0.0, delete_trigger = 0.001, non_happen = 0.00001, otherHappen = 0.75, file_name = "Case4", output_file_name = "Case4.txt"):
        self._no_trigger = no_trigger
        self._sleep_interval = sleep_interval
        self._cond_satisfy = cond_satisfy
        self._cond_notsatisfy = cond_notsatisfy
        self._delete_trigger = delete_trigger
        self._non_happen = non_happen
        self._other_happen = otherHappen
        self._file_name = file_name  ##this is the input file name
        self._output_file_name = output_file_name

            
    def start(self):
        print
        print "the engine has been started..."
        print
        
        notif = notification(self._file_name)   ##check the current notification
        exp = explaSet(cond_satisfy = self._cond_satisfy, cond_notsatisfy = self._cond_notsatisfy, delete_trigger = self._delete_trigger, non_happen = self._non_happen, output_file_name = self._output_file_name)
        exp.explaInitialize()
        #exp.print_explaSet()
        
        
        
        #always iterate
        while(notif._notif.qsize()>0):
            step = notif.get_one_notif()
            notif.delete_one_notif()
            
            #if no notification, and the random prob is less than no_notif_trigger_prob
    #sleep the engine
            
            if step == "none" and random.random()<self._no_trigger:
                time.sleep(self._sleep_interval)
                
            #go through the engine logic to update    
            else:
                if step != "none":
                    sensor_notification = copy.deepcopy(realStateANDSensorUpdate(step, self._output_file_name))
                    #print "the sensor notification: ", sensor_notification
                    exp.setSensorNotification(sensor_notification)  
                # Calcuate the posterior prob of each action in pending set
                otherHappen = exp.action_posterior()
                #print "probability of other happend is: ", otherHappen
                
                # Go into the exception happen procedure
                if otherHappen > self._other_happen:
                    #print "come into handle exception because of otherHappen", otherHappen
                    exp.handle_exception()
                    
                # Go into the normal update procedure
                else:
                    length = len(exp._explaset)
                    
                    ##update the explanation set, part 1. 
                    exp.explaSet_expand_part1(length)
                    print "after part 1"
                    print len(exp._explaset)
                    
                    #udpate the state
                    state = State()
                    state.update_state_belief(exp)
                    
                    #update the explanation set, part 2
                    exp.explaSet_expand_part2(length)
                    print "after part 2"
                    print len(exp._explaset)

                #generate pending set         
                exp.pendingset_generate()
                
                #calculate inner node prob, This would be used for hint
                exp.task_prob_calculate()
                
                #print "Explanation Number:  ", len(exp._explaset)
                exp.print_explaSet()
                
                
                
                
                print "go into the next loop"
                print 
                print
                
                
        
        
        
        '''
        #iterate with notification 
        while(notif._notif.qsize()>0):
            step = notif.get_one_notif()
            notif.delete_one_notif()
            sensor_notification = []
            #if no notification, and the random prob is less than no_notif_trigger_prob
    #sleep the engine
            
            if step == "none" and random.random()<self._no_trigger:
                time.sleep(self._sleep_interval)
            elif step!= "none":
                sensor_notification = copy.deepcopy(realStateANDSensorUpdate(step, self._output_file_name))
                if len(sensor_notification) == 0:
                    time.sleep(self._sleep_interval)
            #go through the engine logic to update    
                else:
                    
                    if step != "none":
                        sensor_notification = copy.deepcopy(realStateANDSensorUpdate(step, self._output_file_name))
                        #print "the sensor notification is:---------- "
                        #print sensor_notification
                       
                    exp.setSensorNotification(sensor_notification)  
                    # Calcuate the posterior prob of each action in pending set
                    otherHappen = exp.action_posterior()
                    #print "probability of other happend is: ", otherHappen
                    
                    # Go into the exception happen procedure
                    if otherHappen > self._other_happen:
                        exp.handle_exception()
                        
                    # Go into the normal update procedure
                    else:
                        length = len(exp._explaset)
                        
                        ##update the explanation set, part 1. 
                        exp.explaSet_expand_part1(length)
                        
                        #udpate the state
                        state = State()
                        state.update_state_belief(exp)
                        
                        #update the explanation set, part 2
                        exp.explaSet_expand_part2(length)

                    #generate pending set         
                    exp.pendingset_generate()
                    
                    #calculate inner node prob, This would be used for hint
                    exp.task_prob_calculate()
                    
                    #print "Explanation Number:  ", len(exp._explaset)
                    exp.print_explaSet()
                    
                    
                    
                    
                    print "go into the next loop"
                    print 
                    print
                
                    
        '''                                         
            
            
       
            
        
    
    
